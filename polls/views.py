from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.

# def index(request):
#     recent = Question.objects.order_by("-pub_date")[:5]
#     return render(request, "polls/index.html", {"recentPosts": recent})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "recentPosts"

    #this sets the model similar to model=Question below
    def get_queryset(self):
        #retrieves 5 most recent questions
        return Question.objects.order_by("-pub_date")[:5]

# def detail(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": q})

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    #don't need to set context_object_name=question bc django defaults to model.tolowercase()

# def results(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": q})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        #either nothing was selected or an invalid choice by altering the html
        #rerender the form with an error message
        return render(request, "polls/detail.html", {"question": question, "error_message": "Please select a choice."})
    else:
        #increase the number of votes in the db
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        #always redirect after successfully processing a post form
        #this prevents resubmission with the back button
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))