# 커스텀 함수

# 라이브러리 import\
import requests
from bs4 import BeautifulSoup

# sleep_sec은 0.7초로 설정
sleep_sec = 0.7

# 크롤링할 기사인지 구분해주는 함수
def is_valid_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    res = requests.get(url, headers=headers)
    res.encoding = None
    soup = BeautifulSoup(res.content, 'html.parser')

    title = soup.head.title.text
    category = soup.find("li", {'class': 'is_active'})
    content = soup.find("div", {'id': 'dic_area'})

    # 경제 카테고리 확인
    if category == None:
        print("카테고리가 존재하지 않습니다. 기사를 수집하지 않습니다.")
        isValid_1 = False
    else:
        if "경제" not in category.get_text():
            print("카테고리가 <" + category.get_text().replace('\n', '') + "> 이므로 기사를 수집하지 않습니다.")
            isValid_1 = False
        else:
            print("카테고리가 <" + category.get_text().replace('\n', '') + "> 이므로 기사를 수집합니다.")
            isValid_1 = True

    # 제목에 "인사" 포함 시 뉴스 기사와 관련 없는 내용, 본문이 비어있는 오류 발생 시 다음 뉴스기사로 넘어가기
    if "인사" not in title:
        if content != None:
            isValid_2 = True
        else:
            isValid_2 = False
    else:
        isValid_2 = False

    # 두개의 if문이 모두 True일때만 isValid = True
    if isValid_1 and isValid_2:
        isValid = True
    else:
        isValid = False

    return isValid, soup
