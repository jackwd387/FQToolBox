import requests
import json
import time

def book_id_inquire(book_id):
    # url = 'https://novel.snssdk.com/api/novel/book/directory/list/v/?book_id= 被和谐
    url2 = f'https://api5-normal-sinfonlinec.fqnovel.com/reading/user/share/info/v/?group_id={book_id}&aid=1967&version_code=513'
    url = f'https://api5-normal-sinfonlineb.fqnovel.com/reading/bookapi/multi-detail/v/?aid=1967&iid=1&version_code=999&book_id={book_id}'
    url1 = 'https://fanqienovel.com/api/reader/directory/detail?bookId='
    # 数据获取
    json_data = json.loads(requests.get(url=url).text)
    # title获取
    json_data2 = json.loads(requests.get(url=url1+book_id).text)
    title_list = []
    for i in json_data2['data']['chapterListWithVolume']:
        for v in i:
            title_list.append(v['title'])
    item_id_list = json_data2['data']['allItemIds']
    book_name = json_data['data'][0]['book_name']
    author = json_data['data'][0]['author']
    abstract = json_data['data'][0]['abstract']
    tags = json_data['data'][0]['tags']
    score = json_data['data'][0]['score']
    word_number = json_data['data'][0]['word_number']
    read_count = json_data['data'][0]['read_count']
    creation_status = json_data['data'][0]['creation_status'] #0:完结 1:连载 4:断更
    thumb_url = json_data['data'][0]['thumb_url']
    if json.loads(requests.get(url=url2).text)['code'] == 100109:
        is_ban = True
    else:
        is_ban = False
    return item_id_list,title_list,book_name,author,abstract,tags,score,word_number,read_count,creation_status,thumb_url,is_ban

def item_id_inquire(item_id):
    # url = 'https://novel.snssdk.com/api/novel/book/directory/detail/v/?item_ids='
    # url1 = 'https://api5-normal-sinfonlinec.fqnovel.com/reading/bookapi/detail/v/?book_id=7421167583522458648&iid=3956468249796948&aid=1967&version_code=513' headers = {"X-Argus":"TEq3zqiMiX8Tauf+Y9nvEiUBYmWyYJ7izG4CQ/ro7zgkJ9f+Zkot7BSehMqcBNyUGyV6JP7a0AMO9AXFr+ypIoBtmkAzSIKHgMgZtsSS/aaAbQbn3v/cHzoaeTDSs4zdHg/T605YGbFmX7wADPS+OflnI0H/f4nLFOMb1Y/ZUED2JW6pe1haPwyHFKnPO0sE8fe+fEXJLA2uxnGdioqrYAauQ9V+lVkMxORWgEwvxAW2UZPOsh6ypDG/hrFc6vX0uZ9stlzQR3upKKgu+msT8hfF"} 备用
    url1 = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id=' #备用API
    json_data3 = json.loads(requests.get(url=url1+item_id).text)
    content = json_data3['data']['content']
    title = json_data3['data']['novel_data']['title']
    author = json_data3['data']['novel_data']['author']
    book_id = json_data3['data']['novel_data']['book_id']
    book_name = json_data3['data']['novel_data']['book_name']
    next_item_id = json_data3['data']['novel_data']['next_item_id']
    pre_item_id = json_data3['data']['novel_data']['pre_item_id']
    return content,title,author,book_id,book_name,next_item_id,pre_item_id

def user_inquire(cookie):
    url2 = 'https://fanqienovel.com/api/user/info/v2'
    headers = {
    'Cookie': cookie
    }
    json_data4 = json.loads(requests.get(url=url2,headers=headers).text)
    if json_data4['code'] == -1:
        return 'false'
    else:
        User_avatar_url = json_data4['data']['avatar']
        User_name = json_data4['data']['name']
        User_id = json_data4['data']['id']
        if 'desc' in json_data4['data']:
            User_desc = json_data4['data']['desc']
        else:
            User_desc = ''
        return User_name,User_avatar_url,User_id,User_desc

def user_bookshelf(cookie):
    url3 = 'https://fanqienovel.com/api/reader/book/progress'
    # url = 'https://api5-normal-sinfonlineb.fqnovel.com/reading/bookapi/multi-detail/v/?aid=1967&iid=1&version_code=999&book_id=' 
    headers = {
    'Cookie': cookie
    }
    book_id_list = []
    item_id_list = []
    read_timestamp_list = []
    json_data5 = json.loads(requests.get(url=url3,headers=headers).text)
    for i in json_data5['data']:
        book_id_list.append(i['book_id'])
        item_id_list.append(i['item_id'])
        read_timestamp_list.append(i['read_timestamp'])
    return book_id_list,item_id_list,read_timestamp_list

def update_progres(cookie,item_id):
    url = 'https://fanqienovel.com/api/reader/book/update_progress'
    url1 = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id='
    json_data3 = json.loads(requests.get(url=url1+item_id).text)
    book_id = json_data3['data']['novel_data']['book_id']
    headers = {
    'Cookie': cookie
    }
    update_data = {"book_id":book_id,"item_id":item_id,"read_progress":0,"index":4,"read_timestamp":int(time.time()),"genre_type":0}
    data = requests.post(url=url,headers=headers,json=update_data).text
    print(data)

def add_bookshelf(cookie,book_id):
    url = 'https://fanqienovel.com/api/book/simple/info'
    url3 = 'https://fanqienovel.com/api/reader/book/progress'
    headers = {
    'Cookie': cookie
    }
    item_ids = []
    for i in json.loads(requests.get(url=url3,headers=headers).text)['data']:
        item_ids.append(i['book_id'])
    item_ids.append(book_id)
    data = {"book_ids":item_ids}
    print(json.loads(requests.post(url=url,headers=headers,data=data).text))

def paragraph_comments(item_id,count):
    url1 = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id='
    json_data3 = json.loads(requests.get(url=url1+str(item_id)).text)
    book_id = json_data3['data']['novel_data']['book_id']
    url = f"https://api5-normal-sinfonlinec.fqnovel.com/reading/ugc/idea/comment_list/v/?item_version=3add812e2984c508c71ce1361c31cf5f_1_v5&item_id={item_id}&para_index={count}&book_id={book_id}&aid=1967&version_code=513"
    res = json.loads(requests.get(url).text)['data']['comments']
    dic = {}
    for i in res:
        dic[i['user_info']['user_name']] = i['text']
    return dic

def book_comments(book_id):
    url = f"https://api5-normal-sinfonlinec.fqnovel.com/reading/ugc/novel_comment/book/v/?&book_id={book_id}&aid=1967&version_code=513"
    headers = {
    "X-Argus": "2DhmtvR3uHS92+jiPSDiYpHKrADwLYuLOuGVmZZGzZQeFwLkCbSb+J3TLiIwUlbaKG6NMydM7LCm5EwzMmK0sJSQh2uoxdwTXSpOSk0U+na16DbbxUaHw0N+ylcp81dhOSfGd4foaifno6KBCahJtNKb0OpMYqpvguhVlXDhKdGPr21vBEcv63xMzvXJTwsxDb/9gaDl1cDEZWqK2Pl3xmabBKQb+koFFZeD01LY0YSmLKJuHHOEdAvQj1Mz2nUiSiKTyk8TivHxlS+3AdQWp3GG"
    }
    res = json.loads(requests.get(url,headers=headers).text)['data']['comment']
    dic = {}
    for i in res:
        dic[i['user_info']['user_name']] = i['text']
    return dic

def recommended_list():
    url = "https://api5-normal-sinfonlinec.fqnovel.com/reading/bookapi/bookmall/tab/v/?aid=1967"
    data = json.loads(requests.get(url).text)['data']['tab_item'][0]['cell_data'][0]['cell_data'][0]['book_data']
    data_list = []
    for r in data:
        dic = {}
        dic['book_id'] = r['book_id']
        dic['book_name'] = r['book_name']
        dic['abstract'] = r['abstract']
        dic['author'] = r['author']
        dic['create_time'] = r['create_time']
        dic['read_count'] = r['read_count']
        dic['score'] = r['score']
        data_list.append(dic)
    return data_list
def user_id_inquire(user_id):
    url = f"https://api5-normal-sinfonlinec.fqnovel.com/reading/user/basic_info/get/v?user_id={user_id}&aid=1967&version_code=65532"
    data = json.loads(requests.get(url).text)
    user_name = data['data']['user_name']
    user_avatar = data['data']['user_avatar']
    is_author = data['data']['is_author']
    description = data['data']['description']
    read_book_time = data['data']['read_book_time']
    read_book_num = data['data']['read_book_num']
    recv_digg_num = data['data']['recv_digg_num']
    fans_num = data['data']['fans_num']
    follow_user_num = data['data']['follow_user_num']
    author_book_list = []
    if is_author == True:
        for i in data['data']['author_book_info']:
            author_book_list.append(i['book_id'])
    return user_name,user_avatar,is_author,description,read_book_time,read_book_num,recv_digg_num,fans_num,follow_user_num,author_book_list
    
def video_get(video_id):
    url = "https://api5-normal-sinfonlinec.fqnovel.com/novel/player/video_model/v1/?aid=1967"
    data = {"biz_param":{"device_level":1,"from_video_id":"","need_all_video_definition":True,"need_mp4_align":False,"source":4,"use_os_player":False,"video_id_type":0,"video_platform":3},"video_id":video_id}

    data = json.loads(requests.post(url, data=data).text)
    return data['data']['main_url'],data['data']['backup_url']

def reading(tone_id,item_ids):
  url = f"https://reading.snssdk.com/reading/reader/audio/playinfo/?tone_id={tone_id}&item_ids={item_ids}&aid=507386&version_code=999"
  data = json.loads(requests.get(url=url).text)["data"][0]
  return data["main_url"],data["backup_url"]