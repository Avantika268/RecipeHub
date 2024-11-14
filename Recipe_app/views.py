from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from .forms import RecipeForm
from .models import Recipe
from django.urls import reverse

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def toggle_share_recipe(request, recipe_id):
    if request.method == "POST" and request.user.is_authenticated:
        # Get the recipe that matches the ID and belongs to the logged-in user
        recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
        
        # Toggle the sharing status
        recipe.shared = not recipe.shared
        recipe.save()

        # Prepare the response message based on the action
        message = 'Recipe shared successfully!' if recipe.shared else 'Recipe unshared successfully!'
        return JsonResponse({'success': True, 'message': message, 'shared': recipe.shared})
    else:
        return JsonResponse({'success': False, 'message': 'Failed to update share status.'})
    
def foodie_club(request):
    # Fetch all shared recipes (you can filter or modify this as needed)
    foodie_club_recipes = Recipe.objects.filter(shared=True)
    
    return render(request, 'foodie_club.html', {
        'foodie_club_recipes': foodie_club_recipes
    })


def search_recipes(request):
    query = request.GET.get('query', '')  # Get the search query from the GET parameters
    
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    else:
        recipes = Recipe.objects.all()
    
    no_results = not recipes.exists()  # True if no recipes were found
    
    return render(request, 'my_recipes.html', {'recipes': recipes, 'no_results': no_results})


def my_profile(request):
    user = request.user
    recipes = Recipe.objects.filter(user=user)  # Fetch recipes created by the current user
    return render(request, 'my_profile.html', {'user': user, 'recipes': recipes})


def contact_us(request):
    return render(request, 'contact_us.html')

# Fetch favorite recipes for the current user
def favorite_recipes(request):
    favorite_recipes = Recipe.objects.filter(user=request.user, favorite=True)
    return render(request, 'fav_recipe.html', {'favorite_recipes': favorite_recipes})

def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.favorite = not recipe.favorite  # Toggle favorite status
    recipe.save()
    return redirect(reverse('recipe_detail', kwargs={'recipe_id': recipe.id}))




def view_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def update_recipe(request, recipe_id):  # Change 'id' to 'recipe_id'
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)  # Use 'recipe_id' here
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe_id)  # Use 'recipe_id' in the redirect
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'update_recipe.html', {'form': form, 'recipe': recipe})


def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    recipe.delete()
    return redirect('my_recipes')  # Redirect to the user's recipes page

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form and assign the user to the recipe
            recipe = form.save(commit=False)
            recipe.user = request.user  # Assign the current user
            recipe.save()
            return redirect('my_recipes')  # Redirect to 'my_recipes' page after creation
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})

def my_recipes(request):
    # Fetch recipes belonging to the current user
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'my_recipes.html', {'recipes': recipes})



# Home page view
def home(request):
    return render(request, 'home.html')  # Adjusted to match your folder structure

def recipe_detail(request, recipe_id):
    # Fetch the recipe object
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Get the 'from' parameter from the GET request, default to 'my_recipes'
    from_page = request.GET.get('from', 'my_recipes')
    
    # Pass the recipe and from_page to the template context
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'from_page': from_page})




# Login page view
def login_view(request):
    if request.method == 'POST':
        # Get the username or email and password from the form
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try to get the user by email if provided
        try:
            # Check if it's an email, if so, get the user by email
            user = User.objects.get(email=username_or_email)
            username = user.username  # Replace with the actual username for authentication
        except User.DoesNotExist:
            username = username_or_email  # Otherwise, treat it as a username
        
        # Authenticate the user with the username and password
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return redirect('main')  # Redirect to a page after successful login (adjust this URL name)
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


# Registration page view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Main page view (after login)
def main_view(request):
    return render(request, 'main.html')

def custom_logout(request):
    # Log the user out
    logout(request)
    
    # Optional: Add a success message after logging out
    messages.success(request, "You have successfully logged out.")
    
    # Redirect to the homepage or any other page after logout
    return redirect('home')  # 'home' is the name of your homepage UR


