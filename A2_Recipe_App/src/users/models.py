from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from recipes.models import Recipe

class User(AbstractUser):
    email = models.EmailField(unique=True)
    saved_recipes = models.ManyToManyField(Recipe, related_name='saved_by_users', blank=True)

    class Meta:
        # Add unique related names to avoid clashes
        permissions = [
            ("can_add_recipe", "Can add recipe"),
            ("can_edit_recipe", "Can edit recipe"),
            ("can_delete_recipe", "Can delete recipe"),
        ]

    # Use unique related names for groups and user_permissions
    groups = models.ManyToManyField(
        "auth.Group", related_name="%(app_label)s_%(class)s_related", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="%(app_label)s_%(class)s_related", blank=True
    )

    def __str__(self):
        return self.username
