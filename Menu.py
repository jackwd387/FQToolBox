import os
import json
import requests
import time
from Main.API import user_inquire
print('欢迎使用FQ Toolbox V1.11')
print('一言:'+json.loads(requests.get(url='https://v1.hitokoto.cn').text)['hitokoto'])
time.sleep(0.5)
print('---------------')
if not os.path.exists('cookie.ini'):
    open('cookie.ini','w',encoding='utf-8')
data = user_inquire(open('cookie.ini','r',encoding='utf-8').read())
if data == 'false':
    print('登录失败,部分功能无法使用，请在cookie.ini配置cookie')
else:
    print(f'用户名称:{data[0]}')
    print(f'用户头像URL:{data[1]}')
    print(f'用户id:{data[2]}')
    print(f'用户简介:{data[3]}')
print('---------------')
while True:
    choose = input('1.搜索书籍\n2.阅读书籍\n3.爬取书籍\n4.DEBUG\n请选择:')
    if choose == '1':
        os.system('python ./Main/FQSearch.py')
    elif choose == '2':
        os.system('python ./Main/FQRead.py')
    elif choose == '3':
        os.system('python ./Main/FQ爬虫.py')
    elif choose == '4':
        choose = input('1.api测试\n2.番茄听书\n请选择:')
        if choose == '1':
            os.system('python ./Main/Test.py')
        elif choose == '2':
            os.system('python ./Main/Test2.py')
    else:
        print('unknown')
    
