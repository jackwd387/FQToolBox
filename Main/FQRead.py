# 导入数据请求模块
import requests
import os
import edge_tts
import asyncio
import _thread
import json
from API import update_progres,user_bookshelf
cookie = open('cookie.ini','r').read()
title_list = []
item_id_list = []
executable = 'False'
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
def get_content(item_id):
        # 完整的小说章节链接
        link_url = url + item_id
        # 发送请求+获取数据内容
        link_data = json.loads(requests.get(url=link_url).text)
        # 把<p>转 \n 换行符
        return link_data['data']['content'].replace('</p><p>','\n').replace('<p>','\n').replace('</p>','\n') #.replace('【','\n中括号\n').replace('】','\n中括号括回来\n')
def thread(p):
    global content,voice,rate_count,volume_count,executable
    print('正在爬取并生成音频')
    if p > len(title_list):
        None
    else:
        content = get_content(item_id_list[p-1])
        print(f'文字数:{len(content)}')
        asyncio.run(run_tts(title_list[p-1]+content,voice,rate_count,volume_count))
        if executable == 'False':
            executable = 'True'
async def run_tts(text: str, voice: str,rate:str,volume:str) -> None:
    global title_list,output_files,count
    communicate =  edge_tts.Communicate(text=text, voice=voice,rate=rate,volume=volume)
    await communicate.save(output_files+item_id_list[p-1+count]+'_TEMP.mp3')
#   模拟浏览器
headers = {
    # User-Agent 用户代理, 表示浏览器/设备的基本身份信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #cookie
    ,'Cookie': cookie
    }
# url地址(小说主页)
if __name__ == '__main__':
    book_id = input('book_id(输入空则使用最近播放):')
    if book_id == '':
        book_id = user_bookshelf(cookie)[0]
    get_item_id(book_id)
    for r in range(len(title_list)):
        print(f'章节 {r+1} :{title_list[r]}')
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
    print('等待初始化完毕')
    while True:
        if executable == 'True':
            if len(title_list) <= p-1+count:
                os.system(f'edge-playback --text  "章节播放完毕 感谢使用" --voice '+ voice)
                break
            else:
                executable = 'False'
                title = title_list[p-1+count]
                item_id = item_id_list[p-1+count]
                count += 1
                print('即将播放:'+name+':'+title)
                update_progres(cookie,item_id)
                _thread.start_new_thread(thread,(p+count,))
                os.system('mpv '+'"'+output_files+item_id+'_TEMP.mp3'+'"')
                os.remove(output_files+item_id+'_TEMP.mp3')
