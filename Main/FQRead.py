# 导入数据请求模块
import requests
import os
import time
import edge_tts
import asyncio
import _thread
import json
cookie = open('cookie.ini','r').read()
title_list = []
item_id_list = []
executable = 'False'
def get_item_id(book_id):
    global name,title_list,item_id_list
    url = 'https://fanqienovel.com/api/reader/directory/detail?bookId='+book_id
    # 发送请求
    json_data = json.loads(requests.get(url=url).text)
    """解析数据: 提取我们需要的数据内容"""
    # 提取章节名
    for i in json_data['data']['chapterListWithVolume']:
        for v in i:
            title_list.append(v['title'])
    # 提取章节ID
    item_id_list = json_data['data']['allItemIds']
    # 提取书名
    json_data2 = json.loads(requests.get(url='https://fanqienovel.com/api/reader/full?itemId='+item_id_list[0]).text)
    name = json_data2['data']['chapterData']['bookName']
    print('书名:'+name)
def get_content(title,item_id):
        # 完整的小说章节链接
        link_url = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id=' + item_id
        # 发送请求+获取数据内容
        link_data = json.loads(requests.get(url=link_url).text)
        # 把<p>转 \n 换行符
        return link_data['data']['content'].replace('</p><p>','\n').replace('<p>','\n').replace('</p>','\n') #.replace('【','\n中括号\n').replace('】','\n中括号括回来\n')
def thread(p):
    global content,voice,rate_count,volume_count,executable
    print('正在爬取并生成音频')
    content = get_content(title_list[p-1],item_id_list[p-1])
    asyncio.run(run_tts(title_list[p-1]+content,voice,rate_count,volume_count))
    if executable == 'False':
        executable = 'True'
async def run_tts(text: str, voice: str,rate:str,volume:str) -> None:
    global title_list,output_files,count
    communicate =  edge_tts.Communicate(text=text, voice=voice,rate=rate,volume=volume)
    await communicate.save(output_files+item_id_list[p-1+count]+'_TEMP.mp3')
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
#   模拟浏览器
headers = {
    # User-Agent 用户代理, 表示浏览器/设备的基本身份信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #cookie
    ,'Cookie': cookie
    }
# url地址(小说主页)
if __name__ == '__main__':
    book_id = input('book_id:')
    get_item_id(book_id)
    c = input('选择阅读方法:\n1.pyttsx4\n2.edge-tts\n你都选择是:')
    print(title_list)
    # 阅读方法1
    if c == '1':
        import pyttsx4
        engine = pyttsx4.init()   # 初始化
        count = 0
        p = int(input('选择:'))
        voices = engine.getProperty('voices')
        for voice in voices:
            print ('id = {} \nname = {} \n'.format(voice.id, voice.name))
        s = int(input('设置语音:'))
        engine.setProperty('voice', voices[s-1].id)  #设置发音人
        rate_count = int(input('语速大小:'))
        rate = engine.getProperty('rate')   # getting details of current speaking rate
        engine.setProperty('rate', rate_count)     # setting up new voice rate

        volume_count = float(input('音量大小:'))
        volume = engine.getProperty('volume')  #getting to know current volume level (min=0 and max=1)
        engine.setProperty('volume',volume_count)    # setting up volume level  between 0 and 1
        while True:
            print('正在爬取'+title_list[p-1+count])
            content = get_content(title_list[p-1+count],item_id_list[p-1+count])
            if count+p > len(item_id_list):
                engine.say('已播放完最新章节')
                engine.runAndWait()
                break
            else:
                engine.say(title_list[p-1+count]+'\n'+content)
            print('正在播放:'+name+':'+title_list[p-1+count])
            engine.runAndWait()
            count += 1
    elif c == '2':
        p = int(input('选择:'))
        count = 0
        content = None
        output_files = './TEMP/' + book_id + '_ceche/'
        os.system('edge-tts --list-voices')
        voice = input('请选择音色(默认zh-CN-XiaoxiaoNeural):')
        rate_count = input('语速大小(默认+0%):')
        volume_count = input('音量大小(默认+0%):')
        if voice == '':
            voice = 'zh-CN-XiaoxiaoNeural'
        if rate_count == '':
            rate_count = '+0%'
        if volume_count == '':
            volume_count = '+0%' 
        if not os.path.exists(output_files):
            os.makedirs(output_files)
        _thread.start_new_thread(thread,(p+count,))
        while True:
            if executable == 'True':
                title = title_list[p-1+count]
                item_id = item_id_list[p-1+count]
                if count+p > len(item_id_list):
                    os.system('edge-playback --text "已播放完最新章节" --voice '+ voice)
                    break
                else:
                    count += 1
                    print('即将播放:'+name+':'+title)
                    update_progres(cookie,item_id)
                    _thread.start_new_thread(thread,(p+count,))
                    os.system('mpv '+'"'+output_files+item_id+'_TEMP.mp3'+'"')
                    os.remove(output_files+item_id+'_TEMP.mp3')
            else:
                print('等待初始化完毕')
                time.sleep(1)
