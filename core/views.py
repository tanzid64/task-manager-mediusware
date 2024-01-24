from django.shortcuts import render
from django.views.generic import TemplateView
from task.models import Task
# Create your views here.
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        priority_filter = self.request.GET.get('priority', None)
        due_date_filter = self.request.GET.get('due_date', None)
        created_at_filter = self.request.GET.get('created_at', None)
        queryset = Task.objects.all()

        if priority_filter:
            context['data'] = Task.objects.filter(priority=priority_filter)
        
        if due_date_filter:
            queryset = queryset.filter(due_date=due_date_filter)

        if created_at_filter:
            queryset = queryset.filter(created_at__date=created_at_filter)
        
        context['data'] = queryset
        return context