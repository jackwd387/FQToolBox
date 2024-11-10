# 导入数据请求模块
import requests
import os
import edge_tts
import asyncio
import _thread
import json
from API import update_progres,user_bookshelf,book_id_inquire,item_id_inquire
cookie = open('cookie.ini','r').read()
executable = 'False'
url = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id='
def thread(p):
    global content,voice,rate_count,volume_count,executable
    print('正在爬取并生成音频')
    if p > len(title_list):
        None
    else:
        content = item_id_inquire(item_id_list[p-1])[0]
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
    data = book_id_inquire(book_id)
    title_list = data[1]
    item_id_list = data[0]
    name = data[2]
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
