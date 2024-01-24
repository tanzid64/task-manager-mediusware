from django.db import models
from core.models import TimeStamp
from account.models import User
from django.utils.text import slugify
from .constants import PRIORITY_CHOICES
# Create your models here.
class Task(TimeStamp):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, related_name='task',default=None,null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Photo(TimeStamp):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='photo_set')
    image = models.ImageField(upload_to='task_photos/')

    def __str__(self):
        return self.image.name