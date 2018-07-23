import os
import pandas as pd
import numpy as np
import pickle
from pandas import DataFrame

#### import edited_data
ip = "edited_data2.h5"
op = pd.HDFStore('Co_occurence2.h5')
df = pd.read_hdf(ip,'total_disease_record','r+')
sub_df = pd.read_hdf(ip,'latest_disease_record','r+')


# select part of the dataframe
# drop_cols = ['year','identifier','dDeath']
cols = list(df)[3:]
df_c = df[cols]
# np.set_printoptions(precision=3)
c_matrix = np.dot(df_c.transpose(),df_c) # cooccurrence_matrix
c_mx_dia = np.diagonal(c_matrix) # cooccurrence_matrix_diagonal
with np.errstate(divide='ignore', invalid='ignore'):
    c_mx_per = np.nan_to_num(np.true_divide(c_matrix, c_mx_dia[:, None]))
    # cooccurrence_matrix_percentage
# pd.set_option('display.max_rows', 999)
pd.set_option('precision', 3)
c = pd.DataFrame(c_mx_per)
