from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from pathlib import Path

def first_page(request):
    return redirect('accounts:login')

@login_required
def map(request):
    markers = ""
    path = Path(__file__).parent / "../sustainableCampus/static/js/markers.json"
    with path.open() as markerFile:
        for line in markerFile:
            print("JSON FILE LINE: " + line)
            markers += line
    print("markers data: " + markers)
    return render(request, "map.html", {"data": markers})

@login_required
def forest(request):
    return render(request, "forest.html")

