
# models.py

from django.db import models  
from django.contrib.auth.models import User  

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='announcement_images/', null=True, blank=True)  # Image field

    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_author_role(self):
        return self.author.role  


