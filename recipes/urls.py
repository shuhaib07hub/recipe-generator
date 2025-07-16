from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('favorites/', views.favorites, name='favorites'),
    path('add_favorite/<int:recipe_id>/', views.add_favorite, name='add_favorite'),
]
