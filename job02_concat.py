#합치는 방법

import pandas as pd
import glob


df = pd.DataFrame()
data_paths = glob.glob('./crawling_data/MR_2017/*')
# print(data_paths)


for path in range(1, 38):
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True) #난값제거
    df = pd.concat([df, df_temp], ignore_index=True) #중복제거

#합친다음 중복이 있을수도있으니 ,중복제거 한번더

df.drop_duplicates(inplace=True)
df.info()
my_year = 2017
df.to_csv('./crawling_data/reviews_{}.csv'.format(my_year))
#팀원은 합쳐진 파일 깃 > 에드 > 방장이 확인 pr

