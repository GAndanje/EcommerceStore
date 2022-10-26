from django.urls import path
from . import views
urlpatterns = [
    path('Register/',views.register,name="register"),
    path('Login/',views.login,name='login'),
    path('Logout/',views.logout,name='logout'),

]
