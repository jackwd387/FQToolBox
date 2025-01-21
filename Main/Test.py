import API
cookie = open('./Cookie.ini','r',encoding='utf-8').read()
while True:
    c = input('FQAPI TEST\n1.查询book_id\n2.查询item_id\n3.查询用户\n4.查询书架\n5.上传阅读进度\n6.添加书架\n7.段评查看\n8.书评查看\n9.查询user_id\n10.剧url获取\n11.听书url获取\n请选择:')
    if c == '1':
        data = API.book_id_inquire(input('book_id:'))
        for i in range(len(data[0])):
            print(f'Title:{data[1][i]}')
            print(f'item_id:{data[0][i]}')
        print(f'book_name:{data[2]}')
        print(f'author:{data[3]}')
        print(f'abstract:{data[4]}')
        print(f'tags:{data[5]}')
        print(f'score:{data[6]}')
        print(f'read_count:{data[8]}')
        print(f'word_number:{data[7]}')
        print(f'thumb_url:{data[10]}')
        if data[11] == True:
            print('此书无法被分享 可能是被封禁或未发布')
    elif c == '2':
        data = API.item_id_inquire(input('item_id:'))
        print(f'content:{data[0]}')
        print(f'title:{data[1]}')
        print(f'author:{data[2]}')
        print(f'book_id:{data[3]}')
        print(f'book_name:{data[4]}')
        print(f'next_item_id:{data[5]}')
        print(f'pre_item_id:{data[6]}')
    elif c == '3':
        data = API.user_inquire(cookie)
        print(f'用户名称:{data[0]}')
        print(f'用户头像URL:{data[1]}')
        print(f'用户id:{data[2]}')
        print(f'用户简介:{data[3]}')
    elif c == '4':
        data = API.user_bookshelf(cookie)
        for i in range(len(data[0])):
            print('用户书架书籍:'+data[0][i])
            print('此用户在此书最后一次阅读的章节:'+data[1][i])
            print('此用户在此书最后一次阅读的时间:'+data[2][i])
            print('————————————————————')
    elif c == '5':
        API.update_progres(cookie,input('item_id:'))
    elif c == '6':
        API.add_bookshelf(cookie,input('book_id:'))
    elif c == '7':
        print(API.paragraph_comments(input('item_id:'),input('para_index:')))
    elif c == '8':
        print(API.book_comments(input('book_id:')))
    elif c == '9':
        data = API.user_id_inquire(input('user_id:'))
        print(f'用户名:{data[0]}')
        print(f'头像:{data[1]}')
        print(f'是否作家:{data[2]}')
        print(f'简介:{data[3]}')
        print(f'阅读时间:{data[4]}')
        print(f'阅读数量:{data[5]}')
        print(f'点赞数:{data[6]}')
        print(f'粉丝数:{data[7]}')
        print(f'关注数:{data[8]}')
        print(f'作者书籍:{data[9]}')
    elif c == '10':
        print(API.video_get(input('video_id:')))
    elif c == '11':
        print(API.reading(input('音色:'),input('item_id:')))
    else:
        break
