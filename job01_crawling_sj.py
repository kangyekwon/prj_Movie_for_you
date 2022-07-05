
#크롤링, 데이터 가져오기 먼저
# 영화를 보고 그 영화와 비슷한 리뷰가 있는 영화들을 찾아줌.

# categories = [2017, 2018, 2019, 2020, 2021, 2022]
# pages = [53, 50, 43, 37, 38, 19]


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import columns as columns

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options) #옵션을 줘야함


review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]' # 본문 내용

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a' #리뷰
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em' #리뷰건수
# 바뀌지 않으니 변수로 설정
your_year = 2020

for i in range(1,3) : #38
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, i)
    titles = []
    reviews = []
    try :
        # driver.get(url)
        # time.sleep(0.5)
        for j in range(1, 3) : #21
            driver.get(url)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            try :
                title = driver.find_element("xpath", movie_title_xpath).text
                # find_element로 xpath 기입하는 방법이 바뀜
                driver.find_element("xpath", movie_title_xpath).click() # 클릭하는 방법
                time.sleep(0.5)
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(0.5)
                review_range = driver.find_element('xpath', review_number_xpath).text
                review_range = review_range.replace(',', '') #숫자의 , 지우기
                review_range = (int(review_range)-1)//10+2  #int로 변경하고 리뷰페이지 선정

                for k in range(1, review_range) : #review_range
                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]/span'.format(k)
                    try :
                        driver.find_element('xpath', review_page_button_xpath).click()
                        for l in range(1,11) :
                            back_flag = False #클릭 못하면 false
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(l)
                            try :
                                review = driver.find_element('xpath', review_title_xpath).click()
                                back_flag = True #클릭하면 true
                                time.sleep(0.5)
                                review = driver.find_element('xpath', review_xpath).text
                                titles.append(title)
                                reviews.append(review) # append 는 한꺼번에 진행
                                driver.back()
                            except :
                                if back_flag : #클릭해서 들어온 경우만 back
                                    driver.back()
                                print('review', i, j, k, l)
                        driver.back()
                    except :
                        print('review page', i, j, k)
            except :
                print('movie', i, j)
        df = pd.DataFrame({'title':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, i), index=False)
    except :
        print('page :', i)
driver.close() #끝까지 진행하게
    # finally :
    #     pass
        # driver.close()




