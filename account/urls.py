from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, UserProfileUpdateView, UserPasswordUpdateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('edit_password/', UserPasswordUpdateView.as_view(), name='edit_password'),
    # Password Reset
    path('reset_password/', PasswordResetView.as_view(template_name='account/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'), name ='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name ='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)