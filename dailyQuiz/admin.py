from django.contrib import admin
from .models import QuizQuestion, QuizAttempt, QuizDailyStreak

# Register your models here.
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option')

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date', 'is_submitted')

class QuizDailyStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'last_completed_quiz_date')


admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuizDailyStreak, QuizDailyStreakAdmin)