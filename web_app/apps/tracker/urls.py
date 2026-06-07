from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start_training', views.start_training, name='start_training'),
    path('session/<int:session_id/', views.live_session, name='live_session'),
]
