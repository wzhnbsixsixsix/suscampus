from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Suggestion
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test


@login_required
def suggestions(request):
    if request.method == 'POST':
        content = request.POST.get('suggestion', '').strip()
        category = request.POST.get('category', None)

        if not content or len(content) < 5:
            messages.error(request, 'Suggestion content cannot be empty or too short')
            return redirect('suggestions')

        if not category or category not in dict(Suggestion.CATEGORY_CHOICES):
            messages.error(request, 'Please select a valid category')
            return redirect('suggestions')

        Suggestion.objects.create(
            user=request.user,
            content=content,
            category=category
        )
        messages.success(request, 'Suggestion submitted successfully!')
        return redirect('suggestions')

    return render(request, 'suggestions.html')


@login_required
def view_suggestions(request):




    suggestions = Suggestion.objects.all().order_by('-created_at')
    return render(request, 'view_suggestions.html', {'suggestions': suggestions})


@login_required
def delete_suggestion(request, suggestion_id):
    try:
        suggestion = Suggestion.objects.get(id=suggestion_id)
        # Check permissions: Current user is a submitter or administrator.
        if request.user == suggestion.user or request.user.is_superuser:
            suggestion.delete()
            messages.success(request, 'Suggestion deleted successfully')
        else:
            messages.error(request, 'You do not have permission to delete this suggestion')
    except Suggestion.DoesNotExist:
        messages.error(request, 'Suggestion does not exist')
    return redirect('view_suggestions')
