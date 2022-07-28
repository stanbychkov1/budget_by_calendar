import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.views import generic
from dateutil.relativedelta import relativedelta
from rest_framework import generics

from accruals import models

from .serializers import PaymentSerializer

_MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'Ocotber',
    11: 'November',
    12: 'December'
}


class CreatePaymentView(LoginRequiredMixin, generics.CreateAPIView):
    model = models.Payment
    serializer_class = PaymentSerializer


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


class AccraulMonthlyView(LoginRequiredMixin, generic.View):
    def get(self, request):
        dict_data = {}
        date = datetime.date.today()-relativedelta(months=5)
        while date <= datetime.date.today():
            amount = request.user.accruals.filter(date__month=date.month).filter(date__year=date.year).aggregate(Sum('amount_USD'))
            dict_data[_MONTHS[date.month]] = amount
            date += relativedelta(months=1)
        return JsonResponse(status=200,
                            data={
                                'success': True,
                                'dictionary': dict_data
                            })



# class AccrualsPaymentApiView(LoginRequiredMixin, generic.View):
#     def get(self, request):
#         dict_data = {}
#         today_month = datetime.datetime.today().month
#         six_last_months = [x for ]
