from django.urls import path
from . import views


app_name = "profiles"
urlpatterns = [
    path("authenticate", views.authenticate),
    path("sign-up", views.SignUp.as_view(), name="sign_up"),
    path("sign-in", views.SignIn.as_view(), name="sign_in"),
    path("homepage", views.homepage),
]
