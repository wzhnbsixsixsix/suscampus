from django.db import models

# Create your models here.
class UserInventory(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, primary_key=True)
    # stores the number of each resource the player has
    paper = models.IntegerField(default=0)
    plastic = models.IntegerField(default=0)
    compost = models.IntegerField(default=0)
    recycled_paper = models.IntegerField(default=0)
    recycled_plastic = models.IntegerField(default=0)
    recycled_compost = models.IntegerField(default=0)
    tree_guard = models.IntegerField(default=0)
    rain_catcher = models.IntegerField(default=0)
    fertilizer = models.IntegerField(default=0)
    oak = models.IntegerField(default=0)
    birch = models.IntegerField(default=0)
    fir = models.IntegerField(default=0)
    red_campion = models.IntegerField(default=0)
    poppy = models.IntegerField(default=0)
    cotoneaster = models.IntegerField(default=0)
    # stores the markers the user has collected today, will reset at midnight
    collected_markers = models.TextField(default = "")

class UserForest(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, primary_key=True)
    cells = models.TextField(default = "{cell_0 : [0,0,0], cell_1 : [0,0,0], cell_2 : [0,0,0], cell_3 : [0,0,0], cell_4 : [0,0,0], cell_5 : [0,0,0],"
    " cell_6 : [0,0,0], cell_7 : [0,0,0], cell_8 : [0,0,0], cell_9 : [0,0,0], cell_10 : [0,0,0], cell_11 : [0,0,0], cell_12 : [0,0,0], cell_13 : [0,0,0],"
    " cell_14 : [0,0,0],cell_15 : [0,0,0]}", max_length=2048)

class Plant(models.Model):
    plant_name = models.TextField(default="plant")
    requirement_type = models.IntegerField()
    rarity = models.IntegerField()