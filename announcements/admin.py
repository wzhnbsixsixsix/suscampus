
from django.contrib import admin

# Register your models here.
=======
# social/admin.py
from django.contrib import admin
from .models import Announcement

admin.site.register(Announcement)

# Register your models here.
