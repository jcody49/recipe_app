from django import forms
from .models import Recipe

# Define a form class named RecipeForm, which is a ModelForm for the Recipe model
class RecipeForm(forms.ModelForm):
    # Customize the label for the ingredients field
    ingredients = forms.CharField(label='Ingredients', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:     # metaclass is a class for classes, defines specific behaviors for the form like 'fields' and 'exclude'
        # Specify the model to use and the fields to include/exclude in the form
        model = Recipe
        fields = ['name', 'cooking_time', 'min_serving_size', 'max_serving_size',
                  'type_of_recipe', 'ingredients', 'directions', 'pic']
        exclude = ['difficulty']        # we don't want the user to give the difficulty, we want the calculate_difficulty function to  generate it

    # __init__ is a special method used to initialize an object's attributes when an instance of a class is created
    def __init__(self, *args, **kwargs):
        # Initialize the RecipeForm instance with custom attributes or modifications
        super(RecipeForm, self).__init__(*args, **kwargs)       # (self, *args, **kwargs): allows a class to accept any number of positional arguments (*args) and keyword arguments (**kwargs) during the instantiation of an object from the parent class using 'super()'
        # Set a placeholder attribute for the 'cooking_time' and 'ingredients' fields
        self.fields['cooking_time'].widget.attrs['placeholder'] = 'Enter cooking time in minutes'
        self.fields['ingredients'].widget.attrs['placeholder'] = 'Enter ingredients, separated by commas'
        self.fields['directions'].widget.attrs['rows'] = 5      # Adjust the number of rows for the 'directions' field using a Textarea widget

