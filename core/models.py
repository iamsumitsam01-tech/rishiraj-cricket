from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)

    logo1 = models.ImageField(upload_to='teams/')
    logo2 = models.ImageField(upload_to='teams/')

    match_date = models.DateField()
    match_time = models.TimeField()

    prediction = models.TextField()
    
    
    confidence_team1 = models.IntegerField(default=50)
    confidence_team2 = models.IntegerField(default=50)

    reason1 = models.CharField(max_length=255, blank=True)
    reason2 = models.CharField(max_length=255, blank=True)
    reason3 = models.CharField(max_length=255, blank=True)

    prediction_lock_time = models.DateTimeField(
    null=True,
    blank=True
    )

    is_today_match = models.BooleanField(default=False)
    prediction_locked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"
    result = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )

    prediction_correct = models.BooleanField(
    default=False
    )
    @property
    def is_correct(self):
     return self.prediction == self.result
    
class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news/')
    description = models.TextField()
    category = models.CharField(max_length=50, default="Cricket")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  
   
class AboutMe(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')

    def __str__(self):
        return self.name   
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='teams/')
    captain = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    ranking = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    user_name = models.CharField(max_length=100)
    accuracy = models.IntegerField()

    def __str__(self):
        return self.user_name
    
class PredictionAccuracy(models.Model):
    total_predictions = models.IntegerField(default=0)
    correct_predictions = models.IntegerField(default=0)

    def __str__(self):
        return "Prediction Stats" 
class Vote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE
    )

    selected_team = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'user',
            'match'
        )

    def _str_(self):
        return f"{self.user.username} - {self.match}"                   