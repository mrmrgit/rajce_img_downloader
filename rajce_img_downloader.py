#!/usr/bin/env python
'''
This thing might not work when http://www.rajce.idnes.cz/ changes its html code
or redirection after login (I suppose)
'''
import os
import urllib2 
import urllib
import cookielib
import requests #http://docs.python-requests.org/en/latest/

print('\n######## Album downloader http://www.rajce.idnes.cz/ #############\n')

login_url = raw_input('Enter URL of the album you want to download: ')
album     = raw_input('Enter name of the album: ') 
user_name = raw_input('Enter user name (if the album is not password protected press ENTER): ')
password  = raw_input('Enter password (if the album is not password protected press ENTER): ')

if not os.path.exists(album): os.makedirs(album) #create folder where to put the images 

acc_pwd = {'login': user_name,
           'password': password,
           }
## login
jar = cookielib.CookieJar()
r = requests.get(login_url, cookies=jar)
r = requests.post(login_url, cookies=jar, data=acc_pwd)

## get html with image urls
html = r.text

## test if it loads OK
print('load:')
start_photoList_i = html.find('id="photoList"')    ## this is weakness
end_photoList_i = html.find('id="clearFloatLine"') ## and also this
print('start index: %i' %start_photoList_i)
print('end index: %i' %end_photoList_i)
print('---------')


## img_urls = []   #uncomment if you want to save the image urls
it=0
img_i = start_photoList_i #we start looking where "photoList" begins
while not img_i == -1:
    img_i = html.find('href',img_i+4) #we look for urls
    if img_i > end_photoList_i: break # and we break when we get to the end of "photoList"

    ## separation of the image url
    img_url_start_i = html.find('"',img_i)
    img_url_stop_i  = html.find('"',img_url_start_i+1)

    img_url = html[img_url_start_i+1:img_url_stop_i]
    ## img_urls.append(img_url)  #uncomment if you want to save the image urls
    it+=1
    ext = img_url.split('.')[-1] #get image extension (.jpg, .png, ...)
    pth = os.path.join(album, '%i.%s'%(it,ext))
    urllib.urlretrieve(img_url, pth) #download image and save it as iteration_number.extension
    
print('iterations: %i'%it)

## uncomment following block if you want to save the image urls
##data_file = open('img_urls.txt','w')
##for img_url in img_urls:
##    data_file.write(img_url)
##    data_file.write('\n')
##data_file.close()

## uncomment following block if you want to save the page html
##f = open('rajce.html','w')
##f.write(html.encode('utf8'))
##f.close()
