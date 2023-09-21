from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm
from cryptography.fernet import Fernet
from django.core.exceptions import ValidationError

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def register(request):

    encryption_key = Fernet.generate_key()
    print(encryption_key)  

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Redirect user to home page
                return redirect('home')
            except ValidationError as e:
                form.add_error('ssn', str(e))  # Add the validation error to the form
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_system/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'user_system/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

class Home(TemplateView):
    template_name = 'user_system/home.html'

@login_required
def download_data(request):
    # Get the current user
    user = request.user

    # Retrieve user data from the database
    user_data = CustomUser.objects.filter(pk=user.pk).values()

    # Create a response object with the CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_data.csv"'

    # Create a CSV writer and write data to the response
    writer = csv.DictWriter(response, fieldnames=user_data[0].keys())
    writer.writeheader()
    for data in user_data:
        writer.writerow(data)

    return response

@login_required
def delete_data(request):
    # Get the current user
    user = request.user

    # Delete user data from the database
    user.delete()

    # You may also want to log out the user after deletion
    logout(request)

    # Redirect the user to the home page
    return redirect('home') 