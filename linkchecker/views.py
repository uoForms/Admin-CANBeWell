from django.shortcuts import render

# Create your views here.

def linkchecker(request):
    context = {
        'page_title': 'Link Checker'
    }
    return render(request, 'linkchecker/index.html', context)