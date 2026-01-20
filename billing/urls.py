from django.urls import path
from . import views

urlpatterns = [
    # HOME / ABOUT
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # BILLING
    path('billing/', views.billing_list, name='billing_list'),
    path('billing/create/', views.create_bill, name='create_bill'),
    path('billing/summary/', views.billing_summary, name='billing_summary'),
    path('billing/print/<int:bill_id>/', views.print_bill, name='print_bill'),
    path('billing/pdf/<int:bill_id>/', views.bill_pdf, name='bill_pdf'),
    path('export_billing/', views.export_billing_csv, name='export_billing'),

    # DELETE BILL
    path('billing/delete-bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),

    # MASTER DATA – HOTEL
    path('billing/add_hotel/', views.add_hotel, name='add_hotel'),
    path('billing/update-hotel/<int:pk>/', views.update_hotel, name='update_hotel'),
    path('billing/delete-hotel/<int:pk>/', views.delete_hotel, name='delete_hotel'),

    # MASTER DATA – ITEM
    path('billing/add_item/', views.add_item, name='add_item'),
    path('billing/update-item/<int:pk>/', views.update_item, name='update_item'),
    path('billing/delete-item/<int:pk>/', views.delete_item, name='delete_item'),

    # MASTER DATA – HOTEL ITEM RATE
    path('billing/add_hotel_item_rate/', views.add_hotel_item_rate, name='add_hotel_item_rate'),
    path('billing/update-rate/<int:pk>/', views.update_hotel_item_rate, name='update_hotel_item_rate'),
    path('billing/delete-rate/<int:pk>/', views.delete_hotel_item_rate, name='delete_hotel_item_rate'),
]
