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

class UserForest(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, primary_key=True)
    cells = {}
    for i in range(0, 16):
        cells["cell{0}".format(i)] = models.JSONField(null=True)