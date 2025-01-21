import threading
import os
from tqdm import tqdm
import re
import time
from API import book_id_inquire,item_id_inquire

def get_content(title,item_id):
        data = item_id_inquire(item_id)
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|]","_",title)#去掉非法字符
        content = re.sub(re.compile('<.*?>'),'\n',data[0].replace('</p><p>','\n'))
        item_content_list[item_id] = title + content
        with open('./output/'+ name +'/'+ title + '.txt', mode='w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(content)
            f.write('\n')
            f.close
        #print(title+'爬取成功')
if __name__ == '__main__':
    item_content_list = {}
    threads = []
    threads_1 = []
    headers = {'Cookie': open('cookie.ini','r').read()}
    book_id = input('book_id:')
    data = book_id_inquire(book_id)
    item_id_list = data[0]
    title_list = data[1]
    name = data[2]
    author = data[3]
    abstract = data[4]
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
            if len(title_list) > 1000:
                print('章节数量超过1000，为防止接口请求失败，已限制释放线程速度')
                for thread in tqdm(threads,desc='释放线程中'):
                    time.sleep(0.012)
                    thread.start()
                print('正在等待线程执行完毕，该过程耗时根据你的宽带')
                for thread in threads:
                    thread.join()
            else:
                for thread in tqdm(threads,desc='释放线程中'):
                    thread.start()
                print('正在等待线程执行完毕，该过程耗时根据你的宽带')
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
                    for fixthread in tqdm(threads_1):
                        fixthread.start()
                    for fixthread in threads_1:
                        fixthread.join()
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
        if input('是否合并TXT?(y/n):') == 'y':
            content = ""
            for item_id in tqdm(item_id_list):
                content += item_content_list[item_id]
            txt_file = './output/' + name + '.txt'
            with open(txt_file,'w',encoding='utf-8') as files:
                files.write(f'书名:{name}\n')
                files.write(f'作者:{author}\n')
                files.write(f'简介:{abstract}\n——————————————\n')
                files.write(content)
                files.close()
            print(f'合并完成,已添加到{txt_file}')
    elif c == '2':
        for r in range(len(title_list)):
            print(f'章节 {r+1} :{title_list[r]}')
        c1 = int(input('选择:'))
        get_content(title_list[c1-1],item_id_list[c1-1])
    else:
        print('unknown')