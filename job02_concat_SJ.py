import pandas as pd
import glob
df = pd.DataFrame()
data_paths = glob.glob('./crawling_data/MR_2022/*')

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
my_year = 2022
df.to_csv('./crawling_data/reviews_{}.csv'.format(my_year), index=False)