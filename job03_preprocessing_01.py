

from unittest.mock import inplace

import pandas as pd
import stopwords as stopwords
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/reviews_2018.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords = list(df_stopwords['stopword'])


cleaned_sentences = []
for review in df.reviews:
    review = re.sub('[^가-힣 ]', ' ', review)
    token = okt.pos(review, stem=True) # 튜플로 묶어줌

    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
    words = []
    for word in df_token.word:
        if len(word) > 1:
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]
df.dropna(inplace=True)

df.to_csv('./crawling_data/cleaned_review_2018.csv', index=False)
df.info()



# from unittest.mock import inplace
#
# import pandas as pd
# import stopwords as stopwords
# from konlpy.tag import Okt
# import re
#
# df=pd.read_csv('./crawling_data/reviews_2020.csv')
# df.info()
#
# #형태소분리 먼저
# okt = Okt()
#
#
#
# #첫번쨰 전처리 한글남기고 다 버리기.  > 불용어 버리기 (스탑워드) ,한글자버리기
# #전처리2에서는 형태소 나누고 등등
#
# df_stopword = pd.read_csv('./crawling_data/stopwords.csv')
# stopwords = list(df_stopwords['stopword'])
#
# token = okt.pos(df.reviews[0], stem=True)
# print(token)
# exit()
#
# cleaned_sentences = []
# for review in df.reviews:
#     count += 1
#     if count % 10 == 0:
#         print('.', end='')
#     if count % 100 == 0:
#         print()
#
#
#
#     review = re.sub('[^가-힣 ]', ' ', review)  #^이 있어야 이거 뒤에꺼 뺴고 나머지 지우기임, ^없으면 가-힣 다지움
#     #형태소분리하기
#     token = okt.pos(review, stem=True) # morphs 몹스 형태소 짤라주는애 . 기존사용함, pos는 짤라준후 ,형태소의 품사까지 알려줌. 딕션어리형태임(튜플로)
#
#     #동사 명사 부사만 남기기 > 데이터프레임 먼저 만들기 , 형태소와 품사 2가지로 됨
#     df_token = pd.DataFrame(token, columns=['word','class'])
#     df_token = pd_token[(df_token['class']=='Noun')
#                         (df_token['class']=='Verb')
#                         (df_token['class']=='Adjective')]
#     #부용어제거하기
#     words = []
#     for word in df_token.word:
#         if len(word) > 1:
#             if word not in stopwords:
#                 words.append(word) #워드에다가 넣기
#
#
#     #한문장으로 팝치기, 형태소들을 띄어쓰기 기준으로 합치기
#     cleaned_sentence = ' '.join(words) #한글만, 명사 동사 수식어만, 한글자 짜리 없음 ,스톱워드제거상태로 다시 이어 붙이기
#     #아까 만들어 놓은 빈 리스트에 넣기
#     cleaned_sentence.append(cleaned_sentence)
# df['cleaned_sentences'] = cleaned_sentences
# df = df['title', 'cleaned_sentences']
# df.dropna(inplace=True)
#
# df.to_csv('./crawling_data/cleaned_review_2020.csv',index=False)
# df.info()
