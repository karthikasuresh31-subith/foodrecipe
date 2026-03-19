from django.urls import path
from adminapp import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('users/', views.users, name='users'),
    path('recipes/', views.recipes, name='recipes'),
    path('reports/', views.reports, name='reports'),
    path('viewrecipe/', views.viewrecipe, name='viewrecipe'),
    path('viewuser/', views.viewuser, name='viewuser'),
     path('dashboard/', views.dashboard, name='dashboard'),
]