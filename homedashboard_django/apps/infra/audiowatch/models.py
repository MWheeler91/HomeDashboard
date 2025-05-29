from django.db import models
from apps.infra.devices.models import ManagedDevice
# Create your models here.
from django.db import models
from apps.core.account.models import User
from datetime import datetime

class MicMonitorConfig(models.Model):
    fk_machine_id = models.ForeignKey(ManagedDevice, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_active': True, 'is_virtual': False}, related_name='MicMonitorConfig_fk')
    warning_threshold = models.FloatField()  # e.g. -20.0 dB
    cutoff_threshold = models.FloatField()   # e.g. -10.0 dB
    cooldown = models.IntegerField()
    is_active = models.BooleanField(default=True)
    

    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='MicMonitorConfig_entered')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='MicMonitorConfig_updated')

    def __str__(self):
        return f"{self.fk_machine_id} config"


class MicEventLog(models.Model):
    fk_machine_id = models.ForeignKey(ManagedDevice, on_delete=models.CASCADE,limit_choices_to={'is_active': True, 'is_virtual': False}, related_name='MicEventLog_fk')
    volume = models.FloatField()
    event_type = models.CharField(max_length=10)  # "warning" or "cutoff"
    timestamp = models.DateTimeField(auto_now_add=True)

    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='MicEventLog_entered')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='MicEventLog_updated')

    def __str__(self):
        return f"{self.fk_machine_id} - {self.event_type} - {self.volume:.2f} dB"