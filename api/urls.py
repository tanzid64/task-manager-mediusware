from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='registration-api'),
    path('login/', UserLoginAPIView.as_view(), name='login-api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
