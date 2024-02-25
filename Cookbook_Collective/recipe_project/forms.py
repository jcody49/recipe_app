from django import forms
from django.contrib.auth.forms import UserCreationForm  
from users.models import User

class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form.

    This form extends the built-in UserCreationForm to include an email field.

    Attributes:
        email (forms.EmailField): Email field for the user's email address.

    Meta:
        model (User): The user model used by the form.
        fields (list): The fields to include in the form, in this case: username, email, password1, password2.
    """
    email = forms.EmailField()

    class Meta:
        """
        Meta class for the UserRegistrationForm.

        Attributes:
            model (User): The user model used by the form.
            fields (list): The fields to include in the form, in this case: username, email, password1, password2.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']
