from django.shortcuts import render, redirect
from .spoonacular import get_recipes_by_ingredients
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Favorite



def home(request):
    query = request.GET.get('ingredients')
    recipes = []
    if query:
        recipes = get_recipes_by_ingredients(query)
    return render(request, 'home.html', {'recipes': recipes, 'query': query})
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
def add_favorite(request, recipe_id):
    title = request.GET.get('title')
    image_url = request.GET.get('image')
    Favorite.objects.create(user=request.user, recipe_id=recipe_id, title=title, image_url=image_url)
    return redirect('favorites')

def favorites(request):
    favs = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favs})