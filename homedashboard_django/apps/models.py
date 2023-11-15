from django.db import models
import os
from django.conf import settings


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

    def __str__(self):
        return self.app_name


