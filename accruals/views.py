import django_filters.views
import requests
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms, caldav_services, filters, tasks


class IndexView(LoginRequiredMixin, generic.ListView):
    model = models.Accrual
    template_name = 'index.html'

    def get_queryset(self):
        task = tasks.upload_rates.delay()
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


class AccrualView(LoginRequiredMixin, generic.ListView):
    model = models.Accrual
    paginate_by = 20
    template_name = 'accruals.html'

    def get_queryset(self):
        queryset = models.Accrual.objects.filter(
            user=self.request.user.id
        ).order_by('-date')
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
            return render(self.request, 'loading_errors.html',
                          context={'errors': errors})
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
        ).order_by('date')
        return unpaid_accruals

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AjaxPaymentView, self).get_context_data()
        user = self.request.user
        methods = models.Method.objects.filter(user=user)
        currencies = models.Currency.objects.all().order_by('-priority')
        context.update(
            {
                'methods': methods,
                'currencies': currencies,
            }
        )
        # TODO: создать фильтр по клиентов, которые относятся только к
        #  пользователю, в данный момент выдает всех клиентов ото всех
        #  пользователей
        return context


class ChartsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'charts.html'
# TODO: создать класс для создания метода ajax.
#  добавить кнопку создания метода на форму создания оплаты.
#  создаты страницу с бар-чартами
