import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
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
        date = datetime.date.today()-relativedelta(months=5)
        while date <= datetime.date.today():
            amount = request.user.accruals.filter(
                date__month=date.month).filter(
                date__year=date.year).aggregate(
                Sum('amount_USD'))
            if amount['amount_USD__sum']:
                dict_data[_MONTHS[date.month]] = int(amount['amount_USD__sum'])
            else:
                dict_data[_MONTHS[date.month]] = 0
            date += relativedelta(months=1)
        return Response(data={
                                'success': True,
                                'dictionary': dict_data
                            })
