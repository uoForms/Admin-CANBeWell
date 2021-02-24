from django.shortcuts import render
from django.http import JsonResponse
import re
import urllib.request
import time
import json
from django.http import HttpResponse

# Don't change the key of files, the name and path could be changed.
files = {"en_topic":"linkchecker/Topic-EN.json",
         "fr_topic":"linkchecker/Topic-FR.json",
         "en_test":"linkchecker/Test-EN.json",
         "fr_test":"linkchecker/Test-FR.json"}

# Don't change the key of fileType, the name and path could be changed.
fileType = {"en_topic":"Topic-EN",
         "fr_topic":"Topic-FR",
         "en_test":"Test-EN",
         "fr_test":"Test-FR"}

def linkchecker(request):
    context = {
        'page_title': 'LinkChecker'
    }
    for key in files:
        urls = resolveUrlInFile(key)
        context.update({key:len(urls)})
    return render(request, 'linkchecker/index.html', context)


def output(request, fileKey):
    urls = resolveUrlInFile(fileKey)
    print(f'\033[31m"start testing"\033[0m')
    # data = data()
    return render(request, 'linkchecker/output.html', {'total': len(urls), 'urls':urls, 'fileType': fileType[fileKey]})

def output_item(request,fileKey, idx):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
    urls = resolveUrlInFile(fileKey)
    index = int(idx) - 1
    if index >= len(urls):
        return JsonResponse({'index':idx, 'result': ''})

    tempUrl = urls[index]
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
    return JsonResponse({'index':idx, 'result': results})

# private function
def  resolveUrlInFile(fileKey):
    file = open(files[fileKey], mode='r', encoding='UTF-8')
    js = json.load(file)
    jsonKey = ''
    if fileKey == 'en_test' or fileKey == 'fr_test':
        jsonKey = 'Patient/Provider Text'
    elif fileKey == 'fr_topic' or fileKey == 'en_topic':
        jsonKey = 'General Patient Text'
    else:
        return []
    urls = []
    for i in range(len(js)):
        txt = js[i][jsonKey]
        url = re.findall('https://.*]$', txt)
        for u in url:
            u = u.replace(']]','')
            urls .append(u)

        url = re.findall('http://.*]$', txt)
        for u in url:
            u = u.replace(']]','')
            urls.append(u)
    return urls
