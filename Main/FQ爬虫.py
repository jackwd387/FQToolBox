# 导入数据请求模块
import requests
import _thread
import os
import time
import re
import json
from API import book_id_inquire,item_id_inquire


def get_content(title,item_id):
        data = item_id_inquire(item_id)
        title = data[1]
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
        with open('./output/'+ name +'/'+ title + '.txt', mode='w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(data[0])
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
data = book_id_inquire(book_id)
item_id_list = data[0]
title_list = data[1]
name = data[2]
if not os.path.exists('./output/'+name):
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
