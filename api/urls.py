from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView, TaskListCreateAPIView, TaskDetailAPIView, TaskCompleteAPIView
urlpatterns = [
    path('accounts/register/', UserRegistrationAPIView.as_view(), name='registration-api'),
    path('accounts/login/', UserLoginAPIView.as_view(), name='login-api'),
    path('accounts/logout/', UserLogoutAPIView.as_view(), name='logout-api'),
    path('accounts/profile/', UserProfileAPIView.as_view(), name='profile-api'),
    path('tasks/all_tasks/', TaskListCreateAPIView.as_view(), name='all-tasks-api'),
    path('tasks/detail_task/<str:slug>/', TaskDetailAPIView.as_view(), name='detail-task-api'),
    path('tasks/complete_task/<str:slug>/', TaskCompleteAPIView.as_view(), name='complete-task-api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
