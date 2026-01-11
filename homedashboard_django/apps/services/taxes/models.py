from django.db import models
from classutils.models import BaseModel
from apps.core.common.models import File
from datetime import datetime
# Create your models here.

class Category(models.Model):
    class Meta():
        ordering = ['name']
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TaxYear(models.Model):
    class Meta:
        db_table = 'tax_year'
        ordering = ['-year']
    year = models.PositiveIntegerField(primary_key=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    tax_return = models.ForeignKey(File, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return str(self.year)

class Business(BaseModel):
    name = models.CharField(max_length=255)
    ein = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Ledger(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'tax_ledger'
        ordering = ['tax_year','description']

    tax_year = models.ForeignKey(TaxYear,limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    fk_business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Entity')
    fk_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Category')
    description = models.TextField(blank=True)
    amount_payable = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Payable', null=True, blank=True)
    amount_receivable = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Receivable', null=True, blank=True)
    date = models.DateField(default=datetime.now)
    receipt = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags like 'mileage, gas'")

    def __str__(self):
        label = f"{self.tax_year.year} - ${self.amount_payable if self.amount_payable else self.amount_receivable} - {str(self.fk_category) if self.fk_category else 'Uncategorized'}"
        return f"{label} ({'Personal' if self.fk_business is None else self.fk_business.name})"
