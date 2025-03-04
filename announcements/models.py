
# models.py

from django.db import models  
from django.contrib.auth.models import User  

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='announcement_images/', null=True, blank=True)  # Image field

    created_at = models.DateTimeField()
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    likes = models.ManyToManyField('accounts.CustomUser', related_name='liked_announcements', blank=True)  # Many-to-many relationship for likes
    dislikes = models.ManyToManyField('accounts.CustomUser', related_name='disliked_announcements', blank=True) 

    def __str__(self):
        return self.title

    def get_author_role(self):
        return self.author.role  

    def total_likes(self):
        return self.likes.count()
