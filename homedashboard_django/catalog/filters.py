import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.forms import TextInput
from django_filters import DateFilter, DateRangeFilter, CharFilter, ModelChoiceFilter
from .models import *


def categories(request):
    if request is None:
        return Category.objects.none()
    else:
        return


class ItemFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_entered', lookup_expr='gte', label="Start Date", widget=TextInput(attrs={'placeholder': 'MM/DD/YY format', 'type': 'date'}))
    end_date = DateFilter(field_name='date_entered', lookup_expr='lte', label="End Date", widget=TextInput(attrs={'placeholder': 'MM/DD/YY format', 'type': 'date'}))
    item_name = CharFilter(field_name='item_name', label="Item", lookup_expr='icontains')
    item_description = CharFilter(field_name='item_description', label="Description", lookup_expr='icontains' )
    item_category = ModelChoiceFilter(field_name='item_category', label="Category", queryset=Category.objects.all())
    condition = ModelChoiceFilter(field_name='condition', label="Condition", queryset=Condition.objects.all())
    room = ModelChoiceFilter(field_name='room', label="Room", queryset=Room.objects.all())
    value_start = CharFilter(field_name='value', label="Value Start Range")
    value_end = CharFilter(field_name='value', label="Value End Range")


    class Meta:
        model = Item
        fields = '__all__'
        # fields = {
        #     'item_name': ['icontains'],
        #     'item_description': ['icontains'],
        #     'item_category': ['icontains'],
        #     'condition': 'condition',
        #     'room': "room",
        #     'value': 'value'
        #
        # }
        exclude = ['date_entered','id']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('item_name', css_class='form-group col-md-6 mb-0'),
    #             Column('item_description', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('item_category', css_class='form-group col-md-4 mb-0'),
    #             Column('condition', css_class='form-group col-md-4 mb-0'),
    #             Column('room', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('start_date', css_class='form-group col-md-4 mb-0'),
    #             Column('end_date', css_class='form-group col-md-4 mb-0'),
    #             Column('value', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #     )
