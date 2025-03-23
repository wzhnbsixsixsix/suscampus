# forms.py
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'summary', 'content', 'image', 'is_event']  # Include image in the form

    currency_reward = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(1000)], widget=forms.NumberInput())
    transaction_description = forms.CharField(max_length=200, required=False)
    event_date = forms.DateField(required=False,  widget=forms.DateInput(attrs={'type': 'date'}))
