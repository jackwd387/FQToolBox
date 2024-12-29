import threading
import os
from tqdm import tqdm
from ebooklib import epub
import re
from API import book_id_inquire,item_id_inquire

def get_content(title,item_id):
    global item_content_list
    data = item_id_inquire(item_id)
    title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
    item_content_list[item_id] = title + '\n' +data[0]
    #print(title+'爬取成功')
chaplist = []
threads = []
threads_1 = []
item_content_list = {}
headers = {'Cookie': open('cookie.ini','r').read()}
book_id = input('book_id:')
data = book_id_inquire(book_id)
item_id_list = data[0]
title_list = data[1]
name = data[2]
author = data[3]
abstract = data[4]

book = epub.EpubBook()
 
# 添加元数据
book.set_identifier(book_id)
book.set_title(name)
book.set_language('zh')

# 添加作者信息
book.add_author(author)

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
        for item_id,title in zip(item_id_list,title_list):
	        # 创建章节
            chaplist.append(epub.EpubHtml(title=title, file_name=f'{item_id}.xhtml', lang='zh',content=item_content_list[item_id]))
        for chap in chaplist:
            book.add_item(chap)
        book.toc = chaplist
        # 书脊设置
        book.spine = chaplist
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(f"./output/{name}.epub",book)
        print(f'文件已生成到./output/{name}.epub')
    elif c1 == '2':
        print('epub版本暂不支持该功能')
elif c == '2':
    print('epub版本暂不支持该功能')
else:
    print('unknown')
