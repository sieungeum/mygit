import pandas as pd
import numpy as np

import relation_dir.to_excel_func as tef
import relation_dir.clusting_func_dir.get_intersection_data_func as gidf
import relation_dir.clusting_func_dir.get_cluster_details_func as gcdf
import relation_dir.tf_idf_custom_func as ticf

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# 따로 실행 시 주석 풀고 거는거 3개 있음

# 따로 사용할때 주석풀기
# path = 'G:/내 드라이브/4학년 1학기/캡스톤디자인 파일/뉴스 일별 모음(4.10부터)/정확성순 대량 데이터/'
# data = pd.read_excel(path + '네이버_경제뉴스_3000개_물가_금리_정책_2023_05_30.xlsx')

def news_relation_analysis(data):
    # 비어있는 데이터 제거
    data = pd.DataFrame(data).T  # 따로 실행할때 주석걸기
    data = data[data['content'].notnull()]  # Null값 데이터 없애기

    # 키워드명 가져오기
    keywords = list(set(data['keyword']))

    # "stop_word.txt" 파일 읽어들여 불용어 가져오기
    f_stop_word = open("stop_word.txt", 'r', encoding='utf-8')
    stopword_kor = " ".join(f_stop_word.readlines()).split(" ")

    # 최대 features는 400, clusting모델 kmeans에 사용할 tf-idf 값 구하기
    max_feature = 400
    tfidf, tfidf_matrix = ticf.tf_idf_custom(data, stopword_kor, max_feature)

    # 클러스터 갯수
    n_clst = 50

    # 클러스터링 모델 생성
    kmeans = KMeans(n_clusters=n_clst, max_iter=50000, random_state=42)

    # 클러스터링 예측값을 데이터 컬럼에 추가
    cluster_label = kmeans.fit_predict(tfidf_matrix)
    data['cluster_label'] = cluster_label

    feature_names = tfidf.get_feature_names_out() # 학습에 사용된 단어사전 변수 선언

    # 클러스터 정보 가져오기
    cluster_details, relation_idx = gcdf.get_cluster_details(cluster_model=kmeans, cluster_data=data,
                                                        feature_names=feature_names, cluster_num=n_clst,
                                                        top_n_features=20)

    # 키워드들이 교집합으로 묶인 클러스터의 데이터들의 인덱스 추출
    relation_idx = gidf.get_intersection_data(cluster_details, relation_idx, keywords)

    # 교집합으로 묶이는 데이터가 없을 경우 종료, 해당 키워드 사용불가
    if len(relation_idx) == 0:
        print("fuck, this keywords is so fucking words")
        return 0

    # 최대 features는 50, 코사인 유사도에 사용될 tf-idf 구하기
    max_feature = 50
    tfidf, tfidf_matrix = ticf.tf_idf_custom(data.loc[relation_idx[0]], stopword_kor, max_feature)

    # 코사인 유사도 분석
    cosine_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 클러스팅 모델로 추출된 뉴스기사 본문 가져오기
    cluster_data = data.loc[relation_idx[0]]['content']
    cluster_data = cluster_data.values

    aver_over = {}  # 평균 이상의 뉴스기사 저장
    average = 0  # 전체 평균

    # 전체 TF-IDF 확률의 평균
    while average < 0.6:

        row_aver = []  # 각 행의 평균치
        aver_over = {}  # 전체 평균 이상인 각 행의 평균치

        # 기사 하나에 대한 다른 기사들 간의 TF-IDF 확률의 평균
        for i in cosine_matrix:
            row_aver.append(np.mean(i))
        average = np.mean(row_aver)

        # 위에서 구한 TF-IDF 확률이 전체 평균 이상인 것만 추출
        for i in range(len(cosine_matrix)):
            if row_aver[i] > average:
                aver_over[i] = row_aver[i]

        print(aver_over)
        print(average)
        print(len(aver_over))

        # 평균 이하의 평균값을 가진 뉴스기사 제거
        b = []
        for i in range(len(cosine_matrix)):
            if i not in aver_over.keys():
                b.append(i)

        cosine_matrix = np.delete(cosine_matrix, b, axis=0)
        cosine_matrix = np.delete(cosine_matrix, b, axis=1)

        cluster_data = np.delete(cluster_data, b, axis=0)

    # 딕셔너리 형태로 선별된 데이터 저장
    extract_dict = {}
    for n, i in enumerate(cluster_data):
        extract_dict[n] = {
            "title": data.loc[data['content'] == i, "title"].values.tolist()[0],
            "keyword": data.loc[data['content'] == i, "keyword"].values.tolist()[0],
            "agency": data.loc[data['content'] == i, "agency"].values.tolist()[0],
            "url": data.loc[data['content'] == i, "url"].values.tolist()[0],
            "content": data.loc[data['content'] == i, "content"].values.tolist()[0]
        }

    # 엑셀로 저장
    tef.to_excel(extract_dict, len(extract_dict))

    # DB에 저장
    # ldf.load_db(extract_dict)

    f_stop_word.close()

def get_intersection_keyword(keywords, cluster_features):
    if len( set(keywords) & set(cluster_features)) == len(keywords):
        return True
    else:
        return False

# 따로 실행할 때 주석 풀기
# news_relation_analysis(data)
