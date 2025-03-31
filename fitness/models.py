from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()  # Duration in days (e.g., 30 for 1 month)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.plan:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
            self.is_active = date.today() <= self.end_date
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"


class FitnessClass(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='fitness_classes/')
    description = models.TextField()

    def __str__(self):
        return self.title