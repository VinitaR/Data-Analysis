import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#display_settings
pd.options.display.max_columns = 50
desired_width = 600
pd.options.display.max_rows = 500
pd.set_option('display.width', desired_width)
pd.options.display.float_format = '{:.0f}'.format


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

data = pd.read_csv('ac.csv')  #input the file name ac_data
# data = data.loc[8532:8566]
#remove the nodes not required
data = data[data.id != 'a0']
data = data[data.id != 'a6']
data = data[data.id != 'c2']
data = data[data.id != '4e']
data = data[data.id != 'a2']

###### enter the time difference between consecutive data
time_difference = 61 # in seconds

data = data.reset_index(drop = True) # false to see both indexes,true to see new index
data.reindex(index = range(1,len(data)))


print(data.to_csv('ac_data_after_filter.csv'))
#check on utc length
data['utc'] = data['utc'].astype(str)
data['utc_new']= data['utc'].str.len()
# print('length of utc more than 10 digits','\n',data[data['utc_new'] >10])
data.drop(data[data['utc_new'] >10].index, inplace=True)
data.drop('utc_new',axis=1,inplace=True)
data['utc'] = pd.to_numeric(data['utc'])


duplicateRows = data[data.duplicated()]
data.drop_duplicates(inplace=True) #duplicates
data.dropna(axis = 0,how='any',inplace=True) #null values
data.loc[data['temp'] > 50, 'temp'] = 0 #constraint on temp
data.loc[data['humidity'] > 100 , 'humidity'] = 0 #constraint on humidity


data.sort_values('utc' , inplace=True , ascending=True) #sort_the_data_based_on_utc

utc_list = list(data.utc)
# print(data.utc)


newlst_utc = []
for i in range(len(data.utc)-1):
    # print(i+1)
    if utc_list[i + 1] - utc_list[i] <= time_difference: #seconds after which data is coming
        newlst_utc.append(utc_list[i])  #1 data less than total will be appended
print(newlst_utc)
# print(newlst_utc)
data.loc[len(data.utc)+1] = [1000000000,'04-10-2019',-1,20,	100,0,6] ########
newlst_utc.append(1000000000)
data1 = pd.DataFrame()
for j in newlst_utc:
    data1 = data.loc[data['utc'].isin(newlst_utc)] ##data_whole



# print('data',data1)

# data = data.reset_index(drop = True) # false to see both indexes,true to see new index
# data.reindex(index = range(1,len(data)))
# print('Original data : \n',data) #head(100)

list_id = data1.id  # = data_whole.id

flag = 0
list_un = []
index = []
print('list id',list_id.tail(10))


################ make list of unique elemnts
print(data1.tail(10))
# data1 = data1.tail(10)
# print(data1)

uniq_id = list(data1.id.unique())
uniq_id.remove(-1)
print('len of uniq id',len(uniq_id))

to_replace = uniq_id
print('to_replace: ',to_replace)
value = list(range(1,len(uniq_id)+1))
print('replace by:', value)



list_id = data1.id
# print('list id',list_id)
# list_id = list_id.replace(to_replace= ['a1','a3','a5','a7','a8','a9'] , value = [1,3,5,7,8,9]) ######
list_id = list_id.replace(to_replace= uniq_id , value = list(range(1,len(uniq_id)+1)))
print('id after replacing',list_id)


n_sen = len(uniq_id) #num of sensor ##########
# print('num of sensor',n_sen)

tc = 1 #column
dat_tot = np.zeros((tc ,n_sen))
# print('dat_tot',dat_tot )
m = np.zeros((1,n_sen)) #4,1
# print('m',m)
sensor_data = 1
i=0
count = 0
# while (sensor_data!=0):
while (sensor_data>0):
    while (count<1):

        for p in list_id:
            sensor_data = p
            sensor_data = float(sensor_data)
            # print('new_data',sensor_data)


            if sensor_data == -1:
                break


            for k in range(0,n_sen): #0,1,2,3
                # print('k',k)
                # print('data', sensor_data)

                if(dat_tot[tc-1][k] == sensor_data):
                    # print('hi')
                    count=count+1
                    tc=tc+1

                    dat_tot = np.vstack((dat_tot, m))
                    i=0

            # print('tc-1',tc-1)
            # print('i',i)
            dat_tot[tc-1][i]=sensor_data
            i=i+1

    count=0

print('final matrix \n',dat_tot)
print('shape : ', dat_tot.shape)


################# making it list and converting back to node names
# final_id_list  = dat_tot.tolist()
# print('final list id',final_id_list)


id_list_1  = dat_tot.tolist()
# print('final list id',id_list_1)

################# making it list and converting back to node names
flatten_list = [j for sub in id_list_1 for j in sub]  ######flatten 2d to 1 d
# print('flatten list', flatten_list)
flatten_list_series = pd.Series(flatten_list)
flatten_id_series = flatten_list_series.replace(to_replace= list(range(1,len(uniq_id)+1)) , value = uniq_id )
flatten_id_series = flatten_id_series.replace(to_replace= 0 , value='missing' )
flatten_id = flatten_id_series.tolist()
print('flatten_id :',flatten_id)


################# missisng elements

index_missing= []
for p in range(len(flatten_id)):
    if flatten_id[p] == 'missing':
        index_missing.append(p)

    if flatten_id[p] == -1:
        index_missing.append(p)

data_missing = []


#@@@@@@@@@@@@@@@@@@@@@@@@@
data1['flag']= '0'


list_un = []
index = []

seq = list(uniq_id)

def insert_row(row_num, df, row_value):
    df1 = df[0:row_num].copy()
    df2 = df[row_num:].copy()
    df1.loc[row_num] = row_value
    df = pd.concat([df1,df2])
    df.index = [*range(df.shape[0])]
    return df



for j in range(0,len(flatten_id),6): # 6 elements at a time, then put 6
    a= (flatten_id[j : j+6]) # 6 elements at a time, then put 6
    a = list(a) #a is list
    # print(a)




    if Counter(seq) == Counter(a):

        index.append(j)
        list_un.append(a)

    elif Counter(seq) != Counter(a):
        for i in a:
            occurance = a.count(i)
            # print('occur',occurance)
        li1 = seq
        li2 = a

        def diff(li1,li2):
            return(list(set(li1) - set(li2))) #node_missing

        absent = diff(li1,li2)
        # print('absent',absent)

        total_missing = len(absent)
        # print('total_missing', total_missing)


        # print('index missing',j)

        index.append(-1) #for missing append -1
        list_un.append('missing value %s'%absent)
        data_missing.append(absent)
# print(data_missing)

new_data_miss = []
for i in data_missing:
    for new_ind in i:
        new_data_miss.append(new_ind)


print('new data missing :',new_data_miss)
print('index missing:',index_missing)


############## function call

for j in range(len(index_missing)):
    row_value = [np.nan, np.nan, new_data_miss[j], np.nan, np.nan, np.nan, np.nan, 1]
    data1 = insert_row(index_missing[j], data1, row_value)
# print(data1.tail(10))
# pd.DataFrame(data1).to_csv('ac_data_new.csv')

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
## linear interpolation

data_i = None
columns = ['utc', 'id', 'temp', 'humidity', 'luminous', 'volt', 'flag']
data_final = pd.DataFrame(columns=columns)

for i in uniq_id:
    data_i = data1.loc[data1.id == i, ['utc', 'id', 'temp', 'humidity', 'luminous', 'volt', 'flag']].copy()
    data_i = (data_i.interpolate(method='linear', limit_direction='both'))
    # print('node wise data: \n',data_i)
    data_final = data_final.append(data_i, ignore_index=True)
    # data_final = (pd.concat([data_i] , ignore_index=True))
    print('concat data \n', data_final)


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
print(p)
data_final1 = data_final.loc[p, :]
print(data_final1)

data_final1 = data_final1.reset_index(drop=True)  # false to see both indexes,true to see new index
data_final1.reindex(index=range(1, len(data_final1)))
# print(data_final1)
# data_final1.to_csv('ac_without_common_utc.csv')
##############@@@@@@@@@@@@@@@@@@@@@@@@@@@@  common utc

for i in range(0, len(data_final1), len(uniq_id)):
    data_final1.loc[i:i + (len(uniq_id)-1), 'utc'] = (data_final1['utc'][i]).copy()

print(data_final1['utc'].head(12))
# data_final1.to_csv('ac_final_sorted.csv')


# print(data_final1['utc'].dtype)

data_final1['date_time'] = pd.to_datetime(data_final1['utc'],unit='s')
timestampStr = data_final1['date_time'].dt.strftime("%d-%m-%Y %H:%M:%S")
print(timestampStr)

data_final1['date'] = timestampStr.str.slice(start= 0 , stop = 10,step=1)


data_final1['time'] = timestampStr.str.slice(start= 11 , stop = 19,step=1)
data_final1.drop(['date_time'] , axis=1 , inplace = True)
print(data_final1.head(24))
data_final1.to_csv('ac_final_imputed.csv')



