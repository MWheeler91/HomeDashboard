from django.db import models
from django.utils import timezone
from datetime import datetime
from account.models import User

# Create your models here.

class Error(models.Model):
    class Meta:
        db_table = "Error_log"
    
    app = models.TextField(max_length=25)
    funct = models.TextField(max_length=25)
    file = models.TextField(max_length=50)
    error_type = models.TextField()
    error = models.TextField()
    user =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='error_user')
    # additonal field when inserting errors from the error log when there is a DB cannt be reached
    error_time = models.DateTimeField(default=timezone.now)

    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='error_entered_by')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='error_updated')

    def save(self, *args, **kwargs):
        # Set default entered_by to the user with the username 'SYS'
        if not self.entered_by:
            self.entered_by = User.objects.filter(username='SYS').first()

        super(Error, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.app} - {self.funct} - {self.file} - {self.date_entered}"


class StackTrace(models.Model):
    class Meta:
        db_table = "Error_Stacktrace"

    TRACE_LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    error_id = models.CharField(max_length=255)
    stack_trace = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    additional_data = models.JSONField(null=True, blank=True)
    trace_level = models.CharField(
        max_length=10,
        choices=TRACE_LEVEL_CHOICES,
        default='ERROR',  # Default to ERROR level
    )

    def __str__(self):
        return f"{self.error_type}: {self.error} at {self.timestamp} - Level: {self.trace_level}"
