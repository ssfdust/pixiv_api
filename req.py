import requests
import json
from hyper.contrib import HTTP20Adapter
import re

class GetKeyValue(object):
    def __init__(self):
        self._value = None

    def get_key_value(self, data, key_w):
        '''
        to quick find the data by key
        O(1)?
        '''
        if isinstance(data, dict):
            for key,value in data.items():
                if key != key_w:
                    self.get_key_value(value, key_w)
                else:
                    self._value = value
        elif isinstance(data, list):
            for item in data:
                self.get_key_value(item, key_w)

    def get_value(self):
        return self._value

class GetImgUrls(object):
    def __init__(self):
        self.url_list = list()

    def get_img_urls(self, img_json):
        if 'illusts' in img_json:
            self.collect_urls(img_json['illusts'])
        if 'ranking_illusts' in img_json:
            self.collect_urls(img_json['ranking_illusts'])
        if 'next_url' in img_json:
            if img_json['next_url'] == None:
                return True
            return img_json['next_url']

    def collect_urls(self, data):
        if isinstance(data, dict):
            for key,value in data.items():
                self.collect_urls(value)
        elif isinstance(data, list):
            for item in data:
                self.collect_urls(item)
        elif isinstance(data, str):
            if re.search('img-original', data):
                self.url_list.append(data)

login_req = requests.Session()
pic_req = requests.Session()
headers = {":authority": "i.pximg.net"}
oauth_url = 'https://oauth.secure.pixiv.net/auth/token'
bookmark_url = 'https://app-api.pixiv.net/v1/user/bookmarks/illust?user_id=#userid#&restrict=public'
recommend_url = 'https://app-api.pixiv.net/v1/illust/recommended?filter=for_android&include_ranking_illusts=true'
oauth_headers = {
    'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800',
    'Content-Type': 'application/x-www-form-urlencoded'
}
req_headers = {
    'Authorization': 'Bearer ',
    'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800',
    'Content-Type': 'application/x-www-form-urlencoded'
}
img_headers = {
    ':authority': 'i.pximg.net',
    'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800',
    'referer': 'https://app-api.pixiv.net/'
}
login_data = {
    'client_id': 'MOBrBDS8blbauoSck0ZfDbtuzpyT',
    'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj',
    'grant_type': 'password',
    'username': None,
    'password': None,
    'device_token': '56901eb1e65c826ab4b9ae598c2d0852', #genrated by random md5
    'get_secure_url': 'true'
}

#Login Method
print('Please enter your login username:')
login_data['username'] = input()
print('Please enter your login password:')
login_data['password'] = input()
print('what pictures do you want to download?\n1 for bookmarked 2 for recomended')
want = input()

keyvalue_handle = GetKeyValue()
login_res = login_req.post(oauth_url, headers=oauth_headers, data=login_data)
login_json = json.loads(login_res.text)
keyvalue_handle.get_key_value(login_json, 'access_token')
access_token = keyvalue_handle.get_value()
keyvalue_handle.get_key_value(login_json, 'id')
user_id = keyvalue_handle.get_value()

#set access_token
req_headers['Authorization'] += access_token

#get bookmarked pictures
if want == '1':
    pic_res = pic_req.get(bookmark_url.replace('#userid#', user_id), headers=req_headers)
elif want == '2':
    pic_res = pic_req.get(recommend_url, headers=req_headers)
pic_res_json = json.loads(pic_res.text)
img_handler = GetImgUrls()

#here we have got at most 30 pictures
next_url = img_handler.get_img_urls(pic_res_json)
for i in range(0,2):
    #Only get 90 pictures at most
    if next_url == True:
        break
    print('next_url:' + next_url)
    pic_res = pic_req.get(next_url, headers=req_headers)
    print(pic_res.status_code)
    pic_res_json = json.loads(pic_res.text)
    next_url = img_handler.get_img_urls(pic_res_json)

img_req = requests.Session()
img_req.mount('https://i.pximg.net', HTTP20Adapter())
length = len(img_handler.url_list)
for cont, img_url in enumerate(img_handler.url_list):
    img_res = img_req.get(img_url, headers=img_headers)
    filename = str(cont + 1) + '.jpg'
    print('%d/%d' % (cont + 1, length))
    if img_res.status_code == 200:
        with open(filename, 'wb+') as f:
            img_res.raw.decode_content = True
            f.write(img_res.content)
            f.close()
