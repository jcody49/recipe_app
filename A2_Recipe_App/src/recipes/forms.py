from django import forms
from .models import Recipe

# ModelForm for entering a new recipe
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

# Define a form class named SearchForm, which inherits from the base class forms.Form.
class SearchForm(forms.Form):
    # Define a form field named 'query' with type: CharField
    # - It is a text input field
    # - It has a label 'Recipe Name or Ingredients'
    # - The maximum length of input allowed is 100 characters.
    # - It is not marked as required, meaning it can be left empty.
    query = forms.CharField(label='Recipe Name or Ingredients', max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()      # super().clean() is a call to the clean method of the parent class, forms.Form, to retrieve the cleaned data for all the form fields.
        query = cleaned_data.get('query')       # retrieving the cleaned and validated value of the 'query' field from the cleaned_data dictionary
        # If the 'query' field is empty, it raises a ValidationError indicating that the user should enter a search query or ingredients
        if not query:
            raise forms.ValidationError({'query': 'Please enter a search query or ingredients.'})

        return cleaned_data






