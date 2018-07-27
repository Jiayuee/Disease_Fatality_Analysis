import pandas as pd
import numpy as np
import os
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import roc_auc_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor, LGBMClassifier

#### import data
ip = 'edited_data2.h5'
df = pd.read_hdf(ip,'selected_patients','r+')
general_info = ['age','male','race']
# lsd_list: less severe disease, sd_list: severe disease
sd_list = ['dCD_AtrFib','dCD_HeartFail','dCD_PVD','dCCI_AMI']
lsd_list = ['dCD_CHD','dCD_DM','dCD_LPD','dCD_Hyp','dCD_Renal','dCD_Rheumatoid',
            'dCD_Stroke','dCD_SuspectedStroke','dCCI_CVD','dCCI_Renal','dCCI_Rheuma']

#### clean dummy variable race
df['race'].apply(lambda x: x.split(sep='_')[1])
dummy_fields = ['race']
for each in dummy_fields:
    dummies = pd.get_dummies(df.loc[:, each], prefix=each )
    df = pd.concat( [df, dummies], axis = 1 )
df = df.drop('race', axis = 1)

x = df.drop(sd_list, axis = 1)
# y = df[sd_list[0]]

#### build five models
model1 = LinearRegression(copy_X=True)
model2 = RandomForestClassifier(max_depth=3, random_state=0)
model3 = XGBClassifier()
model4 = LGBMClassifier()
model5 = LogisticRegression()
models = [model1,model2,model3,model4,model5]

#### evaluate the models
# def evaluate_model_for_disease(disease):
#     scores1 = {} # scores1 is scores by method
#     for i in range(len(models)):
#         scores1[i] = cross_val_score(models[i], x, df[disease],
#                                 scoring='roc_auc', cv=5)
#     for i in range(len(models)):
#         print('{}: {}: {}'.format(disease,models[i].__class__.__name__, np.mean(scores1[i])))
#
# for d in sd_list:
#     evaluate_model_for_disease(d)

#### evaluate models and print out 
for m in models:
    scores2 = {}
    scores = []
    for i in range(len(sd_list)):
        scores2[i] = cross_val_score(m,x,df[sd_list[i]],
                                    scoring='roc_auc', cv=5)
        print('{}: {}: {}'.format(m.__class__.__name__, sd_list[i],np.mean(scores2[i])))
        scores.append(np.mean(scores2[i]))
    score = np.mean(scores)
    print('{}: {}'.format(m.__class__.__name__,score))
