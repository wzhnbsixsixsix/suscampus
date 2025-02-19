from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def shop(request):
    return render(request, 'shop.html')

def transactions(request):
    return render(request, 'transactions.html')

