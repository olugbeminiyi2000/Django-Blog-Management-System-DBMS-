from django.urls import path
from . import views


urlpatterns = [
    path("first", views.TranslateView.as_view()),
    path("testcookie", views.testcookie),
    path("sessfun", views.sessfun),
]
