# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout
from .forms import WorkoutForm
from fitness.models import FitnessClass
from django.contrib.auth.decorators import user_passes_test
from .forms import FitnessClassForm
def workout_list(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})



def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workout-list')  # Ensure the redirect works
    else:
        form = WorkoutForm()
    
    return render(request, 'workouts/workout_form.html', {'form': form})


def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, request.FILES, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workout-list')
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'workouts/workout_form.html', {'form': form})

def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == 'POST':
        workout.delete()
        return redirect('workout-list')
    return render(request, 'workouts/workout_confirm_delete.html', {'workout': workout})

def classes_list(request):
    classes = FitnessClass.objects.all()
    return render(request, 'workouts/class_detail.html', {'classes': classes})

def class_detail(request, class_id):
    fitness_class = FitnessClass.objects.get(id=class_id)
    return render(request, 'workouts/class_detail.html', {'fitness_class': fitness_class})

# Admin Permission Check
def is_admin(user):
    return user.is_authenticated and user.is_staff

# View All Classes
def fitness_class_detail(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    return render(request, 'workouts/class_detail.html', {'fitness_class': fitness_class})

# Add Class (Admin Only)
@user_passes_test(is_admin)
def add_fitness_class(request):
    if request.method == 'POST':
        form = FitnessClassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workout-list')  # Redirect after adding
    else:
        form = FitnessClassForm()
    return render(request, 'workouts/class_form.html', {'form': form})

# Edit Class (Admin Only)
@user_passes_test(is_admin)
def edit_fitness_class(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    if request.method == 'POST':
        form = FitnessClassForm(request.POST, request.FILES, instance=fitness_class)
        if form.is_valid():
            form.save()
            return redirect('workout-list')
    else:
        form = FitnessClassForm(instance=fitness_class)
    return render(request, 'workouts/class_form.html', {'form': form})

# Delete Class (Admin Only)
@user_passes_test(is_admin)
def delete_fitness_class(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    if request.method == 'POST':
        fitness_class.delete()
        return redirect('workout-list')
    return render(request, 'workouts/class_confirm_delete.html', {'fitness_class': fitness_class})

def class_edit(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    
    if request.method == "POST":
        form = FitnessClassForm(request.POST, instance=fitness_class)
        if form.is_valid():
            form.save()
            return redirect('class-detail', pk=pk)
    else:
        form = FitnessClassForm(instance=fitness_class)

    return render(request, 'workouts/class_edit.html', {'form': form})