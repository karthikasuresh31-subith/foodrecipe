from django.shortcuts import render


def login(request):
    return render(request, 'login.html')

def users(request):
    return render(request, 'users.html')

def recipes(request):
    return render(request, 'recipes.html')

def reports(request):
    return render(request, 'reports.html')

def viewrecipe(request):
    return render(request, 'viewrecipe.html')

def viewuser(request):
    return render(request, 'viewuser.html')

def dashboard(request):
    return render(request, 'dashboard.html')


