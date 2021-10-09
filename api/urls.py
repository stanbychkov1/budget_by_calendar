from django.urls import path

from . import views

urlpatterns = [
    path('payments/', views.CreateCrudPaymentView.as_view(),
         name='ajax_crud_create'),
    path('accruals/delete/<int:pk>/', views.DeleteCrudView.as_view(),
         name='ajax_crud_delete'),
    path('methods/', views.MethodView.as_view(),
         name='methods'),
]