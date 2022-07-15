import pandas as pd
from numpy import empty
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec





#코사인 값이 가장 큰(유사한 값 ) 열개 찾아서 출력
def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore] #인덱스만 뽑아내기. 인덱스를 무비인덱스로 받기
    recMovieList = df_reviews.iloc[movieIdx, 0]
    return recMovieList



df_reviews = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()

with open('./models/tfidf.pickle', 'rb')  as f:     #읽어오기
    Tfidf = pickle.load(f)

# #영화제목 / index를 이용
# ## movie_idx=1003
# movie_idx = df_reviews[df_reviews['titles']=='겨울왕국 2 (Frozen 2)'].index[0] #인덱스확인
#
# ## print(movie_idx)
# ## print(df_reviews.iloc[1228, 1])
#
# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# keyword 이용

embedding_model = Word2Vec.load('./models/word2vec_2017_2022_movies.model')
keyword = '스파이더맨'
sim_word = embedding_model.wv.most_similar(keyword, topn=10) #심워드는 유사단어 ,유사값나옴
words = [keyword]
for word, _ in sim_word:
    words.append(word)
sentence=[]
count = 10
for word in words:
    sentence = sentence + [word] * count
    count -= 1
print(sentence)
sentence = ' '.join(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation[:10])

# sentence = [wrods[0]] * 10 + [words[1]] * 9 + # 키워드를 열개 넣는다, 문자열이라 리스트에 넣어주기 [],


