from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import Profiles


# Create your views here.
def authenticate(request):
    return render(request, "profiles/sign_up.html")


def homepage(request):
    curr_user = request.session.get("curr_user", None)
    if curr_user is None:
        return render(request, "profiles/sign_in.html")
    expired = request.COOKIES.get("dateofexpiry", "yes")
    if expired == "yes":
        return render(request, "profiles/sign_in.html")
    cntx = {"message_in": f"Welcome back {curr_user['email']}"}
    return render(request, "profiles/home_page.html", cntx) 


class SignUp(View):
    def get(self, request):
        if request.session.get("save", None) == "both":
            message = request.session.get("message")
            cntx = {"message": message}
            del request.session["save"]
            del request.session["message"]
            return render(request, "profiles/sign_in.html", cntx)
        elif request.session.get("save", None) == "password":
            message = request.session.get("message")
            cntx = {"message": message}
            del request.session["save"]
            del request.session["message"]
            return render(request, "profiles/sign_up.html", cntx)
        elif request.session.get("save", None) == "email":
            message = request.session.get("message")
            cntx = {"message": message}
            del request.session["save"]
            del request.session["message"]
            return render(request, "profiles/sign_up.html", cntx)
        else:
            return render(request, "profiles/sign_up.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        find_email = Profiles.objects.filter(email=email).first()
        find_password = Profiles.objects.filter(password=password).first()
        if not (find_email) and not (find_password):
            new_profile = Profiles(email=email, password=password)
            new_profile.save()
            message = "Congratulations! You have successfully signed up. Sign in to get Welcomed aboard! 🎉"
            request.session["message"] = message
            request.session["save"] = "both"
            return redirect(request.path)
        elif find_email:
            message = "The email address provided is already registered. Please try logging in or use a different email address."
            request.session["save"] ="password"
            request.session["message"] = message
            return redirect(request.path)
        else:
            message = "The password provided is already taken. Please try logging in or use a different and secure password."
            request.session["save"] = "email"
            request.session["message"] = message
            return redirect(request.path)


class SignIn(View):
    def get(self, request):
        if request.session.get("issue", None) == "solved":
            message = request.session.get("message")
            del request.session["message"]
            del request.session["issue"]
            cntx = {"message_in": message}
            return render(request, "profiles/home_page.html", cntx)
        elif request.session.get("issue", None) == "email":
            message = request.session.get("message")
            del request.session["message"]
            del request.session["issue"]
            cntx = {"message_in": message}
            return render(request, "profiles/sign_in.html", cntx)
        elif request.session.get("issue", None) == "password":
            message = request.session.get("message")
            del request.session["message"]
            del request.session["issue"]
            cntx = {"message_in": message}
            return render(request, "profiles/sign_in.html", cntx)
        else:
            return render(request, "profiles/sign_in.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        check_email = Profiles.objects.filter(email=email).first()
        if check_email is None:
            message = "User not found. Please verify your details or sign up."
            request.session["message"] = message
            request.session["issue"] = "email"
            return redirect(request.path)
        check_password = check_email.password
        if check_password == password:
            logins = request.session.get(f"{check_email.email}", 0) + 1
            request.session[f"{check_email.email}"] = logins
            request.session["curr_user"] = {"email": check_email.email, "password": check_email.password}
            if logins > 1:
                message = f"Welcome back {check_email.email}."
                request.session["message"] = message
                request.session["issue"] = "solved"
                response = redirect(request.path)
                response.set_cookie("dateofexpiry", "expires", max_age=900)
                return response
            message = f"Welcome onboard {check_email.email}."
            request.session["message"] = message
            request.session["issue"] = "solved"
            response = redirect(request.path)
            response.set_cookie("dateofexpiry", "expires", max_age=900)
            return response
        message = "Invalid password. Please try again."
        request.session["message"] = message
        request.session["issue"] = "password"
        return redirect(request.path)
