import django_filters
from django.db.models import Q
from task.constants import PRIORITY_CHOICES
from task.models import Task

class TaskFilter(django_filters.FilterSet):
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='exact')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    search = django_filters.CharFilter(method='filter_search', lookup_expr='icontains', label='Search')

    class Meta:
        model = Task
        fields = ['priority', 'due_date', 'created_at', 'search']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value) | queryset.filter(description__icontains=value)
