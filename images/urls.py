# images/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_page, name='upload_page'),  # URL to load the template
    path('upload-image/', views.upload_image, name='upload_image'),  # URL for image upload
    path('visiting-pass/', views.visiting_pass, name='visiting_pass'),
    path('visiting-pass/<str:pass_id>/', views.get_visiting_pass, name='get_visiting_pass'),

]
