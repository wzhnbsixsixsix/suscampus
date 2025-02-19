from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def suggestions(request):
    return render(request, 'suggestions.html')

def view_suggestions(request):
    return render(request, 'view_suggestions.html')