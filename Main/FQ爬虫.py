# 导入数据请求模块
import requests
import _thread
import os
import time
import re
import json
name = ''
title_list = []
item_id_list = []
url = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id='
def get_item_id(book_id):
    global name,title_list,item_id_list
    url1 = 'https://fanqienovel.com/api/reader/directory/detail?bookId='+book_id
    # 发送请求
    json_data = json.loads(requests.get(url=url1).text)
    """解析数据: 提取我们需要的数据内容"""
    # 提取章节名
    for i in json_data['data']['chapterListWithVolume']:
        for v in i:
            title_list.append(v['title'])
    # 提取章节ID
    item_id_list = json_data['data']['allItemIds']
    # 提取书名
    json_data2 = json.loads(requests.get(url=url+item_id_list[0]).text)
    name = json_data2['data']['novel_data']['book_name']
    print('书名:'+name)
def get_content(title,item_id):
        # 完整的小说章节链接
        link_url = url + item_id
        # 发送请求+获取数据内容
        link_data = json.loads(requests.get(url=link_url).text)
        # 把<p>转 \n 换行符
        data = link_data['data']['content'].replace('<p>','\n').replace('</p>','\n')
        # print(content)
        #print(link_url)
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
        with open('./output/'+ name +'/'+ title + '.txt', mode='w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(data)
            f.write('\n\n')
            f.close
        print(title+'爬取成功')

# 模拟浏览器
headers = {
    # User-Agent 用户代理, 表示浏览器/设备的基本身份信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #cookie
    ,'Cookie': open('cookie.ini','r').read()
    }
# url地址(小说主页)
book_id = input('book_id:')
get_item_id(book_id)
if not os.path.exists(name):
    os.makedirs('./output/'+name)
c = input('1.爬取全文\n2.爬取单章\nNext:')
if c == '1':
    #print(title_list)
    # for循环遍历, 提取列表里元素
    if input('是否全文爬取(这将会爬取书籍的所有章节，若否则将会爬取未被爬取的章节)y/n(默认n):') == 'y':
        for title,item_id in zip(title_list, item_id_list):
            _thread.start_new_thread(get_content,(title,item_id))
            time.sleep(0.003)
        input('--------------------------------------------\n总章数:'+str(len(title_list))+"\n等待所有线程下载完毕后，按下回车键\n--------------------------------------------\n")
    print('开始效验并更新文件')
    for title,item_id in zip(title_list, item_id_list):
        if os.path.exists('./output/'+ name +'/'+ title + '.txt'):
            print(f"{title}已创建")
        else:
            print(f'提示:{title}没有被创建')
            _thread.start_new_thread(get_content,(title,item_id))
    input('--------------------------------------------\n总章数:'+str(len(title_list))+"\n等待所有线程下载完毕后，按下回车键\n--------------------------------------------\n")
elif c == '2':
    for r in range(len(title_list)):
        print(f'章节 {r+1} :{title_list[r]}')
    c1 = int(input('选择:'))
    get_content(title_list[c1-1],item_id_list[c1-1])
else:
    print('unknown')
