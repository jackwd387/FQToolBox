import requests
import json
import time
import Ui
cookie = open('./Cookie.ini','r',encoding='utf-8').read()
def book_id_inquire(book_id):
    # url = 'https://novel.snssdk.com/api/novel/book/directory/list/v/?book_id= 被和谐
    url = 'https://api5-normal-sinfonlineb.fqnovel.com/reading/bookapi/multi-detail/v/?aid=1967&iid=1&version_code=999&book_id='
    url1 = 'https://fanqienovel.com/api/reader/directory/detail?bookId='
    # 数据获取
    json_data = json.loads(requests.get(url=url+book_id).text)
    # title获取
    json_data2 = json.loads(requests.get(url=url1+book_id).text)
    title_list = []
    for i in json_data2['data']['chapterListWithVolume']:
        for v in i:
            title_list.append(v['title'])
    # item_id获取
    item_id_list = json_data2['data']['allItemIds']
    for i in range(len(item_id_list)):
        print('title:'+title_list[i])
        print('item_id:'+item_id_list[i])
    print('书名:'+json_data['data'][0]['book_name'])
    print('作者:'+json_data['data'][0]['author'])
    print('描述:'+json_data['data'][0]['abstract'])
    print('类型:'+json_data['data'][0]['tags'])
def item_id_inquire(item_id):
    # url = 'https://novel.snssdk.com/api/novel/book/directory/detail/v/?item_ids='
    url1 = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id=' #备用API
    json_data3 = json.loads(requests.get(url=url1+item_id).text)
    Ui.view_text('item_id对应内容:'+json_data3['data']['content'].replace('</p><p>','\n').replace('</p>','\n').replace('<p>','\n'))
    print('item_id对应作者:'+json_data3['data']['novel_data']['author'])
    print('item_id对应book_id:'+json_data3['data']['novel_data']['book_id'])
    print('item_id对应书名:'+json_data3['data']['novel_data']['book_name'])
    print('item_id对应章节名:'+json_data3['data']['novel_data']['title'])
    print('item_id对应下一章item_id:'+json_data3['data']['novel_data']['next_item_id'])
    print('item_id对应上一章item_id:'+json_data3['data']['novel_data']['pre_item_id'])
def user_inquire(cookie):
    url = 'https://api5-normal-sinfonlineb.fqnovel.com/reading/bookapi/multi-detail/v/?aid=1967&iid=1&version_code=999&book_id='
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
        json_data = json.loads(requests.get(url=url+i['book_id']).text)
        print('书名:'+json_data['data'][0]['book_name'])
        print('作者:'+json_data['data'][0]['author'])
        print('类型:'+json_data['data'][0]['tags'])
        print('---------------')
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
    else:
        break
