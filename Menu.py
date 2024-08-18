import os
import json
import requests
import _thread
import time
print('欢迎使用FQ Toolbox V1.7')
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
def start_server():
    print('由于所使用Api不在开放,需要开启本地FQApi服务器\n---------------')
    os.system('FQApi.exe')
print('一言:'+json.loads(requests.get(url='https://v1.hitokoto.cn').text)['hitokoto'])
_thread.start_new_thread(start_server,())
time.sleep(0.5)
print('---------------')
if not os.path.exists('cookie.ini'):
    open('cookie.ini','w',encoding='utf-8')
if user_inquire(open('cookie.ini','r',encoding='utf-8').read()) == 'false':
    print('登录失败,部分功能无法使用，请在cookie.ini配置cookie')
print('---------------')
while True:
    choose = input('1.搜索书籍\n2.阅读书籍\n3.爬取书籍\n4.DEBUG\n请选择:')
    if choose == '1':
        os.system('python ./Main/FQSearch.py')
    elif choose == '2':
        os.system('python ./Main/FQread.py')
    elif choose == '3':
        os.system('python ./Main/FQ爬虫.py')
    elif choose == '4':
        choose = input('1.api测试\n请选择:')
        if choose == '1':
            os.system('python ./Main/Test.py')
    else:
        print('unknown')
    
