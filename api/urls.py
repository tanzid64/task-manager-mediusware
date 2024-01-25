from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path , include
from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView, TaskCompleteAPIView, TaskViewSet, UserPasswordChangeAPIView, PasswordResetAPIView
router = DefaultRouter()
router.register('all_tasks', TaskViewSet, basename='task-list-api') # Router For All Task List
urlpatterns = [
    path('accounts/register/', UserRegistrationAPIView.as_view(), name='registration-api'),
    path('accounts/login/', UserLoginAPIView.as_view(), name='login-api'),
    path('accounts/logout/', UserLogoutAPIView.as_view(), name='logout-api'),
    path('accounts/password/change/', UserPasswordChangeAPIView.as_view(), name='pass-change-api'),
    path('accounts/password/reset/', PasswordResetAPIView.as_view(), name='pass-reset-api'),
    path('accounts/profile/', UserProfileAPIView.as_view(), name='profile-api'),
    path('complete_task/<str:slug>/', TaskCompleteAPIView.as_view(), name='complete-task-api'),
    path('', include(router.urls))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
