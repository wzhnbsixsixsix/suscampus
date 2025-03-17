from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pathlib import Path
from .models import UserForest, UserInventory

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
    # gets the state of the user's forest saved to the database
    user_forest = UserForest.objects.get(user=request.user)
    user_inventory = UserInventory.objects.get(user=request.user)
    user_data = {"content" : user_forest.cells, "inv" : user_inventory}
    print(user_data)
    return render(request, "forest.html", user_data)

@login_required
def claim_blue_marker(request):
    print("blue claimed")
    user_inventory = UserInventory.objects.get(user=request.user)

@login_required
def claim_red_marker(request):
    print("red claimed")
    user_inventory = UserInventory.objects.get(user=request.user)

@login_required
def claim_green_marker(request):
    print("green claimed")
    user_inventory = UserInventory.objects.get(user=request.user)

@login_required
def save_forest(request):
    print("saving")
    user_forest = UserForest.objects.get(user=request.user)
