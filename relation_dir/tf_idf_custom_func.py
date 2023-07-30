from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

def tf_idf_custom(data, stopword_kor, max_feature):

    # 불용어는 커스텀 불용어 사용 등 모델 생성
    tfidf = TfidfVectorizer(max_features=max_feature,
                                     stop_words=stopword_kor,
                                     ngram_range=(1, 2),
                                     min_df=0.05,
                                     max_df=0.85)

    # tfidf 계산
    tfidf_matrix = tfidf.fit_transform(data['content'])

    # 기존 사용된 단어 사전 커스텀(숫자, 숫자 + 문자, 조사 등 제거)
    use_vocabulary = set(non_word_del(tfidf.vocabulary_, stopword_kor))

    # 커스텀 단어사전 대입
    tfidf = TfidfVectorizer(vocabulary=use_vocabulary)
    tfidf_matrix = tfidf.fit_transform(data['content'])

    return tfidf, tfidf_matrix

def non_word_del(all_word, stopword_kor):
    okt = Okt()

    use_word = []

    for i in all_word.keys():
        # okt는 영어는 그냥 없애버리기 때문에 영어이면 그냥 추가
        if i.encode().isalpha():
            use_word.append(i)
            continue

        i = ''.join(okt.nouns(i))

        if len(i) == 0:
            continue
        elif i not in stopword_kor and i.isalpha():
            use_word.append(i)

    return use_word
