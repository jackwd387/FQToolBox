import requests
import json
import time
cookie = open('./Cookie.ini','r',encoding='utf-8').read()
def book_id_inquire(book_id):
    url = 'https://fanqienovel.com/api/reader/directory/detail?bookId='
    url1 = 'https://fanqienovel.com/api/reader/full?itemId='
    # 数据获取
    json_data = json.loads(requests.get(url=url+book_id).text)
    # item_id获取
    item_id_list = json_data['data']['allItemIds']
    # 书名获取
    json_data2 = json.loads(requests.get(url=url1+item_id_list[0]).text)
    name = json_data2['data']['chapterData']['bookName']
    print('书名:'+name)
    # title获取
    title_list = []
    for i in json_data['data']['chapterListWithVolume']:
        for v in i:
            title_list.append(v['title'])
    for i in range(len(item_id_list)):
        print('title:'+title_list[i])
        print('item_id:'+item_id_list[i])
def item_id_inquire(item_id):
    url1 = 'https://fanqienovel.com/api/reader/full?itemId='
    json_data3 = json.loads(requests.get(url=url1+item_id).text)
    item_id_corresponds_to_author = json_data3['data']['chapterData']['author']
    item_id_corresponds_to_book_id = json_data3['data']['chapterData']['bookId']
    item_id_corresponds_to_book_name = json_data3['data']['chapterData']['bookName']
    item_id_corresponds_to_title = json_data3['data']['chapterData']['title']
    item_id_corresponds_to_firstPassTime = json_data3['data']['chapterData']['firstPassTime']
    item_id_corresponds_to_next_item_id = json_data3['data']['chapterData']['nextItemId']
    item_id_corresponds_to_pre_item_id = json_data3['data']['chapterData']['preItemId']
    print('item_id对应作者:'+item_id_corresponds_to_author)
    print('item_id对应book_id:'+item_id_corresponds_to_book_id)
    print('item_id对应书名:'+item_id_corresponds_to_book_name)
    print('item_id对应章节名:'+item_id_corresponds_to_title)
    print('item_id对应发布时间:'+item_id_corresponds_to_firstPassTime)
    print('item_id对应下一章item_id:'+item_id_corresponds_to_next_item_id)
    print('item_id对应上一章item_id:'+item_id_corresponds_to_pre_item_id)
def user_inquire(cookie):
    url2 = 'https://fanqienovel.com/api/user/info/v2'
    url3 = 'https://fanqienovel.com/api/reader/book/progress'
    headers = {
    'Cookie': cookie
    }
    json_data4 = json.loads(requests.get(url=url2,headers=headers).text)
    User_avatar_url = json_data4['data']['avatar']
    User_name = json_data4['data']['name']
    User_id = json_data4['data']['id']
    User_desc = json_data4['data']['desc']
    print('用户头像url:'+User_avatar_url)
    print('用户名称:'+User_name)
    print('用户id:'+User_id)
    print('用户简介:'+User_desc)
    json_data5 = json.loads(requests.get(url=url3,headers=headers).text)
    for i in json_data5['data']:
        print('用户书架书籍:'+i['book_id'])
        print('此用户在此书最后一次阅读的章节:'+i['item_id'])
        print('此用户在此书最后一次阅读的时间:'+i['read_timestamp'])
def update_progres(cookie,item_id):
    url = 'https://fanqienovel.com/api/reader/book/update_progress'
    url1 = 'https://fanqienovel.com/api/reader/full?itemId='
    json_data3 = json.loads(requests.get(url=url1+item_id).text)
    book_id = json_data3['data']['chapterData']['bookId']
    headers = {
    'Cookie': cookie
    }
    update_data = {"book_id":book_id,"item_id":item_id,"read_progress":0,"index":4,"read_timestamp":int(time.time()),"genre_type":0}
    data = requests.post(url=url,headers=headers,json=update_data).text
    print(data)
while True:
    c = input('FQAPI TEST\n1.查询book_id\n2.查询item_id\n3.查询用户\n4.上传阅读进度\n5.退出\n请选择:')
    if c == '1':
        book_id_inquire(input('book_id:'))
    elif c == '2':
        item_id_inquire(input('item_id:'))
    elif c == '3':
        user_inquire(cookie)
    elif c == '4':
        update_progres(cookie,input('item_id:'))
    elif c == '5':
        break
