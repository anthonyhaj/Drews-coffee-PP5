from django.shortcuts import render
from django.http import HttpResponse

def profile(request):
    """ Display the user's profile. """

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)