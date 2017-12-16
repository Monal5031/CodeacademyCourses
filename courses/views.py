from django.shortcuts import render

from .forms import UsernameForm
from .scraper import Scrape


def query(request):
    return render(request, 'templates/query.html')


def result(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UsernameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Scrape the data and
            # redirect to a new URL:
            person = Scrape(form.username)
            context = {
                'courses': person.courses,
            }
            return render(request, 'templates/result.html', context=context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UsernameForm()

    return render(request, 'templates/query.html', {'form': form})
