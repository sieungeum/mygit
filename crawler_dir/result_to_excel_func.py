# 커스텀 함수

# 라이브러리 import
import os

from pandas import DataFrame
from datetime import datetime


########## 엑셀명에 사용할 날짜 저장 ##########
def result_to_excel(news_dict, dict_idx, keywordList):
    date = str(datetime.now())
    date = date[:date.rfind(' ')].replace('-', '_')

    print('데이터프레임 변환\n')
    news_df = DataFrame(news_dict).T

    folder_path = os.getcwd()
    xlsx_file_name = '네이버_경제뉴스_{}개_{}_{}.xlsx'.format(dict_idx, "_".join(keywordList), date)

    news_df.to_excel(xlsx_file_name)

    print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))
