from django.db import models
from apps.infra.devices.models import ManagedDevice
from apps.core.account.models import User
from classutils.models import BaseModel

# Create your models here.
class MonitoringConfig(BaseModel):
    class meta:
        db_table = 'monitoring_config'

    fk_device_id = models.ForeignKey(ManagedDevice, on_delete=models.CASCADE, related_name='config')
    brute_force_monitoring = models.BooleanField(default=False ) 
    package_checking = models.BooleanField(default=False)
    interval = models.IntegerField(default=60, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.fk_device_id.hostname} Config'

class SystemSnapshot(BaseModel):
    fk_device_id = models.ForeignKey(ManagedDevice, on_delete=models.CASCADE, related_name='snapshots')
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ram_used_mb = models.IntegerField(blank=True, null=True)
    disk_free_gb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disk_used_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    net_recv_mb = models.FloatField(blank=True, null=True)
    net_sent_mb = models.FloatField(blank=True, null=True)
    uptime = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.fk_device_id.hostname} snapshot {self.timestamp}'

class SecurityAlert(BaseModel):
    fk_device_id = models.ForeignKey(ManagedDevice, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    source_ip = models.GenericIPAddressField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.fk_device_id.hostname} - {self.alert_type} @ {self.timestamp}'


class ManualCheckLog(models.Model):
    fk_device_id = models.ForeignKey(ManagedDevice, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=50)  # e.g., "failed_logins"
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    result_summary = models.TextField()
    checked_at = models.DateTimeField(auto_now_add=True)



