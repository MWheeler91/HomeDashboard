from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = (
        'entered_by',
        'date_entered',
        'last_updated_date',
        'last_updated_time',
        'last_updated_by'
    )

    def get_system_user(self):
        return User.objects.get(username="sys")

    def save_model(self, request, obj, form, change):
        user = request.user
        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            user = self.get_system_user()

        if not change and not obj.entered_by:
            obj.entered_by = user
        obj.last_updated_by = user

        super().save_model(request, obj, form, change)
