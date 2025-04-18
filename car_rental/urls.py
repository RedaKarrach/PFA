from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rental import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rental.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),

    
    path('about/', views.about, name='about'),  # Add this line
     path('contact/', views.contact, name='contact'),  # Ajouter cette ligne
]



# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)