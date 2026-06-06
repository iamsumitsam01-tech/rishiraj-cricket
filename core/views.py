from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Match, News, AboutMe, Vote
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def home(request):
    
    search = request.GET.get('search')

    if search:
     latest_news = News.objects.filter(
        Q(title__icontains=search) |
        Q(description__icontains=search)
    )
    else:
     latest_news = News.objects.order_by('-created_at')[:6]
    
    total_predictions = Match.objects.filter(
    prediction_correct__isnull=False
    ).count()

    all_matches = Match.objects.exclude(result__isnull=True)

    correct_predictions = sum(
    1 for match in all_matches
    if match.is_correct
    )

    wrong_predictions = Match.objects.filter(
    prediction_correct=False
    ).count()

    accuracy = 0

    if total_predictions > 0:
     accuracy = round(
        (correct_predictions / total_predictions) * 100
    ) 

    today_matches = Match.objects.filter(
        is_today_match=True
    )

    upcoming_matches = Match.objects.filter(
        is_today_match=False
    )

    latest_news = News.objects.order_by(
        '-created_at'
    )[:6]
    
    history_matches = Match.objects.exclude(
    result__isnull=True
    ).order_by('-id')[:10]

    all_matches = Match.objects.exclude(result__isnull=True)

    total = all_matches.count()

    correct = sum(
    1 for match in all_matches
    if match.is_correct
    )

    accuracy = 0

    if total > 0:
     accuracy = round((correct / total) * 100)

    return render(request, "index.html", {
    "today_matches": today_matches,
    "upcoming_matches": upcoming_matches,
    "latest_news": latest_news,

    "total_predictions": total_predictions,
    "correct_predictions": correct_predictions,
    "wrong_predictions": wrong_predictions,
    "accuracy": accuracy,
    "now": timezone.now(),
    "about": AboutMe.objects.first(),
})
from .models import Leaderboard, Match, Vote

def predictions(request):

    leaderboard = Leaderboard.objects.order_by('-accuracy')
    match = Match.objects.filter(
    is_today_match=True
).first()

    already_voted = False
    user_vote = None

    if request.method == "POST" and request.user.is_authenticated:

        selected_team = request.POST.get('team')

        already_voted_check = Vote.objects.filter(
            user=request.user,
            match=match
        ).exists()

        if already_voted_check:

            messages.error(
                request,
                "You already voted for this match."
            )

            return redirect('predictions')

        Vote.objects.create(
            user=request.user,
            match=match,
            selected_team=selected_team
        )

        messages.success(
            request,
            f"You voted for {selected_team} successfully!"
        )

        return redirect('predictions')


    if request.user.is_authenticated:

        vote = Vote.objects.filter(
            user=request.user,
            match=match
        ).first()

        if vote:
            already_voted = True
            user_vote = vote.selected_team

    return render(
        request,
        'predictions.html',
        {
            'leaderboard': leaderboard,
            'match': match,
            'already_voted': already_voted,
            'user_vote': user_vote,
        }
    )
def teams(request):
    return render(request, 'teams.html')

def about(request):
    about = AboutMe.objects.first()

    return render(request, 'about.html', {
        'about': about
    })
def contact(request):
    return render(request, 'contact.html')

def news(request):

    news_list = News.objects.order_by('-created_at')

    featured_news = News.objects.first()

    return render(
        request,
        'news.html',
        {
            'news_list': news_list,
            'featured_news': featured_news
        }
    ) 

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'signup.html',
                {'error': 'Username already taken!'}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                'signup.html',
                {'error': 'Email already registered!'}
            )

        if len(username) < 4:
            return render(
                request,
                'signup.html',
                {'error': 'Username must be at least 4 characters'}
            )

        if len(password) < 8:
            return render(
                request,
                'signup.html',
                {'error': 'Password must be at least 8 characters'}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request,user)
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error':'Invalid Credentials'}
        )

    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')  

@login_required(login_url='login')
def vote_prediction(request, match_id):

    match = Match.objects.get(id=match_id)

    already_voted = Vote.objects.filter(
        user=request.user,
        match=match
    ).exists()

    if already_voted:

        return render(
            request,
            'vote.html',
            {
                'match': match,
                'error': 'You already voted for this match.'
            }
        )

    if request.method == "POST":

        selected_team = request.POST.get('team')

        Vote.objects.create(
            user=request.user,
            match=match,
            selected_team=selected_team
        )

        return redirect('predictions')

    return render(
        request,
        'vote.html',
        {
            'match': match
        }
    )  
    
    
    