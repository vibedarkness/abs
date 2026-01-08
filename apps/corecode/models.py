# apps/corecode/models.py
from django.db import models

# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Academic Term"""

    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    coefficient = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Coef {self.coefficient})"

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name

class AcademicMonth(models.Model):
    name = models.CharField(max_length=50)  # Octobre, Novembre…
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name