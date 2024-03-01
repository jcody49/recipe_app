#test
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from recipes.models import Recipe

class User(AbstractUser):
    """
    Custom user model extending AbstractUser with additional fields.

    Fields:
    - email: EmailField, unique email address for the user.
    - saved_recipes: ManyToManyField linking to Recipe model, representing recipes saved by the user.

    Meta:
    - permissions: Define custom permissions for adding, editing, and deleting recipes.

    Relationships:
    - groups: ManyToMany relationship with auth.Group.
    - user_permissions: ManyToMany relationship with auth.Permission.

    Methods:
    - __str__: Returns the username as the string representation of the user.
    """
    email = models.EmailField(unique=True)
    #test
    saved_recipes = models.ManyToManyField('recipes.Recipe', related_name='saved_by_users', blank=True)

    class Meta:
        permissions = [
            ("can_add_recipe", "Can add recipe"),
            ("can_edit_recipe", "Can edit recipe"),
            ("can_delete_recipe", "Can delete recipe"),
        ]

    groups = models.ManyToManyField(
        "auth.Group", related_name="%(app_label)s_%(class)s_related", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="%(app_label)s_%(class)s_related", blank=True
    )

    def __str__(self):
        """
        Returns the string representation of the user, which is the username.
        """
        return self.username
