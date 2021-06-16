from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import re
import urllib.request
import time
import json
from django.http import HttpResponse
import requests
import json

URL_Topic_EN = "https://drive.google.com/uc?export=download&id=1KmTemPnVDmXcxMKrJ48y0jAoG5MYl58f"
URL_Topic_FR = "https://drive.google.com/uc?export=download&id=1lru1LitepXYPCvdovo11xz8s7MdZhBzI"
URL_Test_FR = "https://drive.google.com/uc?export=download&id=1iapSdfbUYnUDn6nrDavN536rey-1tiBD"
URL_Test_EN = "https://drive.google.com/uc?export=download&id=1eNwhPOhb9koID2G_c53O7yu3iQ2pJJZR"

URL = [URL_Topic_EN,URL_Topic_FR,URL_Test_EN,URL_Test_FR]
folder_loc = ['linkchecker/Topic-EN.json','linkchecker/Topic-FR.json','linkchecker/Test-EN.json','linkchecker/Test-FR.json']

def json_write(url_name, loc): # function to populate the link checker with the latest json files
    for i in range(0,4):
        resp = requests.get(url = url_name[i]).json()

        with open(loc[i],"w") as outfile:
            json.dump(resp, outfile)

json_write(URL,folder_loc)

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
@login_required(login_url='login')
def linkchecker(request):
    context = {
        'page_title': 'LinkChecker'
    }
    for key in files:
        urls = resolveUrlInFile(key)
        context.update({key:len(urls)})
    return render(request, 'linkchecker/index.html', context)

@login_required(login_url='login')
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
        jsonKey = ['General Patient Text','Health Provider Text']
    else:
        return []

    urls = []
    for x in range(len(jsonKey)):
        for i in range(len(js)):
            txt = js[i][jsonKey] if len(jsonKey)==21 else js[i][jsonKey[x]] #length of 'Patient/Provide text' is 21, which needs to be skipped
            txt_split = txt.split('\n')

            for i in txt_split:
                url = re.findall('https://.*]$', i)
                for u in url:
                    u = u.replace(']]','')
                    urls.append(u)

                url = re.findall('http://.*]$', i)
                for u in url:
                    u = u.replace(']]','')
                    urls.append(u)

    return list(set(urls))
