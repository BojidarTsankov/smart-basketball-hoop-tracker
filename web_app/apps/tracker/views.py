from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg

from .models import TrainingSession

# Create your views here.


def home(request):
    sessions = TrainingSession.objects.all()

    total_shots = sessions.aggregate(total=Sum('total_shots'))['total'] or 0
    total_sessions = sessions.count()

    best_percentage = 0

    for s in sessions:
        if s.total_shots > 0:
            percent = (s.made_shots / s.total_shots) * 100
            if percent > best_percentage:
                best_percentage = percent

    context = {
        'total_shots': total_shots,
        'total_sessions': total_sessions,
        'best_percentage': round(best_percentage, 2)
    }

    return render(request, 'home.html', context)


@login_required
def dashboard(request):

    trainings = TrainingSession.objects.filter(
        user=request.user
    ).order_by('-start_time')

    total_trainings = trainings.count()

    total_shots = sum(
        training.total_shots for training in trainings
    )

    made_shots = sum(
        training.made_shots for training in trainings
    )

    shooting_percentage = 0

    if total_shots > 0:
        shooting_percentage = round(
            (made_shots / total_shots) * 100,
            2
        )

    context = {
        'trainings': trainings,
        'total_trainings': total_trainings,
        'total_shots': total_shots,
        'made_shots': made_shots,
        'shooting_percentage': shooting_percentage,
    }

    return render(request, 'dashboard.html', context)


@login_required
def start_training(request):
    session = TrainingSession.objects.create(user=request.user)
    return redirect('live_session', session_id=session.id)


@login_required
def live_session(request, session_id):
    session = TrainingSession.objects.get(id=session_id, user=request.user)

    return render(request, 'live_session.html', {
        'session': session
    })
