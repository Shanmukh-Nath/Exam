from django.urls import path
from . import views
from .views import Register,LoginView,LogoutView,VerificationView,Password_reset
from .api import UsernameValidation,EmailValidationView,Cheating
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name = "index"),
    path('contact/',views.con,name="contact"),
path('gal/',views.gall,name="gal"),
    path('register/',Register.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('username-validate',UsernameValidation.as_view(),name="username-validate"),
    path('cheat/<str:professorname>',Cheating.as_view(),name="cheat"),
    path('email-validate',EmailValidationView.as_view(),name="email-validate"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name = 'activate'), 
    path('reset-password/',Password_reset.as_view(),name="password_reset"),
    path('reset-password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="student/resetPasswordSent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="student/setNewPassword.html"),name="password_reset_confirm"),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="student/resetPasswordDone.html"),name="password_reset_complete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
