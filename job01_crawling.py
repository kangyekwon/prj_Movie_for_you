#크롤링, 데이터 가져오기 먼저
# 영화를 보고 그 영화와 비슷한 리뷰가 있는 영화들을 찾아줌.

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

#https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2021&page=1
#페이지는 1~37

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'

your_year = 2020 #할당받은 연도로 수정하세요

for i in range(1, 38):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, i)
    titles = []
    reviews = []
    try:
        # driver.get(url)
        time.sleep(0.5)
        for j in range(1, 21):
            driver.get(url)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)

            try:
                title = driver.find_element('xpath', movie_title_xpath).text
                driver.find_element('xpath', movie_title_xpath).click()
                time.sleep(0.5)
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(0.5)
                review_range = driver.find_element('xpath', review_number_xpath).text
                review_range = review_range.replace(',', '')

                review_range = int(review_range)-1 // 10 + 2

                for k in range(1, review_range):
                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]'.format(k)
                    try:
                        driver.find_element('xpath', review_page_button_xpath).click()
                        for l in range(1, 11):
                            back_flag = False
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(l)
                            try:
                                review = driver.find_element('xpath', review_title_xpath).click()
                                back_flag = True
                                time.sleep(0.5)
                                review = driver.find_element('xpath', review_xpath).text

                                titles.append(title)
                                reviews.append(review)
                                #뒤로 가기 한번
                                driver.back()
                            except:
                                if back_flag:
                                    driver.back()

                                print('review', i, j, k, l)
                        driver.back()
                    except:

                        print('review page', i, j, k)
                df = pd.DataFrame({'title':titles, 'reviews':reviews})
                df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, i), index=False)
            except:
                print('movie', i, j)
    except:
        print('page', i)

driver.close()
