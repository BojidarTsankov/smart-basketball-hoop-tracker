from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Max
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt

from .models import TrainingSession, Shot

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

    aggregates = trainings.aggregate(
        total=Sum('total_shots'),
        made=Sum('made_shots')
    )

    total_shots = aggregates['total'] or 0
    made_shots = aggregates['made'] or 0

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
def training_history(request):
    trainings = TrainingSession.objects.filter(
        user=request.user
    ).order_by('-start_time')

    return render(request, 'history.html', {'trainings': trainings})


@login_required
def start_training(request):
    active_session = TrainingSession.objects.filter(
        user=request.user,
        end_time__isnull=True
    ).first()

    if active_session:
        session = active_session
    else:
        session = TrainingSession.objects.create(user=request.user)

    return redirect('live_session', session_id=session.id)


@login_required
def live_session(request, session_id):
    session = get_object_or_404(
        TrainingSession, id=session_id, user=request.user)

    return render(request, 'live_session.html', {
        'session': session
    })


@login_required
def end_session(request, session_id):
    session = get_object_or_404(
        TrainingSession, id=session_id, user=request.user)
    session.end_time = timezone.now()
    session.save()

    return redirect('dashboard')


@login_required
def stats(request):
    trainings = TrainingSession.objects.filter(
        user=request.user
    )

    total_trainings = trainings.count()

    total_shots = sum(
        t.total_shots for t in trainings
    )

    made_shots = sum(
        t.made_shots for t in trainings
    )

    shooting_percentage = (
        round(made_shots / total_shots * 100, 1)
        if total_shots else 0
    )

    best_accuracy = 0

    for t in trainings:
        if t.total_shots:
            acc = round(
                t.made_shots / t.total_shots * 100,
                2
            )
            best_accuracy = max(
                best_accuracy,
                acc
            )

    most_shots = trainings.aggregate(
        Max("total_shots")
    )["total_shots__max"] or 0

    average_shots = trainings.aggregate(
        Avg("total_shots")
    )["total_shots__avg"] or 0

    context = {
        "total_trainings": total_trainings,
        "total_shots": total_shots,
        "made_shots": made_shots,
        "shooting_percentage": shooting_percentage,
        "best_accuracy": best_accuracy,
        "most_shots": most_shots,
        "average_shots": round(average_shots, 1),
    }

    return render(request, 'stats.html', context)


@csrf_exempt
def record_shot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            made = data.get("made", True)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        active_session = TrainingSession.objects.filter(
            end_time__isnull=True
        ).last()

        if active_session:
            Shot.objects.create(
                training_session=active_session,
                made=made
            )

            active_session.total_shots += 1
            if made:
                active_session.made_shots += 1
            active_session.save()

            return JsonResponse({
                "status": "success",
                "total_shots": active_session.total_shots,
                "made_shots": active_session.made_shots
            })
        else:
            return JsonResponse({"error": "No training started"}, status=404)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)
