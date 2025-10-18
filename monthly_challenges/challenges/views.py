from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
# Create your views here.

challenges_text = {
    "january": "January",
    "february": "February",
    "march": "March",
    "april": "April",
    "may": "May",
    "june": "June",
    "july": "July",
    "august": "August",
    "september": "September",
    "october": "October",
    "november": "November",
    "december": None,
}
def index(request):
    months = list(challenges_text.keys())

    return render(request, 'challenges/index.html', {'months': months})


def monthly_challenges_int(request, month):
    if month not in [_ for _ in range(1, 13)]:
        return HttpResponseNotFound("None")
    month = list(challenges_text.keys())[month - 1]
    text_content = challenges_text[month]
    return render(request, 'challenges/challenges.html', {
        'month': month,
        'text': text_content,
    })


def monthly_challenges(request, month):
    if month not in challenges_text.keys():
        return HttpResponseNotFound("None")
    text_content = challenges_text[month]
    return render(request, "challenges/challenges.html", {
        "text":text_content,
        "month": month,
    })