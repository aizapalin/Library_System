
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from book_management import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # BOOK APP
    path('books/', include('book_management.urls')),
    path('librarian/register/', book_views.register_librarian, name='register_librarian'),
    path('', RedirectView.as_view(url='/books/', permanent=False)),

    path('accounts/', include('allauth.urls')),
    path('members/', include("members.urls")),
    path('borrow/', include("borrow.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)