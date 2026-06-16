from django.contrib import admin
from .models import PlayerProfile

# Register your models here.


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_position', 'height']
