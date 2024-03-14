from django.shortcuts import render
from .models import Country, Language
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.html import escape
# create your view here


@method_decorator(csrf_exempt, name="dispatch")
class TranslateView(View):
    # define get method
    def get(self, request):
        context = request.session.get("cntx")
        return render(request, "qwik_aids/translate.html", context)

    # define post method
    def post(self, request):
        country = request.POST.get("country")
        city = request.POST.get("city")
        district = request.POST.get("district")
        languages = Country.objects.filter(country_name=country).first().languages.all()
        main_language = languages[0].language_code
        all_language_list = [language.language_code for language in languages]
        all_language_string = ",".join(all_language_list)
        context = {"country": country, "city": city, "district": district, "m_lang": main_language, "all_lang": all_language_string}
        # now save this context data in the request session temporarily
        request.session["cntx"] = context

        """
        now redirect the path that brought the post request so a get request is sent back
        but this is only possible because we used class based view instead of function
        because we can define post, get, put and delete actions inside of it
        but if we have add function views it would have been difficult but possible
        because we would have to redirect to the same/different application and a different
        view because no to view fucntion would do the same thing it is either get, post, put
        or delete. This action we are preventing is called the POST REFRESH ISSUE
        solved using the POST-REDIRECT-GET REFRESH.
        """
        return redirect(request.path)

def testcookie(request):
    resp_string = """
    Here are the cookies sent by the webbrowser
    after getting them from the webserver 
    """
    if request.COOKIES.get("435", False):
        resp_string += escape(request.COOKIES)
        return HttpResponse(resp_string)
    resp = HttpResponse(resp_string)
    resp.set_cookie("435", "emmanuelobolo", max_age=6000)
    return resp

def sessfun(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    if num_visits > 4 : del(request.session["num_visits"])
    return HttpResponse("view count="+str(num_visits))
