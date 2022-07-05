
#크롤링, 데이터 가져오기 먼저
# 영화를 보고 그 영화와 비슷한 리뷰가 있는 영화들을 찾아줌.

# categories = [2017, 2018, 2019, 2020, 2021, 2022]
# pages = [53, 50, 43, 37, 38, 19]

import columns as columns
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
review_number_xpath =  '//*[@id="reviewTab"]/div/div/div[2]/span/em'
review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'                   #review button
#                      //*[@id="movieEndTabMenu"]/li[6]/a
your_year = 2018 # 할당받은 연도로 수정하세요.
for i in range(17, 18): #38
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, i)
    titles = []
    reviews = []
    try:
        for j in range(1, 21): #21
            driver.get(url)
            time.sleep(1)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            try:
                title = driver.find_element("xpath", movie_title_xpath).text
                driver.find_element("xpath", movie_title_xpath).click()
                time.sleep(1)
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(1)
                review_range = driver.find_element('xpath', review_number_xpath).text
                review_range = review_range.replace(',', '')
                review_range = (int(review_range)-1) // 10 + 2
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
                                time.sleep(1)
                                review = driver.find_element('xpath', review_xpath).text
                                titles.append(title)
                                reviews.append(review)
                                driver.back()
                            except:
                                if back_flag:
                                    driver.back()
                                print('review', i, j, k, l)

                        driver.back()
                    except:
                        print('review page', i, j, k)
            except:
                print('movie', i, j)
        print(len(titles))
        df = pd.DataFrame({'title':titles, 'reviews':reviews})
        print('debug01')
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, i), index=False)
        print('debug02')
    except:
        print('page', i)

driver.close()




