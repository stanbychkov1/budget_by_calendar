import datetime

import django_filters.views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms, caldav_services, filters


class IndexView(LoginRequiredMixin, generic.ListView):
    model = models.Accrual
    template_name = 'index.html'

    def get_queryset(self):
        return models.Accrual.objects.filter(
            user=self.request.user.id).order_by('-date')[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        accrual_amount = models.Accrual.objects.filter(
            user=self.request.user.id).last()
        payment_amount = models.Payment.objects.filter(
            user=self.request.user.id).last()
        context.update({
            'payment_list': models.Payment.objects.filter(
                user=self.request.user.id).order_by('-date')[:5],
            'accrual_balance': accrual_amount,
            'payment_balance': payment_amount,
        })
        return context


class CalendarDateFormView(LoginRequiredMixin, generic.FormView):
    form_class = forms.CalendarDateForm
    template_name = 'calendar_date.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        user_id = self.request.user.id
        caldav_services.uploading_calendar_data(start_date, end_date, user_id)
        return super().form_valid(form)


class AjaxPaymentView(LoginRequiredMixin, django_filters.views.FilterView):
    model = models.Accrual
    template_name = 'ajax_payment.html'
    filterset_class = filters.AccrualFilter

    def get_queryset(self):
        user = self.request.user
        unpaid_accruals = models.Accrual.objects.filter(
            user=user.id,
            paid=False
        )
        return unpaid_accruals

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AjaxPaymentView, self).get_context_data()
        user = self.request.user
        methods = models.Method.objects.filter(user=user)
        context.update(
            {
                'methods': methods,
            }
        )
        return context


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


class ChartsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'charts.html'
