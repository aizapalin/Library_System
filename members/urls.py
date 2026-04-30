from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'members'

urlpatterns = [
    path('', views.member_index, name='index'),
    path('add/', views.add_member, name='add_member'),
    path('<int:pk>/edit/', views.edit_member, name='edit_member'),
    path('<int:pk>/delete/', views.delete_member, name='delete_member'),
    path('register/', views.register_user, name='register'),
    path('login/', LoginView.as_view(template_name='members/login.html'), name='login'),
]