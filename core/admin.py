from django.contrib import admin
from .models import Match, News, AboutMe, Team, Leaderboard, PredictionAccuracy, Vote

admin.site.register(News)
admin.site.register(AboutMe)
admin.site.register(Vote)
admin.site.register(Team)
admin.site.register(Leaderboard)
admin.site.register(PredictionAccuracy)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'team1',
        'team2',
        'prediction',
        'result',
        'prediction_correct'
    )

    def prediction_correct(self, obj):
        return obj.prediction == obj.result



   
