import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
review_word.info()

cleaned_token_reviews = list(review_word['review'])
print(cleaned_token_reviews[0])

cleaned_tokens = []
for sentence in cleaned_token_reviews:
    token = sentence.split()
    cleaned_tokens.append(token)
print(cleaned_tokens[0])

embedding_model = Word2Vec(cleaned_tokens, vector_size=100,
                           window=4, min_count=20,
                           workers=4, epochs=100, sg=1)
embedding_model.save('./models/word2vec_2017_2022_movies.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))



#워드 임배딩 , 비슷한단어들을 같은공간에/ 백터, 백터공간상에 단어배치 . 차원축소 필수
#
# import pandas as pd
# from gensim.models import Word2Vec
#
# #pip install gensim
#
# review_word = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
# review_word.info()

# cleaned_token_reviews = list(review_word['reviews'])
# print(cleaned_token_reivew[0])
#
# cleaned_tokens = []
# for sentence in cleaned_token_reviews:
#     token = sentence.split()
#     cleaned_tokens.append(token)
# print(cleaned_tokens[0])
#
# #문장단위로 주는건 맞는데 형태소들로 줘야함
#
# embedding_model = Word2Vec(cleanaed_tokens, vector_size=100,  #원래는 단어 갯수만큼 차원이 만들어져서 100차원으로줄여서 만들기
#                            window=4, min_count=20,  #윈도우는 4개씩 끊어서 학습하겟다 , 민카운트는 빈도 , 20번이상 출연하는것만 학습
#                            workers=4, epochs=100, sg=1) #에폭스는 백번 반복학습 , sg는 알고리즘
# #형태소들의 리스트로 되어있는 문장으로 넣어주기
#
# #2차원으로 차원축소해서 시각화
# embedding_model.save('./models/word2Vec_2017_2022_movies.model')
# print(list(embedding_model.wv.index_to_key))
# print(len(embedding_model.wv.index_to_key))