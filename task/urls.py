from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import AddTaskView, TaskDetailsView, TaskCompleteView, TaskEditView, DeleteTaskImageView, TaskDeleteView
urlpatterns = [
    path('add_task', AddTaskView.as_view(), name='add_task'),
    path('detail_task/<str:slug>/', TaskDetailsView.as_view(), name='detail_task'),
    path('complete_task/<str:slug>/', TaskCompleteView.as_view(), name='complete_task'),
    path('edit_task/<str:slug>/', TaskEditView.as_view(), name='edit_task'),
    path('delete_task/<str:slug>/', TaskDeleteView.as_view(), name='delete_task'),
    path('delete_img/<int:pk>/', DeleteTaskImageView.as_view(), name='del_img'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)