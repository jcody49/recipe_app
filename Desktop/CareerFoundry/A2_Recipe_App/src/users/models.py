from django.db import models



class User(models.Model): 
    username = models.CharField(max_length=120)
    # on_delete=models.SET_NULL specifies what should happen when the referenced Recipe is deleted--being set to SET_NULL means that if a recipe is deleted, the favorite_recipe field in the user model will be set to NULL , ensuring that a user's favorite recipe doesn't become invalid or reference a non-existent recipe.
    saved_recipes = models.ForeignKey('recipes.Recipe', on_delete=models.SET_NULL, blank=True, null=True)       # models.ForeignKey: This indicates that favorite_recipe is a ForeignKey field, establishing a many-to-one relationship between CustomUser and Recipe models.  

    def __str__(self):
        return self.username