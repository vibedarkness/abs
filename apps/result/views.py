# apps/result/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View

from apps.students.models import Student
from .forms import (
    CreateMonthlyResultsForm,
    EditMonthlyResultsFormSet,
    EditTermResultsFormSet
)
from .models import MonthlyResult, TermResult, AnnualResult
from apps.students.models import Student
from apps.corecode.models import StudentClass, AcademicMonth, AcademicSession
from .models import MonthlyResult
from .forms import CreateMonthlyResultsForm, EditMonthlyResultsFormSet, EditTermResultsFormSet,CreateTermResultsForm
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student



@login_required
def create_monthly_results(request):
    students = Student.objects.all()
    if request.method == "POST":
        form = CreateMonthlyResultsForm(request.POST)
        if form.is_valid():
            session = form.cleaned_data["session"]
            term = form.cleaned_data["term"]
            month = form.cleaned_data["month"]
            subjects = form.cleaned_data["subjects"]
            selected_students = request.POST.getlist("students")

            if not selected_students:
                messages.warning(request, "Vous devez sélectionner au moins un élève.")
            else:
                results_to_create = []
                for student_id in selected_students:
                    stu = Student.objects.get(pk=student_id)
                    for subject in subjects:
                        # Vérifie si le résultat existe déjà
                        existing = MonthlyResult.objects.filter(
                            student=stu,
                            session=session,
                            term=term,
                            month=month,
                            subject=subject
                        ).first()
                        if not existing:
                            results_to_create.append(MonthlyResult(
                                student=stu,
                                session=session,
                                term=term,
                                month=month,
                                current_class=stu.current_class,
                                subject=subject
                            ))

                if results_to_create:
                    MonthlyResult.objects.bulk_create(results_to_create)
                    messages.success(request, "Résultats mensuels créés avec succès")
                else:
                    messages.info(request, "Tous les résultats sélectionnés existent déjà.")

                return redirect("edit-monthly-results")

    else:
        form = CreateMonthlyResultsForm()

    return render(request, "result/create_monthly_results.html", {
        "students": students,
        "form": form
    })


@login_required
def edit_monthly_results(request):
    if request.method == "POST":
        formset = EditMonthlyResultsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Résultats mensuels mis à jour avec succès")
            return redirect("edit-monthly-results")
    else:
        results = MonthlyResult.objects.filter(
            session=request.current_session,
            term=request.current_term
        )
        formset = EditMonthlyResultsFormSet(queryset=results)

    return render(request, "result/edit_monthly_results.html", {
        "formset": formset
    })


@login_required
def edit_term_results(request):
    if request.method == "POST":
        formset = EditTermResultsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Résultats semestriels mis à jour avec succès")
            return redirect("edit-term-results")
    else:
        results = TermResult.objects.filter(
            session=request.current_session,
            term=request.current_term
        )
        formset = EditTermResultsFormSet(queryset=results)

    return render(request, "result/edit_term_results.html", {
        "formset": formset
    })


# ---------------- Bulletin Mensuel ----------------
class MonthlyResultsListView(View):
    def get(self, request):
        # Récupération des filtres
        class_id = request.GET.get("class")
        month_id = request.GET.get("month")
        session_id = request.GET.get("session")

        students = Student.objects.all()

        # Filtre par classe
        if class_id:
            students = students.filter(current_class_id=class_id)

        # Filtre par année académique (session)
        if session_id:
            students = students.filter(
                monthlyresult__session_id=session_id
            ).distinct()

        context = {
            "students": students,
            "classes": StudentClass.objects.all(),
            "months": AcademicMonth.objects.all(),
            "sessions": AcademicSession.objects.all(),
            "selected_class": class_id,
            "selected_month": month_id,
            "selected_session": session_id,
        }

        return render(request, "result/monthly_results_list.html", context)

# ---------------- Bulletin Semestriel ----------------
class TermResultsListView(View):
    def get(self, request, *args, **kwargs):
        results = TermResult.objects.filter(
            session=request.current_session,
            term=request.current_term
        ).order_by("student", "subject")

        bulk = {}
        for r in results:
            if r.student.id not in bulk:
                bulk[r.student.id] = {
                    "student": r.student,
                    "subjects": [],
                    "total_weighted": 0,
                    "total_coef": 0
                }
            bulk[r.student.id]["subjects"].append(r)
            bulk[r.student.id]["total_weighted"] += r.weighted_average()
            bulk[r.student.id]["total_coef"] += r.subject.coefficient

        # Calcul moyenne générale
        for student_id, data in bulk.items():
            data["average"] = round(
                data["total_weighted"] / data["total_coef"], 2
            ) if data["total_coef"] > 0 else 0

        return render(request, "result/term_results_list.html", {
            "results": bulk
        })


# ---------------- Bulletin Annuel ----------------
class AnnualResultsListView(View):
    def get(self, request, *args, **kwargs):
        results = AnnualResult.objects.filter(
            session=request.current_session
        ).order_by("student")

        return render(request, "result/annual_results_list.html", {
            "results": results
        })



@login_required
def create_term_results(request):
    students = Student.objects.all()

    if request.method == "POST":
        form = CreateTermResultsForm(request.POST)

        if form.is_valid():
            session = form.cleaned_data["session"]
            term = form.cleaned_data["term"]
            subjects = form.cleaned_data["subjects"]
            selected_students = request.POST.getlist("students")

            if not selected_students:
                messages.warning(
                    request, "Veuillez sélectionner au moins un élève."
                )
            else:
                results_to_create = []

                for student_id in selected_students:
                    student = Student.objects.get(pk=student_id)

                    for subject in subjects:
                        exists = TermResult.objects.filter(
                            student=student,
                            session=session,
                            term=term,
                            subject=subject
                        ).exists()

                        if not exists:
                            results_to_create.append(
                                TermResult(
                                    student=student,
                                    session=session,
                                    term=term,
                                    current_class=student.current_class,
                                    subject=subject
                                )
                            )

                if results_to_create:
                    TermResult.objects.bulk_create(results_to_create)
                    messages.success(
                        request, "Résultats semestriels créés avec succès."
                    )
                else:
                    messages.info(
                        request, "Tous les résultats existent déjà."
                    )

                return redirect("edit-term-results")

    else:
        form = CreateTermResultsForm()

    return render(
        request,
        "result/create_term_results.html",
        {
            "form": form,
            "students": students,
        }
    )


class TermBulletinFilterView(View):
    def get(self, request):
        session_id = request.GET.get("session")
        term_id = request.GET.get("term")
        class_id = request.GET.get("class")

        students = Student.objects.all()

        if class_id:
            students = students.filter(current_class_id=class_id)

        if session_id:
            students = students.filter(
                termresult__session_id=session_id
            ).distinct()

        if term_id:
            students = students.filter(
                termresult__term_id=term_id
            ).distinct()

        context = {
            "students": students,
            "sessions": AcademicSession.objects.all(),
            "terms": AcademicTerm.objects.all(),
            "classes": StudentClass.objects.all(),
            "selected_session": session_id,
            "selected_term": term_id,
            "selected_class": class_id,
        }

        return render(request, "result/term_bulletin_filter.html", context)