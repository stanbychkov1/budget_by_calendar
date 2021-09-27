import django_filters

from . import models


class AccrualFilter(django_filters.FilterSet):
    class Meta:
        model = models.Accrual
        fields = ('patient',)
