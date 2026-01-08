from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import MonthlyResult, TermResult
from apps.students.models import Student
from apps.corecode.models import AcademicSession, AcademicMonth, AcademicTerm
from django.conf import settings
import os

def get_grade(note):
    if note >= 16:
        return "Très Bien"
    elif note >= 14:
        return "Bien"
    elif note >= 12:
        return "Assez Bien"
    elif note >= 10:
        return "Passable"
    else:
        return "Insuffisant"

def render_to_pdf(template_src, context):
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(
        get_template(template_src).render(context),
        dest=response
    )
    return response

def term_bulletin_pdf(request, student_id):
    session_id = request.GET.get("session")
    term_id = request.GET.get("term")

    # Validation des paramètres
    if not session_id:
        return HttpResponse("Paramètre manquant : session est requis", status=400)
    if not term_id:
        return HttpResponse("Paramètre manquant : semestre est requis", status=400)

    try:
        student = Student.objects.get(id=student_id)
        session = AcademicSession.objects.get(id=session_id)
        term = AcademicTerm.objects.get(id=term_id)
    except Student.DoesNotExist:
        return HttpResponse("Élève introuvable", status=404)
    except AcademicSession.DoesNotExist:
        return HttpResponse("Session académique introuvable", status=404)
    except AcademicTerm.DoesNotExist:
        return HttpResponse("Semestre introuvable", status=404)
    except ValueError:
        return HttpResponse("ID invalide", status=400)

    # Récupération des résultats du semestre
    results = TermResult.objects.filter(
        student=student,
        session=session,
        term=term
    ).select_related("subject")

    total_general = 0
    total_coef = 0

    # Calculs pour chaque matière
    for r in results:
        # moyenne par matière
        avg = r.average() if callable(r.average) else r.average

        # total pondéré
        r.weighted_average = round(avg * r.subject.coefficient, 2)

        # grade
        r.grade = get_grade(avg)

        total_general += r.weighted_average
        total_coef += r.subject.coefficient

    # Moyenne semestrielle
    average = round(total_general / total_coef, 2) if total_coef > 0 else 0

    context = {
        "student": student,
        "session": session,
        "term": term,
        "results": results,
        "average": average,
        "mention": get_grade(average),
        "school_name": "LYCÉE MODERNE DE DAKAR",
        "logo_right": os.path.join(settings.BASE_DIR, 'static/images/logo_gauche.png'),
        "logo_left": os.path.join(settings.BASE_DIR, 'static/images/logo_droite.jpeg'),
    }

    return render_to_pdf("result/pdf/term_bulletin.html", context)

def render_to_pdf(template_src, context):
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(
        get_template(template_src).render(context),
        dest=response
    )
    return response


def monthly_bulletin_pdf(request, student_id):
    session_id = request.GET.get("session")
    month_id = request.GET.get("month")


    # Validation des paramètres
    if not session_id:
        return HttpResponse("Paramètre manquant : session est requis", status=400)
    
    if not month_id:
        return HttpResponse("Paramètre manquant : mois est requis", status=400)

    try:
        student = Student.objects.get(id=student_id)
        session = AcademicSession.objects.get(id=session_id)
        month = AcademicMonth.objects.get(id=month_id)
    except Student.DoesNotExist:
        return HttpResponse("Élève introuvable", status=404)
    except AcademicSession.DoesNotExist:
        return HttpResponse("Session académique introuvable", status=404)
    except AcademicMonth.DoesNotExist:
        return HttpResponse("Mois académique introuvable", status=404)
    except ValueError:
        return HttpResponse("ID invalide : le mois doit être un nombre", status=400)

    results = MonthlyResult.objects.filter(
        student=student,
        session=session,
        month=month
    ).select_related("subject")

    total = 0
    coef = 0
    for r in results:
        total += r.weighted_average()
        coef += r.subject.coefficient

    average = round(total / coef, 2) if coef > 0 else 0
    
    
    total_general = 0
    total_coef = 0

    for r in results:
        # Récupère la moyenne comme float
        avg = r.average() if callable(r.average) else r.average

        # Calcule le total pour chaque matière arrondi à 2 décimales
        r.total = round(avg * r.subject.coefficient, 2)

        # Détermine le grade
        r.grade = get_grade(avg)

        # Ajoute au total général et au total des coefficients
        total_general += r.total
        total_coef += r.subject.coefficient

    # Arrondir le total général à 2 décimales
    total_general = round(total_general, 2)

    # Calcule la moyenne générale arrondie à 2 décimales
    average = round(total_general / total_coef, 2) if total_coef > 0 else 0


    context = {
            "student": student,
            "session": session,
            "month": month,
            "results": results,
            "average": average,
            "total_general": total_general,
            "school_name": "LYCÉE MODERNE DE DAKAR",
            "logo_right": os.path.join(settings.BASE_DIR, 'static/images/logo_gauche.png'),
            "logo_left": os.path.join(settings.BASE_DIR, 'static/images/logo_droite.jpeg'),
        }

    return render_to_pdf("result/pdf/monthly_bulletin.html", context)