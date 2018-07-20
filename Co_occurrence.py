import os
import pandas as pd
import numpy as np
import pickle
from pandas import DataFrame

#### import edited_data
ip = "edited_data.h5"
op = pd.HDFStore('Co_occurence.h5')
df = pd.read_hdf(ip,'total_disease_record','r+')
sub_df = pd.read_hdf(ip,'latest_disease_record','r+')


# select part of the dataframe
cols = ['dCCI_Dementia','dCD_Dementia','dCD_Hyp']
df_c = sub_df[cols]
c_matrix = np.dot(df_c.transpose(),df_c) # cooccurrence_matrix
c_mx_dia = np.diagonal(c_matrix) # cooccurrence_matrix_diagonal
with np.errstate(divide='ignore', invalid='ignore'):
    c_mx_per = np.nan_to_num(np.true_divide(c_matrix, c_mx_dia[:, None]))
    # cooccurrence_matrix_percentage


#
# def get_cooccurence(d1,d2):
#     cols = ['identifier',d1,d2]
#     df_d = df[cols]
#     df_d = df_d.set_index(np.arange(len(df_d)))
#     d1_num,d2_num,co_num = 0,0,0
#     uncertain_num = 0 # cooccurence without previous record
#     if df_d[d2][0] == 1:# the first record of d2 is positive
#         if df_d[d1][0] == 1:# the firsr record of d1 is also positive
#             uncertain_num1 += 1
#     for i in range(1,len(df_d)):
#         c0 = df_d['identifier'][i-1] == df_d['identifier'][i] # same patient
#         c1 = df_d[d2][i-1] == 0 # patient does not has d1 las year
#         c2 = df_d[d2][i] == 1 # patient has d2 this year
#         c_d2 = c0 & c1 & c2 # patient gets d2 this year
#         c3 = df_d[d1][i-1] == 0 # patient does not has d1 last year
#         c4 = df_d[d1][i] == 1 # patient has d1 this year
#         c_d1 = c0 & c3 & c4 # patient gets d1 this year
#         if c_d1:
#             d1_num += 1
#         if c_d2:
#             d2_num += 1
#         if c_d1 & c_d2:
#             co_num += 1
#     d1_num.append(d1_num)
#     d2_num.append(d2_num)
#     co_num.append(co_num)
#     uncertain_nums.append(uncertain_num)
#     return
