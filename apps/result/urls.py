# apps/result/urls.py
from django.urls import path
from .views import (
    create_monthly_results,
    edit_monthly_results,
    edit_term_results,
    MonthlyResultsListView,
    TermResultsListView,
    AnnualResultsListView,
    create_term_results,
    TermBulletinFilterView,
)

from .pdf import monthly_bulletin_pdf, term_bulletin_pdf

urlpatterns = [
    path("monthly/create/", create_monthly_results, name="create-monthly-results"),
    path("monthly/edit/", edit_monthly_results, name="edit-monthly-results"),
    path("term/edit/", edit_term_results, name="edit-term-results"),
    path("monthly/view/all/", MonthlyResultsListView.as_view(), name="view-monthly-results"),
    path("term/view/all/", TermResultsListView.as_view(), name="view-term-results"),
    path("annual/view/all/", AnnualResultsListView.as_view(), name="view-annual-results"),
    path("pdf/monthly/<int:student_id>/", monthly_bulletin_pdf, name="monthly-bulletin-pdf"),
    path("pdf/term/<int:student_id>/", term_bulletin_pdf, name="term-bulletin-pdf"),
    path(
    "term/create/",
    create_term_results,
    name="create-term-results"
),
    
        path(
        "term/bulletin/",
        TermBulletinFilterView.as_view(),
        name="term-bulletin-filter"
    ),
]
