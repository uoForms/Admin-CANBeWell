from django.shortcuts import render

# Create your views here.

def login(request):
    context = {
        'page_title': 'Login'
    }

    return render(request, 'users/login.html', context)

def logout(request):
    return render(request, 'users/logout.html')