import os
import pandas as pd
import numpy as np
import pickle
from pandas import DataFrame
from collections import Counter


def get_patient_num(disease):
    return sum(df0[disease])

def get_death_num(disease):
    idx1 = df0[disease] == 1
    idx2 = df0['dDeath'] == 1
    idx = idx1 & idx2
    return sum(idx)

def get_proportion_m2(disease):
    cols = ['identifier','dDeath',disease]
    df_d = sub_p0[cols]
    df_d = df_d.set_index(np.arange(len(df_d)))
    pt_num = 0
    death = 0
    uncertain_num1 = 0 # patient died at the year of sickness without previous record
    if df_d[disease][0] == 1:# the first record of patient is positive
        if df_d[y][0] == 1:# the patient died at the first year
            uncertain_num1 += 1
    for i in range(1,len(df_d)):
        c0 = df_d['identifier'][i-1] == df_d['identifier'][i] # same patient
        c1 = df_d[disease][i-1] == 0 # patient is not sick at the previous year
        c2 = df_d[disease][i] == 1 # patient is sick this year
        c_d = c0 & c1 & c2 # patient gets sick this year
        c3 = df_d[y][i] == 1 # patient dies this year
        c_y = c0 & c_d & c3 # patient dies due to the disease
        if c_d:
            pt_num += 1
        if c_y:
            death += 1
    if pt_num != 0:
        proportion = death/pt_num
    else:
        proportion = np.NaN
    pt_nums.append(pt_num)
    deaths.append(death)
    proportions.append(proportion)
    uncertain_num1s.append(uncertain_num1)
    return

def get_proportion_m3(disease):
    cols = ['identifier','dDeath',disease]
    df_d = sub_p0[cols]
    df_d = df_d.set_index(np.arange(len(df_d)))
    pt_num = 0
    death = 0
    uncertain_num1 = 0 # patient died at the year of sickness without previous record
    if df_d[disease][0] == 1:# the first record of patient is positive
        if df_d[y][0] == 1:# the patient died at the first year
            uncertain_num1 += 1
    for i in range(1,len(df_d)-1):
        c0 = df_d['identifier'][i-1] == df_d['identifier'][i] # same patient
        c1 = df_d[disease][i-1] == 0 # patient is not sick at the previous year
        c2 = df_d[disease][i] == 1 # patient is sick this year
        c_d = c0 & c1 & c2 # patient gets sick this year
        c3 = df_d[y][i] == 0 # patient survives this year
        c4 = df_d[y][i+1] == 1 # patient dies next year
        c_y = c0 & c_d & c3 & c4 # patient dies due to the disease
        if c_d:
            pt_num += 1
        if c_y:
            death += 1
    if pt_num != 0:
        proportion = death/pt_num
    else:
        proportion = np.NaN
    pt_nums.append(pt_num)
    deaths.append(death)
    proportions.append(proportion)
    uncertain_num1s.append(uncertain_num1)
    return


#### import data
ip = "data.pkl"
op = pd.HDFStore('Proportions.h5')
df = pd.read_pickle(ip)
df = df.sort_values(['identifier','year'])
df = df.set_index(np.arange(len(df)))

## drop irrelevant information
# get name list of all dCD code
dcd = []
for d in df.columns.values:
    if 'dCD' in d:
        dcd.append(d)

# get name list of all dCCI code
dcci = []
for d in df.columns.values:
    if 'dCCI' in d:
        dcci.append(d)
dcci.remove('Tot_dCCI')

# d_list: get disease list for all targeted disease
d_list = dcd + dcci
y = 'dDeath'
cols = ['identifier','year',y] + d_list
df = df[cols]

#### Method 1 : calculate the num of patient and num of death directly
# proportion for patients died at the year of getting that disease
# df0: patient died within 1 year
df0 = df.drop_duplicates(subset=['identifier'], keep = 'last')
# pt_num, death, prop = [], [], []
# for d in d_list:
#     pt_num.append(get_patient_num(d))
#     death.append(get_death_num(d))
#     prop.append(get_death_num(d)/get_patient_num(d))
#
# prop1 = pd.DataFrame({'disease':d_list, 'pt_num':pt_num,
#                     'death':death, 'proportion':prop})
#
# op['current_year_1'] = prop1
### exclude patients who only have one record
sub_p0 = pd.DataFrame()
for i in df0['identifier']:
    idx = df['identifier'] == i
    if len(df[idx]) > 1:
        sub_p0 = sub_p0.append(df[idx])

## Method 2 : run a loop for all rows, for patients with more than one record
# proportion for patient dies the year they get sick
# pt_nums,deaths,proportions,uncertain_num1s=[],[],[],[]
# for d in d_list:
#     get_proportion_m2(d)
# prop2 = pd.DataFrame({'disease':d_list,'pt_num':pt_nums,'death':deaths,
#                         'proportion':proportions,'uncertain_num1':uncertain_num1s})
# op['current_year_2'] = prop2

# proportion for patient dies the year next to the detection year
pt_nums,deaths,proportions,uncertain_num1s=[],[],[],[]
for d in d_list:
    get_proportion_m3(d)
prop3 = pd.DataFrame({'disease':d_list,'pt_num':pt_nums,'death':deaths,
                        'proportion':proportions,'uncertain_num1':uncertain_num1s})
op['next_year'] = prop3
