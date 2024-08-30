import requests,json
query = input('搜索内容:')
page = 1
while True:
    url = f'https://api5-normal-lf.fqnovel.com/reading/bookapi/search/page/v/?query={query}&aid=1967&channel=0&os_version=0&device_type=0&device_platform=0&iid=466614321180296&passback={(page-1)*10}&version_code=999'
    data = json.loads(requests.get(url=url).text)
    for i in data['data']:
        print('book_id:'+i['book_data'][0]['book_id'])
        print('书名:'+i['book_data'][0]['book_name'])
        print('作者:'+i['book_data'][0]['author'])
        print('简介:'+i['book_data'][0]['abstract'])
        print('类型:'+i['book_data'][0]['category'])
        print('Sub_info:'+i['book_data'][0]['sub_info'])
        print('------------------------')
    if input('Next:') == 'n':
        break
    else:
        page = int(input('page:'))
