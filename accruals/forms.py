from django import forms
from django.forms import formset_factory, modelformset_factory

from . import models, services


class CalendarDateForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)


# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = models.Payment
#         fields = ('date', 'patient', 'amount', 'method', 'info',)
#
#     def __init__(self, user, *args, **kwargs):
#         super(PaymentForm, self).__init__(*args, **kwargs)
#         self.fields['accruals'] = forms.ModelMultipleChoiceField(
#             required=False,
#             queryset=models.Accrual.objects.filter(
#                 paid=False,
#                 user=user)
#         )
#         self.fields['method'] = forms.ModelChoiceField(
#             required=True,
#             queryset=models.Method.objects.filter(user=user)
#         )
#         self.fields['patient'] = forms.ModelChoiceField(
#             required=True,
#             queryset=models.Patient.objects.filter(user=user)
#         )
#
#     def clean(self):
#         accruals = self.cleaned_data['accruals']
#         for accrual in accruals:
#             if accrual.patient.id is not self.cleaned_data['patient'].id:
#                 self.add_error('patient',
#                                f'Пациенты не совпадают в начислении'
#                                f' {accrual.id}')
#             elif accrual.paid is True:
#                 self.add_error('accruals',
#                                f'Начисление {accrual.id} уже оплачено')
#             elif accrual.amount != self.cleaned_data['amount']:
#                 self.add_error('amount',
#                                f'Сумма оплаты не ровняется сумме начисления'
#                                f' {accrual.id}')
#         return self.cleaned_data
#
#     def save(self, commit=True):
#         super().save()
#         accruals = self.cleaned_data['accruals']
#         services.add_payment_to_accrual(self.instance, accruals)
#         return self.instance





# class NewPaymentForm(forms.ModelForm):
#
#     class Meta:
#         model = models.Payment
#         fields = ('date', 'method', 'amount', 'patient', 'id')
#         widgets = {
#             'patient': forms.HiddenInput(),
#             'amount': forms.HiddenInput(),
#             'id': forms.HiddenInput(),
#         }
#
#     def __init__(self, user, *args, **kwargs):
#         super(NewPaymentForm, self).__init__(*args, **kwargs)
#         self.fields['method'] = forms.ModelChoiceField(
#             required=True,
#             queryset=models.Method.objects.filter(user=user)
#
#         )
#         self.fields['paid'] = forms.BooleanField(
#             widget=forms.CheckboxInput
#         )
#
#     def clean(self):
#         return super(NewPaymentForm, self).clean()
#
#     # def is_valid(self):
#
#
# NewPaymentFormset = modelformset_factory(models.Payment, form=NewPaymentForm)
