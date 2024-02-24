from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse


from .forms import UserRegistrationForm
import logging

logger = logging.getLogger(__name__)

#test
#define a function view called login_view that takes a request from the user
def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            logger.info(f'Username: {username}')
            logger.info(f'Password: {password}')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                logger.info('User is authenticated')

                # Additional debug logs
                logger.info(f'Request path: {request.path}')
                logger.info(f'Middleware classes: {settings.MIDDLEWARE}')
                logger.info(f'Allowed schemes for HttpResponsePermanentRedirect: {HttpResponsePermanentRedirect.allowed_schemes}')

                login(request, user)
                return redirect('home')  # Use the name of the home URL pattern

            else:
                logger.warning('Authentication failed')

        else:
            error_message = 'Invalid username or password'
            logger.warning(f'Form errors: {form.errors}')

    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)


#define a function view called logout_view that takes a request from the user
def logout_view(request):
    print("Reached logout view")
    try:
        logout(request)
        return render(request, 'recipes/success.html', {'message': 'You\'ve successfully logged out.'})
    except Exception as e:
        messages.error(request, f'An error occurred during logout: {e}')
        return render(request, 'recipes/success.html', {'message': 'Logout unsuccessful. Please try again.'})

@login_required
def delete_account(request):
    if request.method == 'POST':
        confirmation_checkbox = request.POST.get('confirm_delete', False)

        if confirmation_checkbox:
            try:
                # Perform account deletion logic
                request.user.delete()

                # Log the user out after deletion
                logout(request)

                # Add a success message
                messages.success(request, 'Your account was successfully deleted.')

                # Redirect to the login page
                return redirect('login')

            except Exception as e:
                # Add an error message
                messages.error(request, f'An error occurred during account deletion: {e}')

    return render(request, 'auth/delete_account.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipes:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            print(f'Successful registration for {username}')
            return HttpResponseRedirect(reverse('recipes:home'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            print('Form is not valid. Errors:', form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/signup.html', {'form': form})




