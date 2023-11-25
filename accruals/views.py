import django_filters.views
import requests
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from urllib3.exceptions import NewConnectionError

from . import models, forms, caldav_services, filters, tasks


class IndexView(LoginRequiredMixin, generic.ListView):
    model = models.Accrual
    template_name = 'index.html'

    def get_queryset(self):
        task = tasks.upload_rates.delay()
        return self.request.user.accruals.order_by('-date')[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        accrual_amount = self.request.user.accruals.last()
        payment_amount = self.request.user.payments.last()
        payment_list = self.request.user.payments.order_by('-date')[:5]
        context.update({
            'payment_list': payment_list,
            'accrual_balance': accrual_amount,
            'payment_balance': payment_amount,
        })
        return context


class AccrualView(LoginRequiredMixin, generic.ListView):
    model = models.Accrual
    paginate_by = 20
    template_name = 'accruals.html'

    def get_queryset(self):
        queryset = self.request.user.accruals.order_by('-date')
        return queryset


class CalendarDateFormView(LoginRequiredMixin, generic.FormView):
    form_class = forms.CalendarDateForm
    template_name = 'calendar_date.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        user_id = self.request.user.id
        errors = caldav_services.uploading_calendar_data(start_date,
                                                         end_date,
                                                         user_id)
        if len(errors) != 0:
            return render(self.request, 'misc/loading_errors.html',
                          context={'errors': errors})
        return super().form_valid(form)


class AjaxPaymentView(LoginRequiredMixin, django_filters.views.FilterView):
    model = models.Accrual
    template_name = 'ajax_payment.html'
    filterset_class = filters.AccrualFilter

    def get_queryset(self):
        unpaid_accruals = self.request.user.accruals.filter(paid=False)
        return unpaid_accruals

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AjaxPaymentView, self).get_context_data()
        methods = self.request.user.methods.all()
        currencies = models.Currency.objects.order_by('-priority')
        context.update(
            {
                'methods': methods,
                'currencies': currencies,
            }
        )
        return context


class ChartsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'charts.html'


class PatientsSummaryView(LoginRequiredMixin, django_filters.views.FilterView):
    model = models.Accrual
    template_name = 'patient_summarty.html'
    filterset_class = filters.AccrualFilter

    def get_queryset(self):
        queryset = self.request.user.accruals.prefetch_related('payment')
        return queryset
