from pymongo import MongoClient
from pandas import DataFrame
import datetime

def load_db(extract_dict):
    # 현재 날짜
    today = datetime.datetime.now()
    ymd = str(today.year) + str(today.month) + str(today.day)

    # path = 'G:/내 드라이브/4학년 1학기/캡스톤디자인 파일/뉴스 일별 모음(4.10부터)/정확성순 대량 데이터/'
    # data = pd.read_excel(path + '선별된 데이터_317개.xlsx', index_col=0)

    data = DataFrame(extract_dict).T

    keywords = set(data['keyword'])
    print(keywords)
    extract_dict = data.to_dict('records')

    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017/")

    for keyword in keywords:
        db = client.get_database(keyword)
        col = db.get_collection(ymd)

        for i in extract_dict:
            if i['keyword'] == keyword:
                col.insert_one(i)

    client.close()












