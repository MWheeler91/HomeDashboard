from django.db import models
import os
from django.conf import settings
from datetime import datetime
from account.models import User


def upload_image(instance, filename):
    upload_to = os.path.join(settings.BASE_DIR, 'images/')
    return os.path.join(upload_to, filename)


# Create your models here.
class App(models.Model):
    app_name = models.CharField(max_length=50)
    web_address = models.CharField(max_length=150)
    icon = models.ImageField(upload_to=os.path.join('static/images'), blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_vue_app = models.BooleanField(default=False)
    login_required = models.BooleanField(default=False)

    is_monitoring = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    monitoring_port = models.IntegerField(blank=True, null=True, default=5000)

    def __str__(self):
        return self.app_name


class ServerStatus(models.Model):
    app = models.ForeignKey(App, on_delete=models.SET_NULL, blank=True, null=True)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    host_name = models.CharField(max_length=50, blank=True, null=True)

    cpu_cores = models.IntegerField(blank=True, null=True)
    cpu_sockets = models.IntegerField(blank=True, null=True)
    cpu_usage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    disc_space = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disc_space_free = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    disc_percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    network_recv = models.FloatField()
    network_sent = models.FloatField()

    uptime = models.CharField(max_length=25)

    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='monitors_entered')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='monitors_updated')


    def save(self, *args, **kwargs):
        # Ensure field2 is not zero to avoid division by zero
        if self.disc_space_free != 0:
            self.disc_percentage = self.disc_space / self.disc_space_free
        else:
            self.total = None  # Or set to 0 or some default value as needed
        super().save(*args, **kwargs)