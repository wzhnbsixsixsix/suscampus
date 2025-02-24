from django.db import models

# Test model to show how the leaderboard will work. Will be changed or deleted in final version
class TreeScore(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, primary_key=True)
    score = models.IntegerField(default=0)
