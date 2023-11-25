import datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth, Coalesce
from django.http import JsonResponse
from django.views import generic
from dateutil.relativedelta import relativedelta
from rest_framework import generics, views
from rest_framework.response import Response

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


class DeleteCrudView(LoginRequiredMixin, generics.DestroyAPIView):
    def get_queryset(self):
        queryset = self.request.user.accruals.all()
        return queryset

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return JsonResponse(status=204,
                            data={'success': True})


class MethodAPIView(LoginRequiredMixin, views.APIView):
    def get(self, request):
        dict_data = {}
        for method in request.user.methods.all():
            amount = method.payments.all().aggregate(Sum('amount_USD'))
            if amount['amount_USD__sum']:
                dict_data[method.name] = int(amount['amount_USD__sum'])
            else:
                dict_data[method.name] = 0
        return Response(data={
            'success': True,
            'dictionary': dict_data
        })


class AccraulMonthlyAPIView(LoginRequiredMixin, views.APIView):
    def get(self, request):
        dict_data = {}

        tdy = datetime.date.today()
        delta_date = tdy - relativedelta(months=5)

        currencies = (request.user.accruals
                      .filter(date__gte=datetime.date(
            delta_date.year, delta_date.month, 1))
                      .order_by('currency')
                      .values_list('currency', 'currency__title')
                      .distinct())

        for currency_id, currency_title in currencies:
            amount_list = []
            for delta in range(5, -1, -1):
                date = tdy - relativedelta(months=delta)
                amount = request.user.accruals.filter(
                    date__month=date.month,
                    date__year=date.year,
                    currency=currency_id
                ).aggregate(Sum('amount_USD'))
                if amount['amount_USD__sum']:
                    amount_list.append(amount['amount_USD__sum'])
                else:
                    amount_list.append(0)
            dict_data[currency_title] = amount_list
        return Response(data={
            'success': True,
            'dictionary': dict_data
        })
