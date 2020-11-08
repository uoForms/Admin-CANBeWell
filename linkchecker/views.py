from django.shortcuts import render
from django.http import JsonResponse
import os
import urllib.request
import time
from django.http import HttpResponse


def linkchecker(request):
    context = {
        'page_title': 'LinkChecker'
    }
    return render(request, 'linkchecker/index.html', context)


def output(request):
    # Folder name of urls
    file = open('linkchecker/test.txt')
    lines = file.readlines()
    print(f'\033[31m"start testing"\033[0m')
    # data = data()
    return render(request, 'linkchecker/output.html', {'total': len(lines), 'urls': lines})


def output_item(request, idx):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
    # Folder name of urls
    file = open('linkchecker/test.txt')
    lines = file.readlines()
    index = int(idx) - 1
    if index >= len(lines):
        return JsonResponse({'index': idx, 'result': ''})

    tempUrl = lines[index]
    try:
        opener.open(tempUrl)
        results = 'PASS'
        print(f'\033[34m{tempUrl + "  Pass"}\033[0m')
    except urllib.error.HTTPError:
        results = 'HttpError'
        print(f'\033[33m{tempUrl + "  HttpError"}\033[0m')  # yellow
        time.sleep(0.01)
    except urllib.error.URLError:
        results = 'URLError'
        print(f'\033[35m{tempUrl + "  URLError"}\033[0m')  # purple
        time.sleep(0.01)
    return JsonResponse({'index': idx, 'result': results})
