from django.shortcuts import render
from django.http import HttpResponse

def map(request):
    return render(request, 'home.html')
