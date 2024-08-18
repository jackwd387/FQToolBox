from requests import Session
import pyperclip
# Cookie
Cookie = open('cookie.ini','r').read()
# 搜索api
search_url = 'https://novel.snssdk.com/api/novel/channel/homepage/search/search/v1/'
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Danger hiptop 3.4; U; AvantGo 3.2)',
    'Cookie': Cookie
    }


self = Session()  # 创建一个Session对象，并赋值给self
def search(self, keywords: str) -> list[dict] | str:
    """
    搜索书籍信息
    参数:
    keywords (str): 关键字
    返回:
    list: 书籍信息列表
    """
    # 获得书本基本信息
    params = {
        'aid': 1967,
        'q': keywords
    }
    book_list_info = self.get(search_url, params=params, headers=headers).json()
    return book_list_info['data']['ret_data'] if 'ret_data' in book_list_info['data'].keys() else '未配置cookie或者cookie失效'
search_content = input('搜索内容:')
search_result = (search(self,search_content))
for i in range(len(search_result)):
    print(f'No.{i+1}')
    print('title:'+search_result[i]['title'])
    
    print('abstract:'+search_result[i]['abstract'])
    
    print('author:'+search_result[i]['author'])
    
    print('book_id:'+search_result[i]['book_id'])
    
    print('thumb_url:'+search_result[i]['thumb_url'])
    
choose = int(input('请选择:'))-1
print('title:'+search_result[choose]['title'])
pyperclip.copy(search_result[choose]['book_id'])
print('已复制book_id:'+search_result[choose]['book_id'])
