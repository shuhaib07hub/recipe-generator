from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.IntegerField()
    title = models.CharField(max_length=200)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.title}"