from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'description', 'difficulty', 'image', 'video']  # Ensure correct field names

from django import forms
from fitness.models import FitnessClass

class FitnessClassForm(forms.ModelForm):
    class Meta:
        model = FitnessClass
        fields = ['title', 'instructor', 'duration', 'description', 'image']

