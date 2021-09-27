from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('payment/', views.AjaxPaymentView.as_view(),
         name='ajax_payment'),
    path('calendar_date/', views.CalendarDateFormView.as_view(),
         name='calendar_date'),
    path('ajax/crud/create/', views.CreateCrudPaymentView.as_view(),
         name='ajax_crud_create'),
    path('charts/', views.ChartsView.as_view(),
         name='charts')
]
