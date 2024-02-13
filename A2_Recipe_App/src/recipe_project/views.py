from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserRegistrationForm
from django.contrib import messages

#define a function view called login_view that takes a request from user
def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f'Username: {username}')
            print(f'Password: {password}')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                print('User is authenticated')
                login(request, user)
                return redirect('recipes:home')
            else:
                print('Authentication failed')

        else:
            error_message = 'Oops... something went wrong'
            print(f'Form errors: {form.errors}')

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)

#define a function view called logout_view that takes a request from user
def logout_view(request):                                  
   logout(request)             #the use pre-defined Django function to logout
   return render(request, 'recipes/success.html', {'message': 'You\'ve successfully logged out.'})

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Assuming you want to confirm the deletion with a checkbox
        confirmation_checkbox = request.POST.get('confirm_delete', False)

        if confirmation_checkbox:
            # Perform account deletion logic
            request.user.delete()

            # Log the user out after deletion
            logout(request)

            # Redirect to a confirmation page or home page
            return redirect('home')

    return render(request, 'delete_account.html')

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
            return redirect(reverse('recipes:home')) 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            print('Form is not valid. Errors:', form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/signup.html', {'form': form})

