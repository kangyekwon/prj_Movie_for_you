#crawling 작업

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

your_year = 2020

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'

review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'

#네이버영화랭킹-디렉토리-개봉년도(2020) 페이지
for i in range(1, 38): # ~38
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, i)
    titles = []
    reviews = []
    try:
        #driver.get(url)
        time.sleep(0.5)
        for j in range(1, 21): # ~21
            driver.get(url)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)  #영화제목(한페이지에 20개씩 리스트업)
            try:
                title = driver.find_element("xpath", movie_title_xpath).text
                driver.find_element("xpath", movie_title_xpath).click() #영화제목클릭
                time.sleep(0.5)
                driver.find_element("xpath", review_button_xpath).click() #리뷰 탭 클릭
                time.sleep(0.5)
                review_range = driver.find_element("xpath", review_number_xpath).text #총 리뷰수
                review_range = review_range.replace(',','')
                review_range = (int(review_range)-1) // 10 + 2 #한 페이지에 리뷰 10개씩 리스트업
                for k in range(1, review_range): # ~review_range
                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]'.format(k)
                    try:
                        driver.find_element("xpath", review_page_button_xpath).click()
                        for l in range(1, 11): # ~11
                            back_flag = False
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(l)
                            try:
                                review = driver.find_element("xpath", review_title_xpath).click()
                                back_flag = True
                                time.sleep(0.5)
                                review = driver.find_element("xpath", review_xpath).text
                                titles.append(title)
                                reviews.append(review)
                                driver.back()
                            except:
                                if back_flag :
                                    driver.back()  #back_flag=True일때, drive.back()
                                print('review', i, j, k, l)
                        driver.back()
                    except:
                        print('review page', i, j ,k)
            except:
                print('movie', i, j)
        df = pd.DataFrame({'title':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, i), index=False)
    except:
        print('page', i)

driver.close()