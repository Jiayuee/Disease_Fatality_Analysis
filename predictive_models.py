import pandas as pd
import numpy as np
import os
from pandas import DataFrame

import eli5
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import roc_auc_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor, LGBMClassifier

import statsmodels.api as sm

#### import data
ip = 'edited_data2.h5'
df = pd.read_hdf(ip,'selected_patients','r+')
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
df = df.drop(['race','identifier','dDeath'], axis = 1)

x = df.drop(sd_list, axis = 1)


#### build five models

rf = RandomForestClassifier(max_depth=3, random_state=0)
xgb = XGBClassifier()
lgbm = LGBMClassifier()  ##not tree based model1
logit = LogisticRegression()
models = [rf,xgb,lgbm,logit]

#### evaluate models and print out
# for m in models:
#     scores2 = {}
#     scores = []
#     for i in range(len(sd_list)):
#         scores2[i] = cross_val_score(m,x,df[sd_list[i]],
#                                     scoring='roc_auc', cv=5)
#         print('{}: {}: {}'.format(m.__class__.__name__, sd_list[i],np.mean(scores2[i])))
#         scores.append(np.mean(scores2[i]))
#     score = np.mean(scores)
#     print('{}: {}'.format(m.__class__.__name__,score))


#### feature importances in tree based models
for i in range(len(sd_list)):
    y = df[sd_list[i]]
    names = list(x)
    print(sd_list[i])
## for rf and xgb
    for m in [rf,xgb]:
        m.fit(x,y)
        print(m.__class__.__name__,"Features sorted by their score:")
        print(sorted(zip(map(lambda x: round(x, 3), m.feature_importances_), names),
                reverse=True))
    ## for lightgbm feature ranking
    lgbm.fit(x,y)
    print(eli5.explain_weights(lgbm))
    # for LogisticRegression coefficient
    logit_model=sm.Logit(y,x)
    result=logit_model.fit()
    print(result.summary())
