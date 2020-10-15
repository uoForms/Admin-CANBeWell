import urllib.request
import time
 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
#Folder name of urls
file = open('test.txt')
lines = file.readlines()
aa=[]
for line in lines:
	temp=line.replace('\n','')
	aa.append(temp)
print(aa)
 
print(f'\033[31m"start testing"\033[0m')
for a in aa:
	tempUrl = a
	try :
		opener.open(tempUrl)
		print(f'\033[34m{tempUrl + "  Pass"}\033[0m')
	except urllib.error.HTTPError:
		print(f'\033[33m{tempUrl+ "  HttpError"}\033[0m') #yellow
		time.sleep(2)
	except urllib.error.URLError:
		print(f'\033[35m{tempUrl + "  URLError"}\033[0m') #purple
		time.sleep(2)
	time.sleep(0.1)
