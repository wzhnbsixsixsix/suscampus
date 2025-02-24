from django.shortcuts import render, get_object_or_404
from .models import TreeScore

def leaderboard(request):
    # Retrieves the top 10 players with the highest number of trees grown
    all_player_scores = TreeScore.objects.order_by('-score')

    # Retrieves the logined user score
    user_score = TreeScore.objects.get(user=request.user)

    # Finds user rank
    user_rank = 0
    while True:
        user_rank += 1
        if all_player_scores[user_rank - 1] == user_score:
            break

    context = {'top_players':all_player_scores[:10], 'user_score':user_score, 'user_rank': user_rank}
    return render(request, 'leaderboards/leaderboards.html', context)

