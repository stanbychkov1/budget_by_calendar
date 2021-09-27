from django.contrib import admin

from . import models


# class AccrualAdmin(admin.ModelAdmin):
#     list_display = '__all__'
#     search_fields = '__all__'
#     empty_value_display = '-empty-'
#
#
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = '__all__'
#     search_fields = '__all__'
#     empty_value_display = '-empty-'
#
#
# class MethodAdmin(admin.ModelAdmin):
#     list_display = '__all__'
#     search_fields = '__all__'
#     empty_value_display = '-empty-'


admin.site.register(models.Accrual)
admin.site.register(models.Payment)
admin.site.register(models.Method)
admin.site.register(models.Patient)
