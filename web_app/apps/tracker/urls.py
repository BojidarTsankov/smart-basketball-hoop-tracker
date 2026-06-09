from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start_training', views.start_training, name='start_training'),
    path('session/<int:session_id>/', views.live_session, name='live_session'),
    path('session/<int:session_id>/end', views.end_session, name='end_session'),
    path('history/', views.training_history, name='training_history'),
]
