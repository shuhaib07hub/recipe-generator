from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .spoonacular import get_recipes_by_ingredients
from .models import Favorite


def home(request):
    # Use 'query' to match the <input name="query"> in your template
    query = request.GET.get('query', '').strip()
    recipes = []

    if query:
        try:
            api_results = get_recipes_by_ingredients(query)
        except Exception as e:
            # Log error (optional: print or use logging)
            messages.error(request, "There was a problem fetching recipes. Please try again.")
            api_results = []

        # Normalize external API data to what the template expects
        recipes = [
            {
                "id": item.get("id"),
                "title": item.get("title") or "Untitled",
                "image": item.get("image") or "",
            }
            for item in api_results
        ]

    return render(request, 'home.html', {
        'recipes': recipes,
        'query': query,
    })


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "Account created and logged in!")
        return redirect('home')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('home')


@login_required(login_url='login')
def add_favorite(request, recipe_id):
    # Expect title & image passed as query params (GET) from link in template
    title = request.GET.get('title', '').strip()
    image_url = request.GET.get('image', '').strip()

    if not title:
        return HttpResponseBadRequest("Missing recipe title.")

    # Avoid duplicate favorites
    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe_id=recipe_id,
        defaults={'title': title, 'image_url': image_url}
    )

    if created:
        messages.success(request, f"Added '{title}' to favorites!")
    else:
        messages.info(request, f"'{title}' is already in your favorites.")

    return redirect('favorites')


@login_required(login_url='login')
def favorites(request):
    favs = Favorite.objects.filter(user=request.user).order_by('-id')
    return render(request, 'favorites.html', {'favorites': favs})
