from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """
    ModelForm for entering a new recipe.
    """
    ingredients = forms.CharField(label='Ingredients', widget=forms.Textarea(attrs={'rows': 4}))
    pic = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'min_serving_size', 'max_serving_size',
                  'type_of_recipe', 'ingredients', 'directions', 'pic']
        exclude = ['difficulty']

    def __init__(self, *args, **kwargs):
        """
        Constructor for RecipeForm class.
        """
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['cooking_time'].widget.attrs['placeholder'] = 'Enter cooking time in minutes'
        self.fields['ingredients'].widget.attrs['placeholder'] = 'Enter ingredients, separated by commas'
        self.fields['directions'].widget.attrs['rows'] = 5

class SearchForm(forms.Form):
    """
    Form class for searching recipes.
    """
    query = forms.CharField(label='Recipe Name or Ingredients', max_length=100, required=False)

    def clean(self):
        """
        Clean method for additional form validation.
        """
        cleaned_data = super().clean()
        query = cleaned_data.get('query')

        if not query:
            raise forms.ValidationError({'query': 'Please enter a search query or ingredients.'})

        return cleaned_data
