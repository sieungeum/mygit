########## 엑셀로 변환 ##########
import os
from pandas import DataFrame

def to_excel(extract_dict, len_ext_dict):
    print('데이터프레임 변환\n')
    ext_df = DataFrame(extract_dict).T

    folder_path = os.getcwd()
    xlsx_file_name = '선별된 데이터_{}개.xlsx'.format(len_ext_dict)

    ext_df.to_excel(xlsx_file_name)

    print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))