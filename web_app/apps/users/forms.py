from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PlayerProfile

POSITION_CHOICES = [
    ('', 'Select a position'),
    ('PG', 'Point Guard'),
    ('SG', 'Shooting Guard'),
    ('SF', 'Small Forward'),
    ('PF', 'Power Forward'),
    ('C',  'Center'),
]


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    height = forms.FloatField(required=False, help_text="Height in cm")
    favorite_position = forms.ChoiceField(
        choices=POSITION_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            PlayerProfile.objects.create(
                user=user,
                height=self.cleaned_data['height'],
                favorite_position=self.cleaned_data['favorite_position']
            )

        return user


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class PlayerProfileForm(forms.ModelForm):
    favorite_position = forms.ChoiceField(
        choices=POSITION_CHOICES, required=False)

    class Meta:
        model = PlayerProfile
        fields = ['height', 'favorite_position']
