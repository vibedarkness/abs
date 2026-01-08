from django.forms import inlineformset_factory, modelformset_factory

from .models import CanteenInvoice, CanteenPayment
from .models import Invoice, InvoiceItem, Receipt

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=["description", "amount"], extra=1, can_delete=True
)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice,
    Receipt,
    fields=("amount_paid", "date_paid", "comment"),
    extra=0,
    can_delete=True,
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)






CanteenPaymentFormSet = inlineformset_factory(
    CanteenInvoice,
    CanteenPayment,
    fields=("amount_paid", "date_paid", "comment"),
    extra=0,
    can_delete=True,
)

CanteenInvoices = modelformset_factory(
    CanteenInvoice, exclude=(), extra=4
)
