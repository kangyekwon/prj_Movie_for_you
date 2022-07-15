#시각화

import pandas as pd
import matplotlib.pyplot as plt

# pip install matplotlib
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
# pip insatll scikit-learn

import matplotlib as mpl

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False #-값 업애야함
rc('font', family=font_name) #폰트적용

embedding_model = Word2Vec.load('./models/word2vec_2017_2022_movies.model')
key_word = '믿음'
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
print(sim_word)

#시각화
vectors = []
labels = []

##차원축소 / #심워드는 라벨과 값니아모 라벨만 받을꺼라 뒤에는 언더바로 처리
for label, _ in sim_word: #처음 형태 예를들어 살아가다의 형태소가 백터값에 들어가고 , 100차원 좌표 10개들어감
    labels.append(label)
    vectors.append(embedding_model.wv[label])

print(vectors[0])
print(len(vectors[0]))

df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())

tsne_model = TSNE(perplexity=40, n_components=2 , init='pca', n_iter=2500) # 2차원으로 축소 >pca
new_value = tsne_model.fit_transform(df_vectors)
df_xy = pd.DataFrame({'words':labels,
                      'x':new_value[:, 0],
                      'y':new_value[:, 1]})


print(df_xy)
print(df_xy.shape)
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)

plt.figure(figsize=(8,8))
plt.scatter(0, 0, s=1500, marker='*')

for i in range(len(df_xy)-1):
    a= df_xy.loc[[i, 10]]
    plt.plot(a.x, a.y, '-D', linewidth=1)
    plt.annotate(df_xy.words[i], xytext=(1, 1),#글씨쓰기
                 xy=(df_xy.x[i], df_xy.y[i]), #좌표주기
                 textcoords='offset points', #옵셋 살짝떄기
                 ha='right', va='bottom') #수평정렬, 수직정렬

plt.show()
