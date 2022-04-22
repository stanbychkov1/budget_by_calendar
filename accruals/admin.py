from django.contrib import admin

from . import models


class AccrualAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'uuid', 'patient',
                    'payment', 'amount', 'currency', 'amount_USD', 'date',)
    search_fields = ('pk', 'user__username', 'uuid',
                     'patient__name', 'payment__method__name',
                     'amount', 'currency__title', 'date',)
    empty_value_display = '-empty-'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'method', 'patient', 'amount', 'currency',
                    'amount_USD', 'date',)
    search_fields = ('pk', 'user__username', 'method__name',
                     'patient__name', 'amount', 'currency__title', 'date',)
    empty_value_display = '-empty-'


class MethodAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name',)
    search_fields = ('pk', 'user__username', 'name',)
    empty_value_display = '-empty-'


class PatientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name',)
    search_fields = ('pk', 'user__username', 'name',)
    empty_value_display = '-empty-'


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'priority', 'iso_code', 'iso_title',)
    search_fields = ('pk', 'title', 'priority', 'iso_code', 'iso_title',)
    empty_value_display = '-empty-'


class RateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'currency', 'rate', 'nominal', 'date',)
    search_fields = ('pk', 'currency__title', 'rate', 'nominal', 'date',)
    empty_value_display = '-empty-'


admin.site.register(models.Accrual, AccrualAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Method, MethodAdmin)
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Rate, RateAdmin)
