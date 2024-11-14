from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)  # For marking favorite recipes
    shared = models.BooleanField(default=False)

    def clean(self):
        # Ensure description doesn't exceed 100 words
        word_count = len(self.description.split())
        if word_count > 60:
            raise ValidationError("Description should not exceed 60 words.")
    
    def __str__(self):
        return self.title
