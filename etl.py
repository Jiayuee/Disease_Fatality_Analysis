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


ip = "data.pkl"
df = pd.read_pickle(ip)

# df0: patient died within 1 year
# df1: patient died at the next year
df0 = df.drop_duplicates(subset=['identifier'], keep = 'last')
dcd = []
# get name list of all dCD code
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

# proportion for situation 1:
# the patient died at the year of getting that disease
pt_num, death, prop = [], [], []
for d in d_list:
    pt_num.append(get_patient_num(d))
    death.append(get_death_num(d))
    prop.append(get_death_num(d)/get_patient_num(d))

p1 = pd.DataFrame({'disease':d_list, 'pt_num':pt_num,
                    'death':death, 'proportion':prop})
