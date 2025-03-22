from celery import shared_task
from shop.models import UserBalance, CurrencyTransaction
from .models import TreeScore
from celery.schedules import crontab
from celery import Celery

app = Celery('sustainableCampus')

@shared_task
def reward_top_players():
    """Ensures the top 10 players are rewarded every Saturday."""

    top_10_players = TreeScore.objects.order_by('-score')[:10]
    reward_amount = [100, 75, 50, 25, 25, 25, 25, 25, 25, 25]
    count = 0

    for player in top_10_players:
        user = player.user
        user_balance = UserBalance.objects.get(user_id=user)

        # Update balance
        user_balance.currency += reward_amount[count]
        user_balance.save()

        # Create a transaction record for each user in the top 10 who are rewarded
        CurrencyTransaction.objects.create(
            user=user,
            currency_difference=reward_amount[count],
            description=f"Weekly reward for being a top player in the leaderboard",
            game_keeper=None
        )

        count += 1


# Schedule the task every Saturday at midnight (00:00 UTC)
app.conf.beat_schedule = {
    'reward_top_players_every_saturday': {
        'task': 'leaderboards.tasks.reward_top_players',
        'schedule': crontab(minute=0, hour=0, day_of_week='saturday'),  # Runs every Saturday at midnight
    },
}