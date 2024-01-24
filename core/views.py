from django.shortcuts import render
from django.views.generic import TemplateView
from task.models import Task
# Create your views here.
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Task.objects.all()
        return context