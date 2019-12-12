#data should have field names: utc,timestamp,date,id,temp,humidity,luminous,volt
#put the value for time difference
#put the nodes which should not be included in data


import pandas as pd
import numpy as np
from collections import Counter


#display_settings
pd.options.display.max_columns = 50
desired_width = 600
pd.options.display.max_rows = 500
pd.set_option('display.width', desired_width)
pd.options.display.float_format = '{:.0f}'.format
np.set_printoptions(formatter={'float_kind':'{:.0f}'.format})


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
data = pd.read_csv('ac.csv')#march_utc,read the raw file
# data = data.loc[8532:8567]
# print(data.head(20))
data = data[data.id != 'a0']
data = data[data.id != 'a6']
data = data[data.id != 'c2']
data = data[data.id != '4e']
data = data[data.id != 'a2']
# data1.to_csv('filter.csv')

#@@@@@@@@ enter the time difference between consecutive data
time_difference = 61 # in seconds

data = data.reset_index(drop = True) # false to see both indexes,true to see new index
data.reindex(index = range(1,len(data)))
# print('df2',data)
# print('data',data.head(10))

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

newlst_utc = []
for i in range(len(data.utc)-1):
    # print(i+1)
    if utc_list[i + 1] - utc_list[i] <= time_difference: #seconds after which data is coming
        newlst_utc.append(utc_list[i])  #1 data less than total will be appended
        # print(newlst_utc)

# print(len(data.utc)+1)
data.loc[len(data.utc)+1] = [1000000000,'04-10-2019',-1,20,	100,0,6] ########
newlst_utc.append(1000000000)
# print(newlst_utc)
# print(data.head(20))

data1 = pd.DataFrame()
for j in newlst_utc:
    data1 = data.loc[data['utc'].isin(newlst_utc)] ##data_whole

# print('data',data1)

data1 = data1.reset_index(drop = True) # false to see both indexes,true to see new index did data1 from data
data1.reindex(index = range(1,len(data)))
# print('Original data : \n',data1) #head(100)

flag = 0
list_un = []
index = []
# print('list id',list_id.tail(10))

dataf = pd.DataFrame()
dataf['utc'] = data1.utc
dataf['id'] = data1.id
print('utc and id \n',dataf.head(10))

################ make list of unique elements
uniq_id = list(data1.id.unique())
uniq_id.remove(-1)
# print('len of uniq id',len(uniq_id))

to_replace = uniq_id
# print('to_replace: ',to_replace)
value = list(range(1,len(uniq_id)+1))
# print('replace by:', value)

list_id = data1.id
list_id = list_id.replace(to_replace= uniq_id , value = list(range(1,len(uniq_id)+1)))
# print('id after replacing',list_id)


################# missisng elements
n_sen = len(uniq_id) #num of sensor ##########
# print('num of sensor',n_sen)

tc = 1 #column
utc_list = dataf['utc'].to_list()
dat_tot = np.zeros((tc ,n_sen))
utc_tot = np.zeros((tc,n_sen))
# print('dat_tot',dat_tot )
# print('utc_tot',utc_tot)
m = np.zeros((1,n_sen)) #4,1
# print('m',m)
sensor_data = 1
i=0
count = 0
# while (sensor_data!=0):
while (sensor_data>0):
    while (count<1):


        for p in range(len(list_id)):
            sensor_data = list_id[p]
            sensor_data = float(sensor_data)

            if sensor_data == -1:
                break
            # print('new_data',sensor_data)
            # print('index:',list_of_list_id.index(p)) #####


            for k in range(0,n_sen): #0,1,2,3
                # print('k',k)
                # print('data', sensor_data)

                if(dat_tot[tc-1][k] == sensor_data):
                    # print('hi')
                    count=count+1
                    tc=tc+1

                    dat_tot = np.vstack((dat_tot, m))
                    utc_tot = np.vstack((utc_tot, m))
                    i=0

            # print('tc-1',tc-1)
            # print('i',i)
            # print('sensor_data:',sensor_data)
            dat_tot[tc - 1][i] = sensor_data

            utc_tot[tc - 1][i] = utc_list[p]
            i=i+1

    count=0

print('final matrix \n',dat_tot)
print('final matrix utc \n',utc_tot)

discard_utc = []
keep_utc = []
for i in utc_tot:
    if (0 in i) or (1000000000 in i):
        discard_utc.append(i)
    else :keep_utc.append(i)

discard_id = []
keep_id = []
for i in dat_tot:
    if (0 in i) or (-1 in i):
        discard_id.append(i)
    else:
        keep_id.append(i)

# print('discard id:',discard_id)
# print('discard utc', discard_utc)
# print('keep id:',keep_id)
# print('keep utc:',keep_utc)


a_utc = [c for i in keep_utc for c in i]
# print('total number of utc',(a_utc))
a_id = [c for i in keep_id for c in i]
# print('total number of ids',(a_id))


data_new = pd.DataFrame()
data_new['utc'] = a_utc
data_new['id'] = a_id
data_new['id'] = data_new['id'].replace(to_replace =list(range(1,len(uniq_id)+1)) , value = uniq_id )
# print(data_new)


df1 = data1
df2 = data_new
keys = list(df2.columns.values)
i1 = df1.set_index(keys).index
i2 = df2.set_index(keys).index
data_final = df1[i1.isin(i2)]

data_final = data_final.reset_index(drop = True)
data_final.reindex(index = range(1,len(data)))
print('final: \n',data_final)


##common utc
for i in range(0, len(data_final), len(uniq_id)):
    data_final.loc[i:i + (len(uniq_id)-1), 'utc'] = (data_final['utc'][i]).copy()

print(data_final['utc'].head(12))

print(data_final.to_csv('ac_missing.csv'))















