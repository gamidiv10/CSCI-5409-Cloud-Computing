import pymongo
import time

books = []
log_list = []

for i in range(1996, 2021, 1):
    file = 'C:/Users/vamsi/Desktop/A3/gutindexfiles/GUTINDEX.' + str(i) + '.txt'
    start_time = time.time()
    with open(file, 'r', encoding="utf8") as file:
        data = file.read().replace(u'\xa0', u' ')
        for line in data.split('\n'):
            if ", by" in line:
                book = line.strip().replace(u'\xa0', u' ').split('   ')[0].split(', by', 2)
                book[0] = book[0].strip()
                book[1] = ''.join([i for i in book[1] if not i.isdigit()]).strip()
                books.append(book)
    end_time = time.time()
    log_list.append({'file': i , 'start_time':start_time, 'end_time':end_time})

    time.sleep(300)

mongo_client = pymongo.MongoClient("mongodb://admin:myadminpassword@3.82.157.225:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false")
db = mongo_client["Books"]


# for book in books:
#     books_list = []
#     books_list.append({'title': book[0], 'author': book[1]})
    # start_time = time.time()
    # db.books.insert_many(books_list)
    # time.sleep(300)
    # end_time = time.time()
    # log_list.append({'book': book[0], 'start_time':start_time, 'end_time':end_time})
db.log.insert_many(log_list)

mongo_client.close()