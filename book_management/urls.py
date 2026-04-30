from django.urls import path
from . import views

app_name = 'book_management'

# This URL list maps book-management routes to their view functions.
urlpatterns = [
    # This route opens the main book listing page.
    path('', views.index, name='index'),
    # This route returns live search suggestions for the search bar.
    path('suggest/', views.search_suggestions, name='search_suggestions'),
    # This route opens the current user's profile page.
    path('profile/', views.profile, name='profile'),
    # This route opens the profile edit page.
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # This route opens the detail page for a specific book.
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # These routes handle account sign-up, login, and logout.
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_user, name='logout'),

    # These routes handle adding, editing, deleting, and managing related records.
    path('add/', views.add_book, name='add_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-category/', views.add_category, name='add_category'),
]