
from django.contrib import admin
from django.urls import include, path

# urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('images.urls')),  # Include images app URLs
]

