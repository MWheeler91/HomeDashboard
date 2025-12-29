from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.html import format_html
from django.utils import timezone
from django.db import models
from django.contrib import admin
# from unfold.contrib.forms.widgets import WysiwygWidget 
from django_quill.widgets import QuillWidget

User = get_user_model()

MMDDYYYY = "%m/%d/%Y"
MMDDYYYY_HHMM = "%m/%d/%Y %H:%M"
HHMM = "%H:%M"

class BaseModelAdmin(admin):
    base_readonly_fields = (
        "id",
        "entered_by",
        "date_entered",
        "last_updated",
        "last_updated_by",
        # "admin_audit_block",
    )

    formfield_overrides = {
        models.TextField: {
            "widget": QuillWidget(attrs={"class": "w-full min-h-64"})  # Quill for all TextFields
        },
    }

    def get_readonly_fields(self, request, obj=None):
        valid_fields = []
        model = self.model
        for field in self.base_readonly_fields:
            if hasattr(model, field) or hasattr(self, field):
                valid_fields.append(field)
        return valid_fields + list(super().get_readonly_fields(request, obj))

    def get_list_display(self, request):
        default_list_display = super().get_list_display(request)
        if "id" not in default_list_display:
            return tuple(default_list_display)
        return default_list_display

    def get_system_user(self):
        return User.objects.get(username="sys")


    def save_model(self, request, obj, form, change):
        user = request.user
        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            user = self.get_system_user()

        if not change and not getattr(obj, "entered_by", None):
            obj.entered_by = user
        obj.last_updated_by = user

        super().save_model(request, obj, form, change)
    