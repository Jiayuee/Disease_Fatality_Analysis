import os
import pandas as pd
import numpy as np
import pickle
from pandas import DataFrame


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

sub_df = df.drop_duplicates(subset=['identifier'], keep = 'last')
op = pd.HDFStore('edited_data.h5')
op['latest_disease_record'] = sub_df
op['total_disease_record'] = df
