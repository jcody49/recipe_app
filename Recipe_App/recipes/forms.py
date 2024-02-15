from django import forms
from .models import Recipe

# ModelForm for entering a new recipe
class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(label='Ingredients', widget=forms.Textarea(attrs={'rows': 4}))
    
    # Add the pic field with required=False
    pic = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'min_serving_size', 'max_serving_size',
                  'type_of_recipe', 'ingredients', 'directions', 'pic']
        exclude = ['difficulty']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['cooking_time'].widget.attrs['placeholder'] = 'Enter cooking time in minutes'
        self.fields['ingredients'].widget.attrs['placeholder'] = 'Enter ingredients, separated by commas'
        self.fields['directions'].widget.attrs['rows'] = 5
        
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







