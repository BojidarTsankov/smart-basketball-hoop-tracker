from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import TrainingSession

# Create your views here.


def home(request):
    return render(request, 'home.html')


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
