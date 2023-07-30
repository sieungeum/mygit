#커스텀 함수
import crawler_dir.is_valid_article_func as ivaf
import crawler_dir.crawling_main_text_func as cmtf
import crawler_dir.result_to_excel_func as rtef

import relation_dir.news_relaion_analysis_func as nraf
# 라이브러리 import
import sys, os
import requests
import re
import pickle, json, glob, time
import threading
import queue
from pandas import DataFrame
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

#셀레니움 관련 라이브러리
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options #User-agent, headlessChrome 사용시 필요

# 셀레니움 속도 개선
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# KeywordList로 첫번쨰 반복문(키워드 하나마다 반복한다.)

#sleep_sec은 0.5초로 설정
sleep_sec = 0.5

pressList1 = ["머니투데이", "데일리안", "헤럴드경제", "이데일리", "YTN", "서울경제", "뉴스1", "경향신문", "파이낸셜뉴스", "머니S"]
pressList2 = ['매일경제','뉴시스', '연합뉴스', '한국경제', 'KBS', '중앙일보', '조선일보', '국민일보', '아시아경제', '조선비즈']

q_dict = queue.Queue()

def crawling_func(keyword, newsCount, pressList, q_dict):

    news_dict = {}
    dict_idx = 0
    # chromedriver 경로설정 및 option 설정진행
    caps = DesiredCapabilities().CHROME  # 원래는 "normal"로 되있음. 페이지가 완전히 로드되는 것을 안가다림
    caps["pageLoadStrategy"] = "none"

    options = Options()
    options.headless = True  # 구글창 안나오게 하기
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    options.add_argument('user-agent=' + user_agent)
    chromedriver = 'C:/dev_python/Webdriver/chromedriver.exe'
    driver = webdriver.Chrome(service=Service(chromedriver), options=options)

    print('\n● ' + keyword + "에 대한 기사 크롤링을 시작합니다.")
    news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(keyword)
    driver.get(news_url)
    time.sleep(sleep_sec)
    # driver.implicitly_wait(10)

    #### 옵션 클릭
    search_opn_btn = driver.find_element(By.XPATH, '//a[@class="btn_option _search_option_open_btn"]')
    search_opn_btn.click()
    time.sleep(sleep_sec)
    print("option ok")

    #### 기간(순서 중요, 기간, 언론사 등 선택 후 -> 정렬 선택)
    bx_term = driver.find_element(By.XPATH,
                                  '//div[@role="listbox" and @class="api_group_option_sort _search_option_detail_wrap"]//li[@class="bx term"]')
    time.sleep(sleep_sec)

    # 1일까지
    term_tablist = bx_term.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
    time.sleep(sleep_sec)

    driver.implicitly_wait(10)  # 유독 여기에서 오류가 남

    term_tablist[3].click()

    # 7일까지
    # term_tablist = bx_term.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
    # term_tablist[3].click()
    # time.sleep(sleep_sec)

    # 1개월까지
    # term_tablist = bx_term.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
    # term_tablist[4].click()
    # time.sleep(sleep_sec)

    # 3개월 까지
    # term_tablist = bx_term.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
    # time.sleep(sleep_sec)
    #
    # driver.implicitly_wait(10)  # 유독 여기에서 오류가 남
    #
    # term_tablist[5].click()

    #### 정렬
    bx_lineup = driver.find_element(By.XPATH,
                                    '//div[@role="listbox" and @class="api_group_option_sort _search_option_detail_wrap"]//li[@class="bx lineup"]')
    time.sleep(sleep_sec)

    # 최신순
    # lineup_tablist = bx_lineup.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
    # lineup_tablist[1].click()
    # time.sleep(sleep_sec)

    # 정확성순
    lineup_tablist = bx_lineup.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
    lineup_tablist[0].click()
    time.sleep(sleep_sec)

    #### 언론사별 크롤링 시작
    for press in tqdm(pressList, total=len(pressList)):  # 전체 진행수
        # ---------------------------------------------------------------------------------------------------- #

        no_exist = 0  # 검색결과가 없는 경우
        all_search = 0  # 모든 뉴스를 다 돌아봐도 내가 입력한 값보다 부족할 경우
        id = 1
        print('\n' + '=' * 97 + '\n')
        print("언론사 [{}]에서 키워드 [{}]에 대해 크롤링 작업을 시작합니다.".format(press, keyword))
        # time.sleep(sleep_sec)

        #### 언론사
        bx_press = driver.find_element(By.XPATH,
                                       '//div[@role="listbox" and @class="api_group_option_sort _search_option_detail_wrap"]//li[@class="bx press"]')

        # 기준 두번 째(언론사 분류순) 클릭하고 오픈하기
        press_tablist = bx_press.find_elements(By.XPATH, './/div[@role="tablist" and @class="option"]/a')
        press_tablist[1].click()
        time.sleep(sleep_sec)

        # 첫 번째 것(언론사 분류선택)
        bx_group = bx_press.find_elements(By.XPATH,
                                          './/div[@class="api_select_option type_group _category_select_layer"]/div[@class="select_wrap _root"]')[
            0]

        # 언론사 분류
        press_kind_bx = bx_group.find_elements(By.XPATH, './/div[@class="group_select _list_root"]')[0]

        # 언론사 종류
        press_kind_btn_list = press_kind_bx.find_elements(By.XPATH,
                                                          './/ul[@role="tablist" and @class="lst_item _ul"]/li/a')
        time.sleep(sleep_sec)

        # -----언론사의 XPATH를 찾는 반복문-----
        for press_kind_btn in press_kind_btn_list:
            # time.sleep(sleep_sec)

            # 언론사 종류를 순차적으로 클릭(좌측)
            press_kind_btn.click()
            time.sleep(sleep_sec)

            # 언론사선택(우측)
            press_slct_bx = bx_group.find_elements(By.XPATH, './/div[@class="group_select _list_root"]')[1]
            # 언론사 선택할 수 있는 클릭 버튼
            press_slct_btn_list = press_slct_bx.find_elements(By.XPATH,
                                                              './/ul[@role="tablist" and @class="lst_item _ul"]/li/a')
            # 언론사 이름들 추출
            press_slct_btn_list_nm = [psl.text for psl in press_slct_btn_list]
            # 언론사 이름 : 언론사 클릭 버튼 인 딕셔너리 생성 list_nm => 언론사 이름 btn_list => 언론사 클릭버튼
            press_slct_btn_dict = dict(zip(press_slct_btn_list_nm, press_slct_btn_list))

            # 원하는 언론사가 해당 이름 안에 있는 경우
            # 1) 클릭하고
            # 2) 더이상 언론사분류선택 탐색 중지
            if press in press_slct_btn_dict.keys():
                print('<{}> 카테고리에서 <{}>를 찾았으므로 언론사 탐색을 종료합니다'.format(press_kind_btn.text, press))
                press_slct_btn_dict[press].click()
                time.sleep(sleep_sec)
                break

        #         #pressList에 있는 언론사를 찾았다면, 키워드에 대해 크롤링 시작
        #         print('\n=> <' + press + '> 에서 <' + keyword + '>에 대해 크롤링을 시작합니다.')

        #####동적 제어로 페이지 넘어가며 크롤링
        idx = 0
        cur_page = 1

        pbar = tqdm(total=newsCount, leave=True)

        # newsCount를 담기위한 임시변수
        org_news_num = newsCount

        while idx < newsCount:
            # NewsList가 존재할때 try, 존재하지 않는다면 Except
            try:
                table = driver.find_element(By.XPATH, '//ul[@class="list_news"]')
            except:
                print("검색 결과가 존재하지 않습니다. 다음 언론사에서 검색합니다.")
                no_exist = 1
                break

            # '네이버 뉴스'의 태그를 찾는 과정
            li_list = table.find_elements(By.XPATH, './li[contains(@id, "sp_nws")]')
            area_list = [li.find_element(By.XPATH, './/div[@class="news_area"]') for li in li_list]
            info_list = [info.find_element(By.XPATH, './/div[@class="news_info"]') for info in area_list]
            group_list = [group.find_element(By.XPATH, './/div[@class="info_group"]') for group in info_list]
            a_list = [naver.find_element(By.XPATH, './/a[@class="info"][1]') for naver in group_list]
            time.sleep(sleep_sec)

            for n in a_list[:len(a_list)]:
                if idx == newsCount:
                    break

                n_url = n.get_attribute('href')

                isValid, soup = ivaf.is_valid_article(n_url)
                if isValid == True:
                    title, content = cmtf.crawling_main_text(soup, press)

                    # 문장이 비어있거나(이럴경우 'a' 출력) 같은 뉴스가 두번 저장될 경우
                    if content == 'a' or dict_idx - 1 >= 0 and content == news_dict[dict_idx - 1]['content']:
                        idx += 1
                        newsCount += 1
                        continue
                    news_dict[dict_idx] = {'title': title,
                                           'keyword': keyword,
                                           'agency': press,
                                           'url': n_url,
                                           'content': content}
                    idx += 1
                    dict_idx += 1
                    pbar.update(1)
                elif isValid == False:
                    idx += 1
                    newsCount += 1
                    continue

            # 아직 탐색을 끝마치지 못했을때,
            if idx < newsCount:
                cur_page += 1
                pages = driver.find_element(By.XPATH, '//div[@class="sc_page_inner"]')

                try:
                    next_page_url = [p for p in pages.find_elements(By.XPATH, './/a') if p.text == str(cur_page)][
                        0].get_attribute('href')
                # 원하는 양을 찾지 못하고 모든 뉴스기사를 다 돌아 봤을 경우
                except:
                    all_search = 1
                    break

                driver.get(next_page_url)
                time.sleep(sleep_sec)
            else:
                pbar.close()

                print('\n기사 수집을 완료하였습니다. \n')
                time.sleep(sleep_sec)
                break

        # 모든 뉴스를 다 찾았을때
        if all_search == 1:
            print("※ 요청하신 기사의 수보다 기사가 부족합니다.\n다음 언론사에서 검색합니다.")

            time.sleep(sleep_sec)
            newsCount = org_news_num

            # driver.quit()
            # time.sleep(2)

            continue
        elif no_exist == 1:

            time.sleep(sleep_sec)
            newsCount = org_news_num
            #
            # driver.quit()
            # time.sleep(2)
            continue

        newsCount = org_news_num

    driver.quit()
    time.sleep(2)

    q_dict.put(news_dict)

    # 유사도 선별 전 데이터셋 엑셀 저장
    # rtef.result_to_excel(news_dict, dict_idx, keyword)


def naver_crawler():

    print('=' * 25 + "NAVER NEWS CRAWLER" + '=' * 25 + '\n')

    numberOfKeyword = int(input('키워드의 개수 : '))
    keywordList = list()
    for i in range(numberOfKeyword):
        keywordList.append(input(str(i + 1) + "번째 키워드 : "))
    newsCount = int(input('언론사별 수집 뉴스의 수 (숫자만 입력) : '))

    print('\n' + '=' * 25 + "START CRAWLING" + '=' * 25 + '\n')

    # # chromedriver 경로설정 및 option 설정진행
    # options = Options()
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    # options.add_argument('user-agent=' + user_agent)
    # chromedriver = 'C:/dev_python/Webdriver/chromedriver.exe'
    # driver = webdriver.Chrome(service=Service(chromedriver), options=options)

    thread1 = []
    thread2 = []
    for keyword in tqdm(keywordList,
                        total=len(keywordList),  ## 전체 진행수
                        desc='Keyword ProgressBar',  ## 진행률 앞쪽 출력 문장
                        ascii=' =',  ## 바 모양, 첫 번째 문자는 공백이어야 작동
                        leave=True,  ## True 반복문 완료시 진행률 출력 남김. False 남기지 않음.
                        ):
        t1 = threading.Thread(target=crawling_func, args=(keyword, newsCount, pressList1, q_dict,))
        t2 = threading.Thread(target=crawling_func, args=(keyword, newsCount, pressList2, q_dict,))

        thread1.append(t1)
        thread2.append(t2)

        t1.start()
        t2.start()

    for i, j in zip(thread1, thread2):
        i.join()
        j.join()

    news_dict = {}
    dict_idx = 0

    for i in q_dict.queue:
        for j in i.values():
            news_dict[dict_idx] = j
            dict_idx += 1

    # driver.quit()
    print('=' * 25 + "Finish Crawling" + '=' * 25)

    # 유사도 선별 전 데이터셋 엑셀 저장
    rtef.result_to_excel(news_dict, dict_idx, keywordList)

    # 유사도 선별 후 데이터셋 엑셀 저장
    # nraf.news_relation_analysis(news_dict)

    # 유사도 선별 후 데이터베이스에 저장

