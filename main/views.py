from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pathlib import Path
from .models import UserForest, UserInventory, Plant
from django.http import HttpResponse, JsonResponse
from random import randint
from django.views.decorators.csrf import csrf_exempt
import datetime

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
    user_inventory = UserInventory.objects.get(user=request.user)
    collected = user_inventory.collected_markers
    print("inv: ", user_inventory)
    print("collected markers: ", collected)
    return render(request, "map.html", {"data": markers, "collected" : collected})

@login_required
def forest(request):
    # gets the state of the user's forest saved to the database
    user_forest = UserForest.objects.get(user=request.user)
    user_inventory = UserInventory.objects.get(user=request.user)
    # gets all relevant information from the plants table, allowing it to be used within the view/page
    plant_string = ""
    for plant in Plant.objects.all():
        plant_string += str(plant.id) + "," + str(plant.requirement_type) + "," + str(plant.rarity) + "," + str(plant.plant_name) + ";"
    # converts the contents of the user's inventory to a more useful format to be given to the page
    user_inventory_dict = user_inventory.to_dict()
    print(user_inventory_dict)
    user_inventory_str = ""
    for key in user_inventory_dict.keys():
        user_inventory_str += str(user_inventory_dict[key]) + ","
    print(user_inventory_str)
    # calculates the forest value on page load
    value = calculate_forest_value(user_forest)

    return render(request, "forest.html", {"user_forest" : user_forest.cells, "user_inventory" : user_inventory_str, "plant_list" : plant_string, "forest_value" : value})

@login_required
@csrf_exempt
def claim_blue_marker(request):
    print("blue claimed")
    user_inventory = UserInventory.objects.get(user=request.user)
    # blue markers give paper and sometimes seedlings
    user_inventory.paper += randint(1, 4)
    user_inventory = drop_seedling(user_inventory)
    # update collected markers (needs id of marker)
    if (request.method == 'POST' and 'marker_id' in request.POST):
        marker_id = request.POST['marker_id']
        user_inventory.collected_markers += (marker_id + ",")
        curr_date = datetime.datetime.now().isocalendar()
        print("iso date:", curr_date)
        user_inventory.last_collected = str(curr_date[0]) + "-" + str(curr_date[1]) + "-" + str(curr_date[2])
        print("MARKER CLAIMED AT: " + user_inventory.last_collected)
    else:
        return JsonResponse({"result" : "error when recieving marker id"})
    user_inventory.save()
    return JsonResponse({"result" : 1})

@login_required
@csrf_exempt
def claim_red_marker(request):
    print("red claimed")
    user_inventory = UserInventory.objects.get(user=request.user)
    # red markers give plastic and sometimes seedlings
    user_inventory.plastic += randint(1, 4)
    user_inventory = drop_seedling(user_inventory)
    # update collected markers (needs id of marker)
    if (request.method == 'POST' and 'marker_id' in request.POST):
        marker_id = request.POST['marker_id']
        user_inventory.collected_markers += (marker_id + ",")
        curr_date = datetime.datetime.now().isocalendar()
        print("iso date:", curr_date)
        user_inventory.last_collected = str(curr_date[0]) + "-" + str(curr_date[1]) + "-" + str(curr_date[2])
        print("MARKER CLAIMED AT: " + user_inventory.last_collected)
    else:
        return JsonResponse({"result" : "error when recieving marker id"})
    user_inventory.save()
    return JsonResponse({"result" : 1})

@login_required
@csrf_exempt
def claim_green_marker(request):
    print("green claimed")
    user_inventory = UserInventory.objects.get(user=request.user)
    # green markers give compost and sometimes seedlings
    user_inventory.compost += randint(1, 4)
    user_inventory = drop_seedling(user_inventory)
    # update collected markers (needs id of marker)
    if (request.method == 'POST' and 'marker_id' in request.POST):
        marker_id = request.POST['marker_id']
        user_inventory.collected_markers += (marker_id + ",")
        curr_date = datetime.datetime.now().isocalendar()
        print("iso date:", curr_date)
        user_inventory.last_collected = str(curr_date[0]) + "-" + str(curr_date[1]) + "-" + str(curr_date[2])
        print("MARKER CLAIMED AT: " + user_inventory.last_collected)
    else:
        return JsonResponse({"result" : "error when recieving marker id"})
    user_inventory.save()
    return JsonResponse({"result" : "updated user inventory successfully"})

@login_required
def save_forest(request):
    user_forest = UserForest.objects.get(user=request.user)
    return JsonResponse({"result" : "updated user forest successfully"})

@login_required
def drop_seedling(inv):
    # sometimes gives a seedling
    if (randint(1, 10) > 5):
        # there are different rarities of sapling
        rarity = 0
        rand_num_rarity = randint(1, 100)
        if (rand_num_rarity > 90):
            rarity = 2
        elif (rand_num_rarity > 75):
            rarity = 1
        # else rarity remains 0
        # plants that can be obtained depend on the rarity
        match rarity:
            case 0:
                # there are three plants in this rarity
                plant_got = randint(0, 2)
                match plant_got:
                    case 0:
                        inv.oak += 1
                    case 1:
                        inv.birch += 1
                    case 2:
                        inv.poppy += 1
            case 1:
                # only two plants in this rarity
                if (randint(0, 1)):
                    inv.fir += 1
                else:
                    inv.red_campion += 1
            case 2:
                inv.cotoneaster += 1
    return inv

@login_required
def update_inv_on_page(request):
    # used in the geolocSystem itself to update the inventory data on the map page when a user collects a marker
    # this prevents them from collecting the same marker multiple times
    inv_data = UserInventory.objects.get(user=request.user)
    collected = inv_data.collected_markers
    # if the date of the last collected marker is not the current date, reset collected markers so they can all be collected again
    if (collected != ""):
        print("LAST COLLECTED: " + inv_data.last_collected)
        curr_date = datetime.datetime.now().isocalendar()
        curr_date = str(curr_date[0]) + "-" + str(curr_date[1]) + "-" + str(curr_date[2])
        print("CURRENT DATE: " + curr_date)
        if (inv_data.last_collected != curr_date):
            print("Resetting collected markers, the date has changed")
            inv_data.collected_markers = ""
            collected = ""
            inv_data.save()
        else:
            print("Collected markers do not need to be reset")

    return JsonResponse({"collected":collected})

@login_required
def update_forest_on_page(request):
    user_forest = UserForest.objects.get(user=request.user)
    forest_value = calculate_forest_value(user_forest)
    return JsonResponse({"user_forest" : user_forest.cells, "forest_value" : forest_value})

@login_required
def calculate_forest_value(forest):
    plant_list = []
    for plant in Plant.objects.all():
        curr_plant_list = [plant.id, plant.requirement_type, plant.rarity, plant.requirement_type]
        plant_list.append(curr_plant_list)
    # gets the details of each cell in the user's forest, used here to calculate the value of the forest
    forest_cells = forest.cells.split(";")
    cell_details = []
    for cell in forest_cells:
        cell_details.append(cell.split(","))
    print(cell_details)
    # value calculation: 
    # iterate over each cell: if there is a plant in a cell +(100 for common, 150 for uncommon, 200 for rare), account for growth stage (seedlings are worth 0 regardless of rarity, mid stage plants are worth half)
    # count how many unique plants are used
    # multiply total by 1.(number of unique plants)
    unique_plants_count = 0
    unique_plants = [] # stores ids of unique plants in the forest
    value = 0
    for cell in cell_details:
        # if cell is empty skip it
        if cell[0] == '0':
            continue
        else:
            cell_val = 0
            growth_stage = cell[1]
            plant_id = cell[0]
            rarity = plant_list[int(plant_id) - 1][2]

            # checks if the plant is (in the cells that have been iterated through already) unique
            if (plant_id not in unique_plants):
                unique_plants_count += 1
                unique_plants.append(plant_id)

            # seedling only contribute to biodiversity, not the value
            if (growth_stage == '0'):
                continue

            # now check rarity and assign base value accordingly
            if (rarity == '2'):
                cell_val = 200
            elif (rarity == '1'):
                cell_val = 150
            else:
                cell_val = 100
            
            # half the value if the plant is in the middle growth stage
            if (growth_stage == '1'):
                cell_val *= 0.5
            
            value += cell_val
    
    # multiplies the value by 1.(number of unique plants)
    value *= (1 + (unique_plants_count/10))

    print("calculated value: " + str(value))
    return str(value)

@login_required
def get_recycled_count(request):
    user_inv = UserInventory.objects.get(user=request.user)
    recycled_paper = user_inv.recycled_paper
    recycled_plastic = user_inv.recycled_plastic
    recycled_compost = user_inv.recycled_compost
    return JsonResponse({"count_paper" : recycled_paper, "count_plastic" : recycled_plastic, "count_compost" : recycled_compost})

@login_required
@csrf_exempt
def handle_recycling(request):
    user_inv = UserInventory.objects.get(user=request.user)
    if (request.method == 'POST' and 'type' in request.POST):
        recycling_type = request.POST['type']
        match recycling_type:
            case "paper":
                # a paper is recycled; if the user has 5 recycled papers they are automatically
                # turned into a tree guard
                user_inv.paper -= 1
                user_inv.recycled_paper += 1
                if (user_inv.recycled_paper == 5):
                    print("made tree guard")
                    user_inv.tree_guard += 1
                    user_inv.recycled_paper = 0
            case "plastic":
                # works just as paper, but a rain catcher is made instead of a tree guard
                user_inv.plastic -= 1
                user_inv.recycled_plastic += 1
                if (user_inv.recycled_plastic == 5):
                    print("made rain catcher")
                    user_inv.rain_catcher += 1
                    user_inv.recycled_plastic = 0
            case "compost":
                # works just as paper, but fertilizer is made instead of a tree guard
                user_inv.compost -= 1
                user_inv.recycled_compost += 1
                if (user_inv.recycled_compost == 5):
                    print("made fertilizer")
                    user_inv.fertilizer += 1
                    user_inv.recycled_compost = 0
    else:
        return JsonResponse({"result" : "error when recieving recycling data"})
    user_inv.save()
    return JsonResponse({"result" : "database updated to reflect recyled item successfully"})

@login_required
@csrf_exempt
def save_forest(request):
    user_forest = UserForest.objects.get(user=request.user)
    if (request.method == 'POST' and 'user_forest_cells' in request.POST):
        user_forest.cells = request.POST['user_forest_cells']
    else:
        return JsonResponse({"result" : "error when receiving user forest"})
    user_forest.save()
    return JsonResponse({"result" : "updated user forest successfully"})

@login_required
def get_plant_list(request):
    plantString = ""
    for plant in Plant.objects.all():
        plantString += plant.id + "," + plant.requirement_type + "," + plant.rarity + "," + plant.plant_name + ";"

    return JsonResponse({"plant_list" : plantString})
