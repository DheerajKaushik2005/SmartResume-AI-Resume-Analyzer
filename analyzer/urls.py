from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("result/<int:analysis_id>/", views.result, name="result"),
    path("history/", views.history, name="history"),
    path("history/<int:analysis_id>/delete/", views.delete_history, name="delete_history"),
]
