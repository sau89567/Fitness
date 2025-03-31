from django.contrib import admin

# Register your models here.

from .models import Workout
from fitness.models import FitnessClass

admin.site.register(Workout)
@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'duration')
    search_fields = ('title', 'instructor')