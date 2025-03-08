from django.urls import path
from . import views

app_name = 'myapp'  # Namespace for URL mapping

urlpatterns = [
    path('', views.index, name='index'),  # Home Page
    path('about/', views.about, name='about'),  # About Page
    path('<int:cat_no>/', views.detail, name='detail'),  # Category Detail Page
    path('products/', views.products, name='products'),
    path('products/<int:prod_id>/', views.productdetail, name='productdetail'),
    path('place_order/', views.place_order, name='place_order'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('myorders/', views.myorders, name='myorders'),

]
