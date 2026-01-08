# apps/finance/urls.py
from django.urls import path

from .views import (
    InvoiceCreateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
    InvoiceUpdateView,
    ReceiptCreateView,
    ReceiptUpdateView,
    bulk_invoice,
    
    
    
    CanteenInvoiceListView,
    CanteenInvoiceCreateView,
    CanteenInvoiceDetailView,
    CanteenInvoiceUpdateView,
    CanteenInvoiceDeleteView,
    CanteenPaymentCreateView,
)

urlpatterns = [
    path("list/", InvoiceListView.as_view(), name="invoice-list"),
    path("create/", InvoiceCreateView.as_view(), name="invoice-create"),
    path("<int:pk>/detail/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("<int:pk>/update/", InvoiceUpdateView.as_view(), name="invoice-update"),
    path("<int:pk>/delete/", InvoiceDeleteView.as_view(), name="invoice-delete"),
    path("receipt/create", ReceiptCreateView.as_view(), name="receipt-create"),
    path(
        "receipt/<int:pk>/update/", ReceiptUpdateView.as_view(), name="receipt-update"
    ),
    path("bulk-invoice/", bulk_invoice, name="bulk-invoice"),
    
    
    
    
    
    path("canteen/", CanteenInvoiceListView.as_view(), name="canteen-invoice-list"),
    path("canteen/create/", CanteenInvoiceCreateView.as_view(), name="canteen-invoice-create"),
    path("canteen/<int:pk>/detail/", CanteenInvoiceDetailView.as_view(), name="canteen-invoice-detail"),
    path("canteen/<int:pk>/update/", CanteenInvoiceUpdateView.as_view(), name="canteen-invoice-update"),
    path("canteen/<int:pk>/delete/", CanteenInvoiceDeleteView.as_view(), name="canteen-invoice-delete"),
    path("canteen/payment/create/", CanteenPaymentCreateView.as_view(), name="canteen-payment-create"),

]
