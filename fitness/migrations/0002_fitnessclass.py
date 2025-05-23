# Generated by Django 5.1.6 on 2025-03-13 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FitnessClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('instructor', models.CharField(max_length=255)),
                ('duration', models.IntegerField(help_text='Duration in minutes')),
                ('image', models.ImageField(upload_to='fitness_classes/')),
                ('description', models.TextField()),
            ],
        ),
    ]
