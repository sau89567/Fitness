from django.urls import path
from .views import workout_list, workout_create, workout_update, workout_delete
from django.contrib.auth import views as auth_views
from workouts import views

urlpatterns = [
    path('', workout_list, name='workout-list'),  # Homepage
    path('new/', workout_create, name='workout-create'),
    path('<int:pk>/edit/', workout_update, name='workout-update'),
    path('<int:pk>/delete/', workout_delete, name='workout-delete'),
    path('login/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('classes/', views.classes_list, name='classes'),
    path('classes/<int:class_id>/', views.class_detail, name='class_detail'),
    path('class/<int:pk>/edit/', views.class_edit, name='class-edit'),
    path('class/add/', views.add_fitness_class, name='class-add'),
    path('class/edit/<int:pk>/', views.edit_fitness_class, name='class-edit'),
    path('class/delete/<int:pk>/', views.delete_fitness_class, name='class-delete'),
]
