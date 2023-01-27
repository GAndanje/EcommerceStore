from django.urls import path
from . import views
urlpatterns = [
    path('Register/',views.register,name="register"),
    path('Login/',views.login,name='login'),
    path('Logout/',views.logout,name='logout'),
    path('Dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotPassword/',views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('resetPassword/',views.resetPassword, name='resetPassword'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
]
