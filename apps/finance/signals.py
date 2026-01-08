
# apps/finance/signals.py
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import CanteenPayment
from .models import Invoice


@receiver(post_save, sender=Invoice)
def after_creating_invoice(sender, instance, created, **kwargs):
    if created:
        previous_inv = (
            Invoice.objects.filter(student=instance.student)
            .exclude(id=instance.id)
            .last()
        )
        if previous_inv:
            previous_inv.status = "closed"
            previous_inv.save()
            instance.balance_from_previous_term = previous_inv.balance()
            instance.save()



@receiver(post_save, sender=CanteenPayment)
@receiver(post_delete, sender=CanteenPayment)
def update_canteen_invoice_status(sender, instance, **kwargs):
    invoice = instance.invoice
    invoice.update_status()