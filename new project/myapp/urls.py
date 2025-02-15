from django.urls import path
from . import views

app_name = 'myapp'  # Namespace for URL mapping

urlpatterns = [
    path('', views.index, name='index'),  # Home Page
    path('about/', views.about, name='about'),  # About Page
    path('<int:cat_no>/', views.detail, name='detail'),  # Category Detail Page
]
