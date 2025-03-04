import logging
import traceback
from django.db.utils import IntegrityError, OperationalError
from .models import Error, StackTrace
from account.models import User
from django.utils.timezone import now
from django.db import transaction
import csv
import inspect
import os

"""
Purpose: Manage all error logging in 1 file
    Log_Error:
        1.  Get user object from the database ( if no user use SYS user )
        2.  Attept to write error to the database Error table.
    get_user:
        1. Attempt to get user object from DB
        2. If user is not found default to sys user ( write User cannot be found to the error table)
    write_to_file:
        1.  If DB is unreachable write error to .CSV file for Celery task to process later
"""

logger = logging.getLogger("error_logger")

def serialize_argument(arg):
    try:
        return str(arg)
    except Exception:
        return "Error Parsing Parameters"

class ErrorLogger:
    @staticmethod
    def log_error(user, app, file, funct, error, stack_trace, sys_user="SYS", error_type='Exception'):
        try:
            frame = inspect.currentframe().f_back  # Get the caller's frame
            call_args = inspect.getargvalues(frame)  # Get arguments passed to the calling function
            
            func_args_list = {arg: serialize_argument(call_args.locals[arg]) for arg in call_args.args}

            user_obj = ErrorLogger.get_user(sys_user if not user else user)

            try:
                with transaction.atomic():
                    err = Error.objects.create(
                        app = app,
                        funct = funct,
                        file = file,
                        error =str (error),
                        error_type = error_type,
                        user = user_obj
                    )
                    if stack_trace is not None:
                        ErrorLogger.log_trace(err, stack_trace, func_args_list)
            except Exception as e:
                logger.error(f"Error logging to DB failed: {e}")
                logger.error(f"Error details: {traceback.format_exc()}")

        except (IntegrityError, OperationalError) as db_error:
            # logger.error(f"Database error while logging error: {db_error}")
            ErrorLogger.write_to_file(user, app, file, funct, error, error_type)
            ErrorLogger.write_to_file(user, app, file, funct, str(db_error), 'DB_Error')

        except Exception as e:
            # logger.error(f"Unexpected error during logging: {e}")
            # logger.error(f"Error details: {traceback.format_exc()}")
            ErrorLogger.write_to_file(user, app, file, funct, error, error_type)

    @staticmethod
    def log_trace(err, stack_trace, func_args_list):
        try:
            trace_level = ErrorLogger.get_trace_level(stack_trace)
            StackTrace.objects.create (
                error_id = err,
                stack_trace = str(stack_trace),
                additional_data = func_args_list,
                trace_level = trace_level
            )
        except (IntegrityError, OperationalError) as db_error:
            # logger.error(f"Database error while logging error: {db_error}")
            ErrorLogger.write_to_file('SYS', 'Error_mgt', 'logger.py', 'log_trace', str(db_error), 'DB_Error')
        except Exception as e:
            # logger.error(f"Unexpected error during logging: {e}")
            # logger.error(f"Error details: {traceback.format_exc()}")
            ErrorLogger.write_to_file('SYS', 'Error_mgt', 'logger.py', 'log_trace', str(e), 'Exception')

    @staticmethod
    def get_user(user):
        try:
            return User.objects.get(username=user)
        except User.DoesNotExist as e:
            ErrorLogger.log_error(user, 'Error Logging', 'get_user', 'logger.py', e, 'User Does Not Exist')
            return User.objects.get(username="SYS")
        except Exception as e:
            # Catch any other errors and log them to file
            logger.error(f"{user},error_logging,logger.py,get_user,{e},Exception")
            logger.error(f"get_user error: {traceback.format_exc()}")
            ErrorLogger.log_error(user, 'Error Logging', 'get_user', 'logger.py', e)
            return None  # Avoid breaking main execution

    @staticmethod
    def write_to_file(user, app, file, funct, error, error_type):
        log_dir = "logs"
        log_file_path = os.path.join(log_dir, "error_log_fallback.csv")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir) 
        try:
            with open(log_file_path, mode='a', newline='') as log_file:
                csv_writer = csv.writer(log_file)
                # Write header if file is empty
                if log_file.tell() == 0:
                    csv_writer.writerow(["user", "app", "file", "funct", "error", "error_type", "timestamp"])

                csv_writer.writerow([user, app, file, funct, str(error), error_type, now()])
                logger.info(f"Error written to fallback log file: {log_file_path}")
        
        except IOError as e:
            logger.error(f"Error writing to file {log_file_path}: {e}")
            logger.error(f"Write-to-file error: {traceback.format_exc()}")

    @staticmethod
    def get_trace_level(stack_trace):
        message = stack_trace.lower()
        
        if "fatal" in message or "critical" in message:
            return 'CRITICAL'
        elif "timeout" in message or "unreachable" in message:
            return 'ERROR'
        elif "not found" in message or "missing" in message:
            return 'WARNING'
        else:
            return 'DEBUG'
