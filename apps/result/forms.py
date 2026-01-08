# apps/result/forms.py
from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicTerm, Subject, AcademicMonth
from apps.students.models import Student
from .models import MonthlyResult, TermResult


class CreateMonthlyResultsForm(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    month = forms.ModelChoiceField(queryset=AcademicMonth.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class EditMonthlyResultForm(forms.ModelForm):
    class Meta:
        model = MonthlyResult
        fields = ["devoir_1", "devoir_2", "composition", "teacher_comment"]


EditMonthlyResultsFormSet = modelformset_factory(
    MonthlyResult,
    form=EditMonthlyResultForm,
    extra=0,
    can_delete=False
)


class EditTermResultForm(forms.ModelForm):
    class Meta:
        model = TermResult
        fields = ["devoir_1", "devoir_2", "composition", "teacher_comment"]


EditTermResultsFormSet = modelformset_factory(
    TermResult,
    form=EditTermResultForm,
    extra=0,
    can_delete=False
)


class CreateTermResultsForm(forms.Form):
    session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        label="Année académique"
    )
    term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.all(),
        label="Semestre"
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Matières"
    )
