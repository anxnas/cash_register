from django.urls import path
from shop.views.cash_machine_view import CashMachineView
from shop.views.system_info_view import system_info

urlpatterns = [
    path('', system_info, name='system_info'),
    path('cash_machine/', CashMachineView.as_view(), name='cash_machine'),
]