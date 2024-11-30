import threading
import os
from tqdm import tqdm
import re
from API import book_id_inquire,item_id_inquire

def get_content(title,item_id):
        data = item_id_inquire(item_id)
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
        with open('./output/'+ name +'/'+ title + '.txt', mode='w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(data[0])
            f.write('\n\n')
            f.close
        #print(title+'爬取成功')

threads = []
threads_1 = []
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
    c1 = input('1.全文爬取\n2.更新爬取(只会爬取未爬取的章节):')
    if c1 == '1':
        for title,item_id in zip(title_list, item_id_list):
            thread = threading.Thread(target=get_content,args=(title,item_id))
            threads.append(thread)
        for thread in tqdm(threads):
            thread.start()
        for thread in threads:
            thread.join()
        print('开始效验')
        for title,item_id in zip(title_list, item_id_list):
            title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
            if os.path.exists('./output/'+ name +'/'+ title + '.txt'):
                #print(f"{title}已创建")
                pass
            else:
                print(f'提示:{title}没有被创建')
                thread = threading.Thread(target=get_content,args=(title,item_id))
                threads_1.append(thread)
            if threads_1 != []:
                for thread in tqdm(threads_1):
                    thread.start()
                for thread in threads_1:
                    thread.join()
        print('效验完成')
    elif c1 == '2':
        for title,item_id in zip(title_list, item_id_list):
            title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
            if os.path.exists('./output/'+ name +'/'+ title + '.txt'):
                print(f"{title}已创建")
            else:
                print(f'提示:{title}没有被创建')
                thread = threading.Thread(target=get_content,args=(title,item_id))
                threads_1.append(thread)
        if threads_1 != []:
            for thread in tqdm(threads_1):
                thread.start()
            for thread in threads_1:
                thread.join()
elif c == '2':
    for r in range(len(title_list)):
        print(f'章节 {r+1} :{title_list[r]}')
    c1 = int(input('选择:'))
    get_content(title_list[c1-1],item_id_list[c1-1])
else:
    print('unknown')
