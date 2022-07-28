from django.forms import SelectDateWidget
from django import forms
from django_filters import filters, FilterSet
from django_filters.widgets import DateRangeWidget, RangeWidget

from . import models


def user_patients(request):
    if request is None:
        return models.Patient.objects.none()
    return request.user.patients.all()


class NewRangeWidget(DateRangeWidget):
    def __init__(self, attrs=None):
        widgets = (forms.SelectDateWidget, forms.SelectDateWidget,)
        super(RangeWidget, self).__init__(widgets, attrs)


class AccrualFilter(FilterSet):
    patient = filters.ModelChoiceFilter(queryset=user_patients)
    date = filters.DateFromToRangeFilter(
        # widget=NewRangeWidget
    )
