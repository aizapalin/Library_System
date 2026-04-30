from django.urls import path
from . import views

app_name = 'borrow'

urlpatterns = [
    # Change 'index' to 'borrow_index' to match your template
    path('', views.borrow_index, name='borrow_index'), 
    path('add/', views.add_borrow, name='add_borrow'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/<str:action>/', views.update_status, name='update_status'),
    path('<int:pk>/edit/', views.edit_borrow, name='edit_borrow'),
    path('<int:pk>/delete/', views.delete_borrow, name='delete_borrow'),
]