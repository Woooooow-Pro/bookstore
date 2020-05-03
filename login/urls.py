from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('', views.login),
    path('logout/', views.logout, name='logout')
]