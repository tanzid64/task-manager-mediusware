from typing import Any
from django import forms
from .models import Task, Photo

class AddTaskForm(forms.ModelForm):
    task_photo = forms.ImageField()
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Task
        exclude = ['completed_by','is_completed', 'slug']
    
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
            task_photo = self.cleaned_data.get('task_photo')
            Photo.objects.create(
                task = task,
                image = task_photo
            )
        return task