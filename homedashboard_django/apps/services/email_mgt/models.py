from django.db import models
from datetime import datetime
from apps.core.account.models import User

# Create your models here.
class DKIM(models.Model):
    class Meta:
        db_table = "email_dkim"

    domain=models.TextField(max_length=100, blank=True, null=True)
    org=models.CharField(max_length=100, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    extra_contact=models.CharField(max_length=100, blank=True, null=True)
    report_id=models.CharField(max_length=100)
    start_date=models.DateTimeField( blank=True, null=True)
    end_date=models.DateTimeField( blank=True, null=True)
    adkim=models.CharField(max_length=1, blank=True, null=True)
    aspf=models.CharField(max_length=1, blank=True, null=True)
    dkim_policy=models.CharField(max_length=10, blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dkim_entered_by')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dkim_updated')

    def __str__(self):
        return f"{self.start_date} - {self.domain}"
    
class DKIM_Record(models.Model):
    class Meta:
        db_table = "email_dkim_record"

    fk_dkim_id = models.ForeignKey(DKIM, on_delete=models.SET_NULL, null=True, related_name='dkim_record')    
    source_ip = models.GenericIPAddressField(blank=True, null=True)
    record_type = models.CharField(max_length=10, blank=True, null=True)
    domain = models.TextField(max_length=100, blank=True, null=True)
    selector = models.CharField(max_length=100, blank=True, null=True)
    result = models.BooleanField(default=False)

    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dkim_record_entered_by')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dkim_record_updated')

    def __str__(self):
        return f"{self.fk_dkim_id} - {self.domain} - {self.record_type}: {self.result}"