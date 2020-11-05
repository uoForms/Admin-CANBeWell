from django.shortcuts import render
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
    context = {
        'page_title': 'LinkChecker Output'
    }
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
    #Folder name of urls
    file = open('linkchecker/test.txt')
    lines = file.readlines()
    aa=[]
    for line in lines:
        temp=line.replace('\n','')
        aa.append(temp)
    print(f'\033[31m"start testing"\033[0m')
    results = []
    for a in aa:
        tempUrl = a
        try :
            opener.open(tempUrl)
            results.append(tempUrl + ' >>> PASS')
            print(f'\033[34m{tempUrl + "  Pass"}\033[0m')
        except urllib.error.HTTPError:
            results.append(tempUrl + ' >>> HttpError')
            print(f'\033[33m{tempUrl+ "  HttpError"}\033[0m') #yellow
            time.sleep(0.01)
        except urllib.error.URLError:
            results.append(tempUrl + ' >>> URLError')
            print(f'\033[35m{tempUrl + "  URLError"}\033[0m') #purple
            time.sleep(0.01)
        time.sleep(0.01)
    
    data = output
    print (data)
    # data = data()
    return render(request,'linkchecker/output.html', {'data': data, 'results': results})
