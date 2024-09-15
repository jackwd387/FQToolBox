import API
cookie = open('./Cookie.ini','r',encoding='utf-8').read()
while True:
    c = input('FQAPI TEST\n1.查询book_id\n2.查询item_id\n3.查询用户\n4.查询书架\n5.上传阅读进度\n6添加书架\n请选择:')
    if c == '1':
        API.book_id_inquire(input('book_id:'))
    elif c == '2':
        API.item_id_inquire(input('item_id:'))
    elif c == '3':
        API.user_inquire(cookie)
    elif c == '4':
        API.user_bookshelf(cookie)
    elif c == '5':
        API.update_progres(cookie,input('item_id:'))
    elif c == '6':
        API.add_bookshelf(cookie,input('book_id:'))
    else:
        break