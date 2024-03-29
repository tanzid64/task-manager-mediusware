from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .forms import AddTaskForm
from .models import Task, Photo
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.
class AddTaskView(UserPassesTestMixin,FormView):
    template_name = 'task/add_task.html'
    form_class = AddTaskForm
    success_url = reverse_lazy('homepage')
    def test_func(self):
        return self.request.user.is_staff
    def form_valid(self,form):
        form.save()
        messages.success(self.request, 'Task Added Successfully.')
        return super().form_valid(form)
    
class TaskDetailsView(DetailView):
    template_name = 'task/detail_task.html'
    model = Task
    slug_field = 'slug'  # Specify the field to use for the slug
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Photo.objects.filter(task=self.get_object())
        context['total_images'] = Photo.objects.filter(task=self.get_object()).count()
        return context
    
class TaskCompleteView(View):
    def get(self, request, slug):
        task = get_object_or_404(Task, slug=slug)
        task.is_completed = True
        task.completed_by = self.request.user
        task.save()
        messages.success(self.request, 'Successfully completed task.')
        return redirect('homepage')
    
class TaskEditView(UserPassesTestMixin, UpdateView):
    template_name = 'task/edit_task.html'
    model = Task
    form_class = AddTaskForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('homepage')
    def test_func(self):
        return self.request.user.is_staff
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Edit Task'
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Task Updated Successfully')
        return super().form_valid(form)

class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('homepage')
    def test_func(self):
        return self.request.user.is_staff


class DeleteTaskImageView(UserPassesTestMixin, View):
    def get(self, request,pk):
        img = get_object_or_404(Photo, pk=pk)
        img.delete()
        messages.warning(self.request, 'Image Delation Successfull')
        return redirect('homepage')
    def test_func(self):
        return self.request.user.is_staff