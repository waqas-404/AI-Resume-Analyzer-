from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/<int:pk>/', views.results, name='results'),
    path('history/', views.history, name='history'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"), 
]