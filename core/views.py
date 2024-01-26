from django.shortcuts import render
from django.views.generic import TemplateView
from task.models import Task
from django_filters.views import FilterView
from api.filters import TaskFilter
# Create your views here.
# class HomeView(TemplateView):
#     template_name = 'core/home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset = Task.objects.all()
#         priority_filter = self.request.GET.get('priority', None)
#         due_date_filter = self.request.GET.get('due_date', None)
#         created_at_filter = self.request.GET.get('created_at', None)
#         search_query = self.request.GET.get('search', None)

#         if priority_filter:
#             context['data'] = Task.objects.filter(priority=priority_filter)

#         if due_date_filter:
#             queryset = queryset.filter(due_date=due_date_filter)

#         if created_at_filter:
#             queryset = queryset.filter(created_at__date=created_at_filter)
        
#         if search_query:
#             queryset = queryset.filter(title__icontains=search_query)
#         context['data'] = queryset
#         return context
    
class HomeView(FilterView):
    template_name = 'core/home.html'
    filterset_class = TaskFilter
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context['filter'].form.cleaned_data)
        return context