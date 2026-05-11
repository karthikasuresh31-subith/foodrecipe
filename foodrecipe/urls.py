from django.urls import path
from adminapp import views  


urlpatterns = [
    path('adminlogin/', views.Adminlogin, name='login'),
    path('users/', views.users, name='users'),
    path('recipes/', views.recipes, name='recipes'),
    path('reports/', views.reports, name='reports'),
    path('viewrecipe/<int:recipe_id>/', views.viewrecipe, name='viewrecipe'),
    path('viewuser/<int:user_id>/', views.viewuser, name='viewuser'),
    path('dashboard/', views.dashboard, name='dashboard'),



    path('signup/', views.Signup, name='signup'),
    path('login', views.Userlogin, name='login_api'),
    path('profile/', views.profile, name='profile'),
    path('create/',views.add_recipe),
    path('ViewRecipe/',views.ViewRecipe,name='ViewRecipe'),
    path('addrecipe/',views.add_recipe,name='add-recipe'),
    path('editrecipe/<int:recipe_id>/', views.edit_recipe, name='edit-recipe'),

    # path('simple_view/', views.simple_view, name='simple_view'),
]