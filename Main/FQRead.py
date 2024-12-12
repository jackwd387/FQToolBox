import os
import edge_tts
import asyncio
import threading
from API import update_progres,user_bookshelf,book_id_inquire,item_id_inquire
cookie = open('cookie.ini','r').read()
def thread(p):
    global content,voice,rate_count,volume_count
    print('正在爬取并生成音频')
    if p+1 > len(title_list):
        pass
    else:
        content = item_id_inquire(item_id_list[p])[0]
        #print(f'文字数:{len(content)}')
        asyncio.run(run_tts(title_list[p]+content,voice,rate_count,volume_count))
async def run_tts(text: str, voice: str,rate:str,volume:str) -> None:
    global title_list,output_files,count
    communicate =  edge_tts.Communicate(text=text, voice=voice,rate=rate,volume=volume)
    await communicate.save(output_files+item_id_list[p]+'_TEMP.mp3')
if __name__ == '__main__':
    user_data = user_bookshelf(cookie)
    book_id = input('book_id(输入空则使用最近播放书籍):')
    if book_id == '':
        book_id = user_data[0][0]
    data = book_id_inquire(book_id)
    title_list = data[1]
    item_id_list = data[0]
    name = data[2]
    for r in range(len(title_list)):
        print(f'章节 {r+1} :{title_list[r]}')
    p = input('选择(输入空则使用最近播放章节):')
    content = None
    output_files = './TEMP/' + book_id + '_ceche/'
    if p == '':
        item_id = user_data[1][0]
        p = item_id_list.index(item_id)
    else:
        p = int(p) - 1
    os.system('edge-tts  --list-voices')
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
    initialize_thread = threading.Thread(target=thread,args=(p,))
    initialize_thread.start()
    print('等待初始化完毕')
    initialize_thread.join()
    while True:
            if len(title_list) <= p:
                os.system(f'edge-playback --text  "章节播放完毕 感谢使用" --voice '+ voice)
                break
            else:
                title = title_list[p]
                item_id = item_id_list[p]
                p += 1
                print(f'即将播放:{name}:{title}')
                update_progres_thread = threading.Thread(target=update_progres,args=(cookie,item_id))
                update_progres_thread.start()
                ready_thread = threading.Thread(target=thread,args=(p,))
                ready_thread.start()
                os.system('mpv '+'"'+output_files+item_id+'_TEMP.mp3'+'"')
                os.remove(output_files+item_id+'_TEMP.mp3')
                ready_thread.join()
