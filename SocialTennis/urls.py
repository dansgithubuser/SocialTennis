from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('signup', views.signup),
    path('login', auth_views.LoginView.as_view(template_name='login.html')),
    path('friend', views.friend),
    path('event', views.event),
    path('event/delete/<int:id>', views.event_delete),
]
