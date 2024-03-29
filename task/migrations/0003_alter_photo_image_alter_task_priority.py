# Generated by Django 5.0.1 on 2024-01-24 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=10),
        ),
    ]
