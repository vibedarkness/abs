#result/models.py
from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from .utils import score_grade



class MonthlyResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    month = models.ForeignKey("corecode.AcademicMonth", on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    devoir_1 = models.FloatField(default=0)
    devoir_2 = models.FloatField(default=0)
    composition = models.FloatField(default=0)

    teacher_comment = models.TextField(blank=True)

    class Meta:
        unique_together = (
            "student",
            "session",
            "term",
            "month",
            "subject",
        )
        ordering = ["subject"]

    def average(self):
        return round((self.devoir_1 + self.devoir_2 + self.composition) / 3, 2)

    def weighted_average(self):
        return self.average() * self.subject.coefficient

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.month}"


# Create your models here.
class TermResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    devoir_1 = models.FloatField(default=0)
    devoir_2 = models.FloatField(default=0)
    composition = models.FloatField(default=0)

    teacher_comment = models.TextField(blank=True)

    class Meta:
        unique_together = (
            "student",
            "session",
            "term",
            "subject",
        )
        ordering = ["subject"]

    def average(self):
        return round((self.devoir_1 + self.devoir_2 + self.composition) / 3, 2)

    def weighted_average(self):
        return self.average() * self.subject.coefficient

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.term}"
class AnnualResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)

    final_average = models.FloatField(default=0)
    decision = models.CharField(
        max_length=20,
        choices=(
            ("PASS", "Passe"),
            ("REPEAT", "Redouble"),
        ),
    )

    class Meta:
        unique_together = ("student", "session")

    def mention(self):
        avg = self.final_average
        if avg < 8:
            return "Médiocre"
        elif avg < 10:
            return "Passable"
        elif avg < 12:
            return "Assez Bien"
        elif avg < 14:
            return "Bien"
        else:
            return "Très Bien"

    def __str__(self):
        return f"{self.student} - {self.session}"
