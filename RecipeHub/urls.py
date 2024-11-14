from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Recipe_app.views import home,login_view,register_view,main_view,custom_logout,my_recipes,create_recipe,recipe_detail,toggle_favorite,update_recipe,delete_recipe,view_recipe,favorite_recipes,contact_us,my_profile,search_recipes,foodie_club,toggle_share_recipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('main/', main_view, name='main'), 
    path('logout/', custom_logout, name='logout'),
    path('create-recipe/', create_recipe, name='create_recipe'),
    path('my-recipes/', my_recipes, name='my_recipes'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('toggle-favorite/<int:recipe_id>/', toggle_favorite, name='toggle_favorite'),
    path('recipe/<int:recipe_id>/update/', update_recipe, name='update_recipe'),
    path('recipe/<int:id>/delete/', delete_recipe, name='delete_recipe'),
    path('recipe/<int:id>/', view_recipe, name='view_recipe'),
    path('favorite_recipes/', favorite_recipes, name='favorite_recipes'),
    path('contact/', contact_us, name='contact_us'),
    path('profile/', my_profile, name='my_profile'),
    path('search/',search_recipes, name='search_recipes'),
    path('foodie_club/', foodie_club, name='foodie_club'),
    path('toggle_share_recipe/<int:recipe_id>/', toggle_share_recipe, name='toggle_share_recipe'),


    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
