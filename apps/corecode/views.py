from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentClassForm,
    SubjectForm,
    AcademicMonthForm
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
    AcademicMonth
    
)

from django.db.models import Count, Q, Sum
from apps.students.models import Student
from apps.staffs.models import Staff
from apps.finance.models import CanteenInvoice



# ---------------- Index ----------------
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques des étudiants
        total_students = Student.objects.count()
        total_boys = Student.objects.filter(gender='male').count()
        total_girls = Student.objects.filter(gender='female').count()
        
        # Statistiques du staff
        total_staff = Staff.objects.count()
        staff_men = Staff.objects.filter(gender='male').count()
        staff_women = Staff.objects.filter(gender='female').count()
        
        # Statistiques de la cantine
        canteen_invoices = CanteenInvoice.objects.all()
        total_canteen_subscribers = canteen_invoices.count()
        
        # Statistiques de paiement cantine
        paid_canteen = canteen_invoices.filter(status='paid').count()
        partial_canteen = canteen_invoices.filter(status='partial').count()
        unpaid_canteen = canteen_invoices.filter(status='unpaid').count()
        
        # Pourcentage d'abonnés cantine
        canteen_percentage = (total_canteen_subscribers / total_students * 100) if total_students > 0 else 0
        
        # Statistiques par classe (pour graphique)
        students_by_class = Student.objects.values(
            'current_class__name'
        ).annotate(
            count=Count('id')
        ).order_by('current_class__name')
        
        # Données pour graphique de répartition par genre
        gender_distribution = [
            {'gender': 'Garçons', 'count': total_boys},
            {'gender': 'Filles', 'count': total_girls},
        ]
        
        # Staff par genre
        staff_gender_distribution = [
            {'gender': 'Hommes', 'count': staff_men},
            {'gender': 'Femmes', 'count': staff_women},
        ]
        
        # Statut de paiement cantine
        canteen_status_distribution = [
            {'status': 'Payé', 'count': paid_canteen, 'color': '#10B981'},
            {'status': 'Partiel', 'count': partial_canteen, 'color': '#F59E0B'},
            {'status': 'Impayé', 'count': unpaid_canteen, 'color': '#EF4444'},
        ]
        
        context.update({
            # Totaux
            'total_students': total_students,
            'total_boys': total_boys,
            'total_girls': total_girls,
            'total_staff': total_staff,
            'staff_men': staff_men,
            'staff_women': staff_women,
            'total_canteen_subscribers': total_canteen_subscribers,
            'canteen_percentage': round(canteen_percentage, 1),
            
            # Distributions
            'students_by_class': list(students_by_class),
            'gender_distribution': gender_distribution,
            'staff_gender_distribution': staff_gender_distribution,
            'canteen_status_distribution': canteen_status_distribution,
            
            # Statistiques de paiement
            'paid_canteen': paid_canteen,
            'partial_canteen': partial_canteen,
            'unpaid_canteen': unpaid_canteen,
        })
        
        return context


# ---------------- Site Config ----------------
class SiteConfigView(LoginRequiredMixin, View):
    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        return render(request, self.template_name, {"formset": formset})

    def post(self, request):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        return render(request, self.template_name, {"formset": formset, "title": "Configuration"})


# ---------------- Session & Term ----------------
class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current Session, Term and Month"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.filter(current=True).first(),
                "current_term": AcademicTerm.objects.filter(current=True).first(),
                "current_month": AcademicMonth.objects.first()
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            month = form.cleaned_data.get("current_month")

            AcademicSession.objects.update(current=False)
            AcademicTerm.objects.update(current=False)

            AcademicSession.objects.filter(pk=session.pk).update(current=True)
            AcademicTerm.objects.filter(pk=term.pk).update(current=True)

            messages.success(request, "Current session, term and month updated")
            return redirect("current-session")

        return render(request, self.template_name, {"form": form})


# ---------------- CRUD Classes, Subjects, Months ----------------
class ClassListView(LoginRequiredMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"
    context_object_name = "classes"
    extra_context = {"form": StudentClassForm()}


class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"
    context_object_name = "subjects"
    extra_context = {"form": SubjectForm()}


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"


class AcademicMonthListView(LoginRequiredMixin, ListView):
    model = AcademicMonth
    template_name = "corecode/month_list.html"
    context_object_name = "months"
    extra_context = {"form": AcademicMonthForm()}


class AcademicMonthCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicMonth
    form_class = AcademicMonthForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("months")
    success_message = "New month successfully added"



# ---------------- Classes ----------------
class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "Class successfully updated"


class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("classes")
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)


# ---------------- Subjects ----------------
class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated"


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("subjects")
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)


# ---------------- Months ----------------
class AcademicMonthUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicMonth
    form_class = AcademicMonthForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("months")
    success_message = "Month successfully updated"


class AcademicMonthDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicMonth
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("months")
    success_message = "The month {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)


# ---------------- Sessions ----------------
class SessionListView(LoginRequiredMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"
    context_object_name = "sessions"
    extra_context = {"form": AcademicSessionForm()}


class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated"


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("sessions")
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)


# ---------------- Terms ----------------
class TermListView(LoginRequiredMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"
    context_object_name = "terms"
    extra_context = {"form": AcademicTermForm()}


class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"


class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated"


class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("terms")
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)
