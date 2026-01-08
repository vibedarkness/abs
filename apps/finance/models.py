from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student


# ========================
# FACTURES SCOLAIRES
# ========================

class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    class_for = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    balance_from_previous_term = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

    class Meta:
        ordering = ["student", "term"]

    def __str__(self):
        return f"{self.student}"

    def balance(self):
        return self.total_amount_payable() - self.total_amount_paid()

    def amount_payable(self):
        return sum(item.amount for item in InvoiceItem.objects.filter(invoice=self))

    def total_amount_payable(self):
        return self.balance_from_previous_term + self.amount_payable()

    def total_amount_paid(self):
        return sum(
            receipt.amount_paid for receipt in Receipt.objects.filter(invoice=self)
        )

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()


class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Receipt on {self.date_paid}"


# ========================
# CANTINE
# ========================

class CanteenInvoice(models.Model):
    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    datecreation = models.DateField(default=timezone.now, blank=True, null=True)
    total_amount = models.IntegerField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="unpaid"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student"]
        unique_together = ("student", "session")

    def __str__(self):
        return f"Cantine - {self.student}"

    def total_paid(self):
        return sum(
            p.amount_paid for p in CanteenPayment.objects.filter(invoice=self)
        )

    def balance(self):
        return self.total_amount - self.total_paid()

    def update_status(self):
        paid = self.total_paid()
        if paid == 0:
            self.status = "unpaid"
        elif paid < self.total_amount:
            self.status = "partial"
        else:
            self.status = "paid"
        self.save()

    def get_absolute_url(self):
        return reverse("canteen-invoice-detail", kwargs={"pk": self.pk})


class CanteenPayment(models.Model):
    invoice = models.ForeignKey(CanteenInvoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Payment {self.amount_paid} - {self.date_paid}"
