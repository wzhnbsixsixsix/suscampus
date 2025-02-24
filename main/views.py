from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def first_page(request):
    return redirect('accounts:login')

@login_required
def map(request):
    return render(request, "map.html")

@login_required
def forest(request):
    return render(request, "forest.html")

