from django.shortcuts import render
from django.http import HttpResponse

def map(request):
    return render(request, "map.html")

def forest(request):
    return render(request, "forest.html")
