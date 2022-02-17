from django.contrib import admin

from . import models


class AccrualAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'uuid', 'patient',
                    'payment', 'amount', 'date',)
    search_fields = ('pk', 'user__username', 'uuid',
                     'patient__name', 'payment__method__name',
                     'amount', 'date',)
    empty_value_display = '-empty-'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'method', 'patient', 'amount', 'date',)
    search_fields = ('pk', 'user__username', 'method__name',
                     'patient__name', 'amount', 'date',)
    empty_value_display = '-empty-'


class MethodAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name',)
    search_fields = ('pk', 'user__username', 'name',)
    empty_value_display = '-empty-'


class PatientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name',)
    search_fields = ('pk', 'user__username', 'name',)
    empty_value_display = '-empty-'


admin.site.register(models.Accrual, AccrualAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Method, MethodAdmin)
admin.site.register(models.Patient, PatientAdmin)
