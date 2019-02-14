from django.urls import path, include
from . import views

app_name = 'products'

extra_patterns = [
    path('create/', views.create, name='create'),
    path('<slug:product_slug>-<int:product_id>/', views.detail, name='detail'),
    path('<slug:product_slug>-<int:product_id>/likes/', views.likes, name='likes'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', include(extra_patterns))
]
