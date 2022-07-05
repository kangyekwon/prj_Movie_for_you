import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
#저장할떄 라이트 ,읽을떄 로드로 사용
import pickle

df_reviews = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['review']) #형태소들의 정보를 가지고 있게됨

print(Tfidf_matrix[0][0])
#리뷰개수와 단어들

print(Tfidf_matrix[0].shape)


with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)