from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .models import User,Recipe
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializer import ProfileSerializer
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.contrib import messages


# from .serializers import ProfileSerializer



def Adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_admin:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password, or you are not an admin.')
            return redirect('login')
    return render(request, 'login.html')

@login_required
def users(request):
    q = request.GET.get('q', '')
    if q:
        users_list = User.objects.filter(Q(name__icontains=q) | Q(email__icontains=q))
    else:
        users_list = User.objects.all()
    
    context = {
        'users': users_list,
        'search_query': q,
    }
    return render(request, 'users.html', context)

@login_required
def recipes(request):
    q = request.GET.get('q', '')
    if q:
        recipes_list = Recipe.objects.filter(title__icontains=q)
    else:
        recipes_list = Recipe.objects.all()
    
    context = {
        'recipes': recipes_list,
        'search_query': q,
    }
    return render(request, 'recipes.html', context)

@login_required
def reports(request):
    top_recipes = Recipe.objects.order_by('-views')[:10]
    
    context = {
        'top_recipes': top_recipes,
    }
    return render(request, 'reports.html', context)

@login_required
def ViewRecipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    
    context = {
        'recipe': recipe,
        'image_url': recipe.image.url if recipe.image else None,
        'creator_name': recipe.Createdby.name if recipe.Createdby else 'Unknown',
    }
    return render(request, 'ViewRecipe.html', context)

@login_required
def viewuser(request, user_id):
    user_obj = User.objects.get(id=user_id)
    user_recipes = Recipe.objects.filter(Createdby_id=user_id)
    
    context = {
        'user': user_obj,
        'user_recipes': user_recipes,
        'recipe_count': user_recipes.count(),
    }
    return render(request, 'viewuser.html', context)

@login_required
def dashboard(request):
    total_recipes = Recipe.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    categories = 0  # No Category model
    total_views = Recipe.objects.aggregate(Sum('views'))['views__sum'] or 0
    recent_recipes = Recipe.objects.order_by('-id')[:5]
    
    context = {
        'total_recipes': total_recipes,
        'active_users': active_users,
        'categories': categories,
        'total_views': total_views,
        'recent_recipes': recent_recipes,
    }
    return render(request, 'dashboard.html', context)





@api_view(['POST'])
@permission_classes((AllowAny,))

def Signup(request):
        email  = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        print(email,password,name)
        if not name or not email or not password:
            return Response({'message':'All fields are required'})
        if User.objects.filter(email=email).exists():
            print("ok")
            return  JsonResponse({'message':'Email already exist'})
        user = User.objects.create_user(email=email,password=password)
        user.name = name
        print("ok")
        user.save()
        return JsonResponse({'message':'user created successsfully'} ,status = 200)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Userlogin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile(request):
    if request.method == 'GET':
        user= request.user.id
        profiles = User.objects.filter(id=user)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    

    

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))

def add_recipe(request):
    if request.method == 'POST':
        user = request.user.id
        title = request.data.get('title')
        description = request.data.get('description')
        ingredients = request.data.get('ingredients')
        instructions = request.data.get('instructions')
        image = request.FILES.get('image')
        difficulty_level = request.data.get('difficulty_level')
        cooking_time = request.data.get('cooking_time')

        recipe_obj = Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            image=image,
            difficulty_level=difficulty_level,
            Cooking_time=cooking_time,
            Createdby_id=user
        )
        return Response({'message': 'Recipe added successfully'}, status=200)


@csrf_exempt           
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def viewrecipe(request):
    if request.method == 'GET':
        user = request.user.id
        recipes = Recipe.objects.filter(Createdby_id=user)
        recipe_data = []
        for recipe in recipes:
            recipe_data.append({
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'ingredients': recipe.ingredients,
                'instructions': recipe.instructions,
                'image': recipe.image.url if recipe.image else None,
                'difficulty_level': recipe.difficulty_level,
                'cooking_time': recipe.Cooking_time,
            })
        return Response(recipe_data, status=200)
    
@csrf_exempt    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def viewuser(request):
    if request.method == 'GET':
        user = request.user.id
        users = User.objects.filter(id=user)
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
            })
        return Response(user_data, status=200)
    

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))     
def editprofile(request):
    if request.method == 'POST':
        user = request.user.id
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        user_obj = User.objects.get(id=user)
        user_obj.name = name
        user_obj.email = email
        if password:
            user_obj.set_password(password)
        user_obj.save()
        return Response({'message': 'Profile updated successfully'}, status=200)
    
@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))

def edit_recipe(request, recipe_id):
    if request.method == 'POST':
        user = request.user.id
        title = request.data.get('title')
        description = request.data.get('description')
        ingredients = request.data.get('ingredients')
        instructions = request.data.get('instructions')
        image = request.FILES.get('image')
        difficulty_level = request.data.get('difficulty_level')
        cooking_time = request.data.get('cooking_time')

        recipe_obj = Recipe.objects.get(id=recipe_id, Createdby_id=user)
        recipe_obj.title = title
        recipe_obj.description = description
        recipe_obj.ingredients = ingredients
        recipe_obj.instructions = instructions
        if image:
            recipe_obj.image = image
        recipe_obj.difficulty_level = difficulty_level
        recipe_obj.Cooking_time = cooking_time
        recipe_obj.save()
        return Response({'message': 'Recipe updated successfully'}, status=200)
    



            
            



                        
        

