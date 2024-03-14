from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.utils.html import escape
from .models import Question, Choice
from django.template import loader
from django.views import generic
from django.views import View


class IndexView(View):
    def get(self, request):
        question = get_object_or_404(Question, pk=1)
        context = {
            "required_string": "e644f76c",
            "question": question,
        }
        return render(request, "polls/detail.html", context)

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
        "required_string": "e644f76c",
    }
    return HttpResponse(template.render(context, request))

def detail(request, pk):
    return HttpResponse("You're looking at question %s." % pk)

def results(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, "polls/results.html", {"question": question, "required_string": "e644f76c"})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "required_string": "e644f76c",
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def owner(request):
    return HttpResponse("Hello, world. e644f76c is the polls index.")
