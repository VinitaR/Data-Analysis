import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#display_settings
pd.options.display.max_columns = 50
desired_width = 600
pd.options.display.max_rows = 500
pd.set_option('display.width', desired_width)
# pd.options.display.float_format = '{:.0f}'.format

data = pd.read_csv('ac_final_imputed.csv',usecols=['utc','id','temp','humidity','luminous','volt','flag']) #ac_final_sorted_if
diff = []



def insert_row(row_num, df, row_value):  #row num,dataset,row value
    df1 = df[0:row_num].copy()
    df2 = df[row_num:].copy()
    df1.loc[row_num] = row_value
    df = pd.concat([df1,df2])
    df.index = [*range(df.shape[0])]
    return df


# print(data.head(10))
uniq_id = list(data['id'].unique())
print(uniq_id)
# print(data.describe())
# print(data.dtypes)


for j in range(0, len(data)-1):
    print(data['utc'][j + 1] , data['utc'][j])
    d = data['utc'][j + 1] - data['utc'][j]
    if (d) >100:
        diff.append(j + 1)
print('difference',diff)
print('length',len(diff))
print(Counter(diff))

diff1= []
for i in range(len(diff)):
    diff1.append(diff[i]+ len(uniq_id)*i)

print('diff1:',diff1)

for j in range(len(diff1)):

    for k in range(len(uniq_id)):
        # print(k, uniq_id[k])
        row_value = [np.nan, uniq_id[k], np.nan, np.nan, np.nan, np.nan, 1]
        data = insert_row(diff1[j], data, row_value)
# print('inserted \n:',data.head(10))
# print(data.to_csv('inserted_new.csv'))

############# function call
data_i = None
columns = ['utc', 'id', 'temp', 'humidity', 'luminous', 'volt', 'flag']
data_final = pd.DataFrame(columns=columns)

print('unique id',uniq_id)
for i in uniq_id:
    # print('data_1',data)
    data_i = data.loc[data.id == i, ['utc', 'id', 'temp', 'humidity', 'luminous', 'volt', 'flag']].copy()
    data_i = (data_i.interpolate(method='linear', limit_direction='both'))
    # print('node wise data: \n',data_i.head(100))
    data_final = data_final.append(data_i, ignore_index=True)
    
# print('concat data \n', data_final.tail(10))
# print(data_final.to_csv('imputed.csv'))



data_final2 = pd.DataFrame(columns=columns)

id_index = []
for i in uniq_id:
    id_index.append(data_final.id.ne(i).idxmin())
print(id_index)

p = []
for i in range(len(data_i)):
    for j in id_index:
        # print(j,i)
        p.append(j + i)
# print(p)
data_final1 = data_final.loc[p, :]
# print(data_final1)

data_final1 = data_final1.reset_index(drop=True)  # false to see both indexes,true to see new index
data_final1.reindex(index=range(1, len(data_final1)))
# print(data_final1)



data_final1['date_time'] = pd.to_datetime(data_final1['utc'],unit='s')
timestampStr = data_final1['date_time'].dt.strftime("%d-%m-%Y %H:%M:%S")
# print(timestampStr)

data_final1['date'] = timestampStr.str.slice(start= 0 , stop = 10,step=1)


data_final1['time'] = timestampStr.str.slice(start= 11 , stop = 19,step=1)
data_final1.drop(['date_time'] , axis=1 , inplace = True)
print(data_final1.head(24))
data_final1.to_csv('ac_final_imputed_all_instances.csv')

