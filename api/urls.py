from django.urls import path

from . import views

urlpatterns = [
    path('payments/', views.CreatePaymentView.as_view(),
         name='ajax_crud_create'),
    path('accruals/delete/<int:pk>/', views.DeleteCrudView.as_view(),
         name='ajax_crud_delete'),
    path('methods/', views.MethodAPIView.as_view(),
         name='methods'),
    path('accruals_monthly/', views.AccraulMonthlyAPIView.as_view(),
         name='accruals_monthly_amount'),
]
