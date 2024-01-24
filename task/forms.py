from typing import Any
from django import forms
from .models import Task, Photo

class AddTaskForm(forms.ModelForm):
    task_photo = forms.ImageField(required=False)
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For Image Field 
        self.fields['task_photo'].widget.attrs.update({
            'class': 'bg-gray-200',
            'required': False
        })
        # For other all fields
        for field in self.fields:
            if field != 'image':
                self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ),
                'required': False
            })