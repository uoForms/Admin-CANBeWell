from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login(request):
    return render(request, 'users/login.html')

def logout(request):
    return render(request, 'users/logout.html')

def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})