from django.shortcuts import render

# Create your views here.

def visualization(request):
    context = {
        'page_title': 'Data Visualization'
    }
    return render(request, 'visualization/index.html', context)