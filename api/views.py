from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.views import generic

from accruals import models


class CreateCrudPaymentView(LoginRequiredMixin, generic.View):
    def get(self, request):
        user = self.request.user
        accrual_id = request.GET.get('id', None)
        accrual = models.Accrual.objects.get(id=accrual_id)
        if accrual.paid:
            return JsonResponse(status=201,
                                data={'success': True})
        patient_id = request.GET.get('patient_id', None)
        amount = request.GET.get('amount', None)
        date = request.GET.get('date', None)
        method = request.GET.get('method', None)
        if len(method) == 0 or method is None:
            return JsonResponse(status=500,
                                data={'success': False})
        if patient_id is None or len(patient_id) == 0:
            patient_id = accrual.patient_id
        if amount is None or len(amount) == 0:
            amount = accrual.amount
        if date is None or len(date) == 0:
            date = accrual.date
        obj = models.Payment.objects.create(
            user=user,
            amount=amount,
            method_id=method,
            date=date,
            patient_id=patient_id
        )
        accrual.paid = True
        accrual.payment_id = obj.id
        accrual.save()
        return JsonResponse(status=201,
                            data={'success': True})


class DeleteCrudView(LoginRequiredMixin, generic.DeleteView):
    def get_queryset(self):
        queryset = models.Accrual.objects.filter(user=self.request.user.id)
        return queryset

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return JsonResponse(status=204,
                            data={'success': True})


class MethodView(LoginRequiredMixin, generic.View):
    def get(self, request):
        dict_data = {}
        for method in models.Method.objects.filter(user=request.user.id):
            amount = method.payments.all().aggregate(Sum('amount'))
            dict_data[method.name] = amount
        return JsonResponse(status=200,
                            data={
                                'success': True,
                                'dictionary': dict_data
                            })
