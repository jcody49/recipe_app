#test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.urls import reverse
from .forms import UserRegistrationForm
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    """
    View function for user login.

    Handles user authentication using the provided credentials.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Use the name of the home URL pattern

            else:
                error_message = 'Invalid username or password'

        else:
            error_message = 'Invalid username or password'

    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context, status=401)


def logout_view(request):
    """
    View function for user logout.

    Logs out the currently authenticated user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    try:
        logout(request)
        return render(request, 'recipes/success.html', {'message': 'You\'ve successfully logged out.'})
    except Exception as e:
        messages.error(request, f'An error occurred during logout: {e}')
        return render(request, 'recipes/success.html', {'message': 'Logout unsuccessful. Please try again.'})


@login_required
def delete_account(request):
    """
    View function for deleting a user account.

    Requires authentication. Deletes the authenticated user's account.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    if request.method == 'POST':
        confirmation_checkbox = request.POST.get('confirm_delete') == 'on'

        if confirmation_checkbox:
            try:
                # Perform account deletion logic
                request.user.delete()

                # Log the user out after deletion
                logout(request)

                # Add a success message
                messages.success(request, 'Your account was successfully deleted.')

                return redirect('login')

            except Exception as e:
                # Add an error message
                messages.error(request, f'An error occurred during account deletion: {e}')

    return render(request, 'auth/delete_account.html')


def signup(request):
    """
    View function for user registration.

    Handles user registration using the provided form data.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return HttpResponseRedirect(reverse('recipes:home'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = UserRegistrationForm()

    return render(request, 'auth/signup.html', {'form': form})


def placeholder_view(request):
    """
    Placeholder view for Sphinx-generated documentation.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    return HttpResponse("This is a placeholder for Sphinx-generated documentation.")
