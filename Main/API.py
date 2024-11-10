import requests
import json
import time

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
    print('评分:'+json_data['data'][0]['score'])
    if json_data['data'][0]['creation_status'] == '0':
        print('状态:完结')
    elif json_data['data'][0]['creation_status'] == '1':
        print('状态:连载')
    elif json_data['data'][0]['creation_status'] == '4':
        print('状态:断更')
    else:
        print('状态:'+json_data['data'][0]['creation_status'])
    print('sub_info:'+json_data['data'][0]['sub_info'])
    return item_id_list,title_list,json_data['data'][0]['book_name']

def item_id_inquire(item_id):
    # url = 'https://novel.snssdk.com/api/novel/book/directory/detail/v/?item_ids='
    # url1 = 'https://api5-normal-sinfonlinec.fqnovel.com/reading/bookapi/detail/v/?book_id=7421167583522458648&iid=3956468249796948&aid=1967&version_code=513' headers = {"X-Argus":"TEq3zqiMiX8Tauf+Y9nvEiUBYmWyYJ7izG4CQ/ro7zgkJ9f+Zkot7BSehMqcBNyUGyV6JP7a0AMO9AXFr+ypIoBtmkAzSIKHgMgZtsSS/aaAbQbn3v/cHzoaeTDSs4zdHg/T605YGbFmX7wADPS+OflnI0H/f4nLFOMb1Y/ZUED2JW6pe1haPwyHFKnPO0sE8fe+fEXJLA2uxnGdioqrYAauQ9V+lVkMxORWgEwvxAW2UZPOsh6ypDG/hrFc6vX0uZ9stlzQR3upKKgu+msT8hfF"} 备用
    url1 = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id=' #备用API
    json_data3 = json.loads(requests.get(url=url1+item_id).text)
    content = json_data3['data']['content'].replace('</p><p>','\n').replace('</p>','\n').replace('<p>','\n')
    title = json_data3['data']['novel_data']['title']
    print('item_id对应内容:'+ content)
    print('item_id对应作者:'+json_data3['data']['novel_data']['author'])
    print('item_id对应book_id:'+json_data3['data']['novel_data']['book_id'])
    print('item_id对应书名:'+json_data3['data']['novel_data']['book_name'])
    print('item_id对应章节名:'+ title)
    print('item_id对应下一章item_id:'+json_data3['data']['novel_data']['next_item_id'])
    print('item_id对应上一章item_id:'+json_data3['data']['novel_data']['pre_item_id'])
    return content,title

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
        User_desc = json_data4['data']['desc']
        print('用户头像url:'+User_avatar_url)
        print('用户名称:'+User_name)
        print('用户id:'+User_id)
        print('用户简介:'+User_desc)

def user_bookshelf(cookie):
    url3 = 'https://fanqienovel.com/api/reader/book/progress'
    url = 'https://api5-normal-sinfonlineb.fqnovel.com/reading/bookapi/multi-detail/v/?aid=1967&iid=1&version_code=999&book_id='
    headers = {
    'Cookie': cookie
    }
    book_id_list = []
    json_data5 = json.loads(requests.get(url=url3,headers=headers).text)
    for i in json_data5['data']:
        print('用户书架书籍:'+i['book_id'])
        book_id_list.append(i['book_id'])
        print('此用户在此书最后一次阅读的章节:'+i['item_id'])
        print('此用户在此书最后一次阅读的时间:'+i['read_timestamp'])
        print('---------------')
    return book_id_list

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
    print('以下是段评内容')
    for i in res:
        print('\n')
        print(i['user_info']['user_name']+':'+i['text'])

def book_comments(book_id):
    url = f"https://api5-normal-sinfonlinec.fqnovel.com/reading/ugc/novel_comment/book/v/?&book_id={book_id}&aid=1967&version_code=513"
    headers = {
    "X-Argus": "2DhmtvR3uHS92+jiPSDiYpHKrADwLYuLOuGVmZZGzZQeFwLkCbSb+J3TLiIwUlbaKG6NMydM7LCm5EwzMmK0sJSQh2uoxdwTXSpOSk0U+na16DbbxUaHw0N+ylcp81dhOSfGd4foaifno6KBCahJtNKb0OpMYqpvguhVlXDhKdGPr21vBEcv63xMzvXJTwsxDb/9gaDl1cDEZWqK2Pl3xmabBKQb+koFFZeD01LY0YSmLKJuHHOEdAvQj1Mz2nUiSiKTyk8TivHxlS+3AdQWp3GG"
    }
    res = json.loads(requests.get(url,headers=headers).text)['data']['comment']
    for i in res:
        print('\n')
        print(i['user_info']['user_name']+':'+i['text'])
