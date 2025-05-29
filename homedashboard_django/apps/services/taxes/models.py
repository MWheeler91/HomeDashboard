from django.db import models
from classutils.models import BaseModel
from apps.core.common.models import File, Category
# Create your models here.

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

class WriteOff(BaseModel):
    class Meta:
        ordering = ['tax_year','description']

    tax_year = models.ForeignKey(TaxYear,limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    receipt = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags like 'mileage, gas'")

    def __str__(self):
        label = f"{self.tax_year.year} - ${self.amount} - {str(self.category) if self.category else 'Uncategorized'}"
        return f"{label} ({'Personal' if self.business is None else self.business.name})"
