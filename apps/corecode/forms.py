from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
    AcademicMonth,
)

# Formset pour la configuration du site
SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=("key", "value"),
    extra=0,
)

# ---------------- Sessions et Terms ----------------
class AcademicSessionForm(ModelForm):
    class Meta:
        model = AcademicSession
        fields = ["name", "current"]


class AcademicTermForm(ModelForm):
    class Meta:
        model = AcademicTerm
        fields = ["name", "current"]


# ---------------- Matières et Classes ----------------
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "coefficient"]  # coefficient ajouté


class StudentClassForm(ModelForm):
    class Meta:
        model = StudentClass
        fields = ["name"]


# ---------------- Mois et sélection actuelle ----------------
class AcademicMonthForm(ModelForm):
    class Meta:
        model = AcademicMonth
        fields = ["name", "order"]


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session',
    )
    current_term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.all(),
        help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term',
    )
    current_month = forms.ModelChoiceField(
        queryset=AcademicMonth.objects.all(),
        required=False,
        help_text='Optionnel: sélectionner le mois pour les bulletins mensuels'
    )
