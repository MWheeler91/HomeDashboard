from celery import shared_task
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
import email
from email import policy
import gzip
import io
import xmltodict
from django.core.mail import send_mail
from django.utils.timezone import make_aware
import environ
import datetime, timedelta
from models import DKIM, DKIM_Record
import logging
from error_logging.logger import ErrorLogger
# logging
logger = logging.getLogger(__name__)

# SerEnvironment
env = environ.Env()

# Google vars
twenty_four_hours_ago = int((datetime.utcnow() - timedelta(days=1)).timestamp())

# ---- Gmail API Authentication ----
SERVICE_ACCOUNT_FILE = env('SERVICE_ACCOUNT_FILE')
SCOPES = env('SCOPES')
USER_EMAIL = env('USER_EMAIL')

# Authenticate with Gmail API
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
).with_subject(USER_EMAIL)

service = build("gmail", "v1", credentials=credentials)


def create_dkim_record(dkim, source_ip, record_type, domain, selector, result):
    try:
        DKIM_Record.objects.create(
            dkim_id=dkim,
            source_ip=source_ip,
            record_type=record_type,
            domain=domain,
            selector=selector,
            result=result,
        )
    except Exception as e:
        ErrorLogger().log_error(user=None, app="email_mgt", funct="create_dkim_record", file="task.py", error=str(e))

        
def save_xml_to_db(xml_data):
    try:
        dmarc_report = xmltodict.parse(xml_data)

        metadata = dmarc_report.get("feedback", {}).get("report_metadata", {})
        records = dmarc_report.get("feedback", {}).get("record", [])
        policy = dmarc_report.get("feedback", {}).get("policy_published", {})

        report_id = metadata.get("report_id")

        start_time = make_aware(datetime.utcfromtimestamp(int(metadata.get("date_range", {}).get("begin", 0))))
        end_time = make_aware(datetime.utcfromtimestamp(int(metadata.get("date_range", {}).get("end", 0))))

        # Save DKIM report
        try:
            dkim, created = DKIM.objects.get_or_create(
                report_id=report_id,
                defaults={
                    "domain": policy.get("domain") or None,
                    "org": metadata.get("org_name") or None,
                    "email": metadata.get("email") or None,
                    "extra_contact": metadata.get("extra_contact") or None,
                    "start_date": start_time,
                    "end_date": end_time,
                    "adkim": policy.get("adkim") or None,
                    "aspf": policy.get("aspf") or None,
                    "dkim_policy": policy.get("dkim_policy") or None,
                }
            )
        except Exception as e:
            ErrorLogger().log_error(user=None, app="email_mgt", funct="save_xml_to_db", file="task.py", error=str(e))
            return

        
        if not isinstance(records, list):  
            records = [records]

        # Save DKIM records
        for record in records:
            source_ip = record["row"].get("source_ip")

            auth_results = record.get("auth_results", {})
            if not isinstance(auth_results, dict):
                continue  
            
            for record_type, details in auth_results.items():
                record_type_upper = record_type.upper()
                if isinstance(details, list):
                    for entry in details:
                        create_dkim_record(dkim, source_ip, record_type_upper, entry.get("domain"), entry.get("selector"), entry.get("result"))
                else:
                    create_dkim_record(dkim, source_ip, record_type_upper, details.get("domain"), details.get("selector"), details.get("result"))
           
        return 0
    except Exception as e:
        ErrorLogger().log_error(user=None, app="email_mgt", funct="save_xml_to_db", file="task.py", error=str(e))
        return 1


@shared_task
def fetch_dmarc_reports():
    try:
        # Search for unread emails with "DMARC" in the subject
        query = f'label:"DMARC" after:{twenty_four_hours_ago}'
        results = service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])

        for msg in messages:
            err = 0 # Error counter
            msg_id = msg["id"]
            message = service.users().messages().get(userId="me", id=msg_id, format="raw").execute()
            raw_email = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
            msg_obj = email.message_from_bytes(raw_email, policy=policy.default)

            for part in msg_obj.walk():
                if part.get_content_type() == "application/gzip" and part.get("Content-Disposition") == "attachment":
                    attachment = part.get_payload(decode=True)

                    with gzip.open(io.BytesIO(attachment), "rb") as f:
                        xml_data = f.read().decode()
                        # returns 0 if no errors or 1 if there was an error writing to the DB
                        err += save_xml_to_db(xml_data)
            #  if no errors mark email as read
            if err == 0:
                # Mark email as read
                service.users().messages().modify(
                    userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
                ).execute()


    except Exception as e:
        ErrorLogger().log_error(user=None, app="email_mgt", funct="fetch_dmarc_reports", file="task.py", error=str(e))
