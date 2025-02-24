from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def suggestions(request):
    return render(request, 'suggestions.html')

@login_required
def view_suggestions(request):
    return render(request, 'view_suggestions.html')