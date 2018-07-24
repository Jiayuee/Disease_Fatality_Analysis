import os
import pandas as pd
import numpy as np
import pickle
from pandas import DataFrame

#### import dataframe
ip = "data.pkl"
op = pd.HDFStore('Proportions2.h5')
df = pd.read_pickle(ip)
df = df.sort_values(['identifier','year'])
df = df.set_index(np.arange(len(df)))

## select subset of dataframe
d_list = ['dCD_AtrFib','dCD_CHD','dCD_DM','dCD_LPD','dCD_HeartFail','dCD_Hyp',
            'dCD_PVD', 'dCD_Renal','dCD_Rheumatoid', 'dCD_Stroke','dCD_SuspectedStroke',
            'dCCI_AMI','dCCI_CVD','dCCI_Renal','dCCI_Rheuma']
cols = ['identifier','year','dDeath','age','male','race'] + d_list
df = df[cols]
sub_df = df.drop_duplicates(subset=['identifier'], keep = 'last')

df2 = pd.DataFrame()
for i in sub_df['identifier']:
    idx = df['identifier'] == i
    if len(df[idx]) > 1:
        df2 = df2.append(df[idx])
op = pd.HDFStore('edited_data2.h5')
op['latest_disease_record'] = sub_df
op['total_disease_record'] = df
op['selected_patients'] = df2
