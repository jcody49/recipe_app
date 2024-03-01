#test
from django.db import models

class Ingredient(models.Model):
    """
    Model representing an ingredient.

    Fields:
    - name: CharField with a maximum length of 225 characters, representing the name of the ingredient.

    Methods:
    - __str__: Returns a string representation of the model, which is the name of the ingredient.
    """
    name = models.CharField(max_length=225)

    def __str__(self):
        """
        Returns a string representation of the model, which is the name of the ingredient.
        """
        return str(self.name)
