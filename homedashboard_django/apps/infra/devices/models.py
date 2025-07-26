from django.db import models
from classutils.models import BaseModel
from rest_framework.authtoken.models import Token
from apps.core.account.models import User

OS_CHOICES = [
    ("Windows", "Windows"),
    ("Linux", "Linux"),
    ("MacOS", "MacOS")
]
Type_CHOICES = [
    ("server", "Server"),
    ("pc", "PC"),
    ("yubikey", "YubiKey"),
]
key_CHOICES = [
    ("rsa", "RSA"),
    ("ed25519 ", "ed25519 ")
]


# Create your models here.
class ManagedDevice(BaseModel):
    class Meta:
        db_table = 'managed_devices'

    fk_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name='fk_user')
    hostname = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    os = models.CharField(max_length=20, choices=OS_CHOICES)
    device_type = models.CharField(max_length=20, choices=Type_CHOICES)
    is_active = models.BooleanField(default=True)
    is_virtual = models.BooleanField(default=False)
    is_public_facing = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    has_keys = models.BooleanField(default=False)
    needs_keys = models.BooleanField(default=True)
    kernel_version = models.CharField(max_length=100, blank=True, null=True)
    cpu_cores = models.IntegerField(blank=True, null=True)
    ram_total_mb = models.IntegerField(blank=True, null=True)
    disk_total_gb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    agent_version = models.CharField(max_length=20, blank=True, null=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname
    

class DeviceAuth(models.Model):
    device = models.OneToOneField(ManagedDevice, on_delete=models.CASCADE, related_name='auth')
    token = models.OneToOneField(Token, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auth for {self.device.hostname}"  

class SshKeys(BaseModel):
    class Meta:
        db_table = 'ssh_keys'

    fk_device_id = models.ForeignKey(ManagedDevice, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50)
    public_key = models.TextField()
    key_type = models.CharField(choices=key_CHOICES)
    comments = models.CharField(max_length=255, blank=True,null=True)


    def __str__(self):
        return self.name 