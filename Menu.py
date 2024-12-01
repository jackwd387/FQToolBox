import os
import json
import requests
import time
from Main.API import user_inquire
print('欢迎使用FQ Toolbox V1.12')
print('一言:'+json.loads(requests.get(url='https://v1.hitokoto.cn').text)['hitokoto'])
time.sleep(0.5)
print('---------------')
if not os.path.exists('cookie.ini'):
    ce = open('cookie.ini','w',encoding='utf-8')
    ce.close()

data = open('cookie.ini','r',encoding='utf-8')
login_data = user_inquire(data.read())
if login_data == 'false':
    print('登录失败,部分功能无法使用，请配置cookie')
else:
    print(f'用户名称:{login_data[0]}')
    print(f'用户头像URL:{login_data[1]}')
    print(f'用户id:{login_data[2]}')
    print(f'用户简介:{login_data[3]}')
data.close()
print('---------------')
while True:
    choose = input('1.搜索书籍\n2.阅读书籍\n3.爬取书籍\n4.推荐榜\n5.设置\n6.DEBUG\n请选择:')
    if choose == '1':
        os.system('python ./Main/FQSearch.py')
    elif choose == '2':
        os.system('python ./Main/FQRead.py')
    elif choose == '3':
        os.system('python ./Main/FQ爬虫.py')
    elif choose == '4':
        os.system('python ./Main/FQ推荐.py')
    elif choose == '5':
        choose = input('1.设置Cookie\n请选择:')
        if choose == '1':
            while True:
                cookie = input('Cookie:')
                data = user_inquire(cookie)
                if data == 'false':
                    print('Cookie无效,请重新设置')
                else:
                    f = open('cookie.ini','w',encoding='utf-8')
                    f.write(cookie)
                    f.close()
                    print(f'用户名称:{data[0]}')
                    print(f'用户头像URL:{data[1]}')
                    print(f'用户id:{data[2]}')
                    print(f'用户简介:{data[3]}')
                break
    elif choose == '6':
        choose = input('1.api测试\n2.番茄听书\n请选择:')
        if choose == '1':
            os.system('python ./Main/Test.py')
        elif choose == '2':
            os.system('python ./Main/Test2.py')
    else:
        print('unknown')
    
