from API import recommended_list
for i in recommended_list():
    print(f"book_id:{i['book_id']}")
    print(f"书名:{i['book_name']}")
    print(f"简介:{i['abstract']}")
    print(f"作者:{i['author']}")
    print(f"书籍创建时间:{i['create_time']}")
    print(f"阅读人数:{i['read_count']}")
    print(f"分数:{i['score']}")
    print('————————————————————')
    