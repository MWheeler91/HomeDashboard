from django import forms
from .models import Ledger
from apps.core.common.models import Category 
class WriteOffForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Determine if this is a bound form (POST) or unbound (initial display)
        business = self.initial.get('business') or self.data.get('business')

        # Filter category field based on whether it's a business write-off
        if business:
            self.fields['category'].queryset = Category.objects.filter(is_tax_business=True)
        else:
            self.fields['category'].queryset = Category.objects.filter(is_tax_personal=True)