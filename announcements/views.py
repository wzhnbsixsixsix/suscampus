from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Announcement
from .forms import AnnouncementForm
from django.contrib import messages


@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    if not request.user.is_authenticated: # makes sure user is logged in
        return redirect('/accounts/login/')  
    if request.user.role == 'player':  # makes sure user can't post if player role
        messages.error(request, "You must be a Game Keeper to access this page.")    
        return redirect('/announcements/')
    if request.method == 'POST': # posts the announcement
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            new_announcement = form.save(commit=False)
            new_announcement.author = request.user
            new_announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create_announcement.html', {'form': form})


@login_required
def like_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    user = request.user

    if user in announcement.likes.all():
        announcement.likes.remove(user)  # Unlike the announcement
    else:
        announcement.likes.add(user)  # Like the announcement
        announcement.dislikes.remove(user)  # Remove like if the user had liked it

    return redirect('/announcements/', announcement_id=announcement.id)  # Redirect to the announcement detail page

@login_required
def dislike_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    user = request.user

    if user in announcement.dislikes.all():
        announcement.dislikes.remove(user)  # Remove dislike
    else:
        announcement.dislikes.add(user)  # Add dislike
        announcement.likes.remove(user)  # Remove like if the user had liked it

    return redirect('/announcements/', announcement_id=announcement.id)