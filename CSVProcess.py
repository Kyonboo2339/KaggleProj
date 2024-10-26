import sys
import pandas as pd
import numpy as np
import csv
df = pd.read_csv('train_final.csv')
print(df)
attributeIntervals = {}
unknownReplacements = {}

#Age by quartile
i = pd.IntervalIndex(pd.qcut(df["age"], q= 4).value_counts().index)
L1 = list(zip(i.left, i.right))[:3]
age_intervals = [y for x in L1 for y in x]
age_intervals.extend([-1, 99])
attributeIntervals["age"] = age_intervals
print(df.groupby("age").size())

#fnlwgt by quartile
i = pd.IntervalIndex(pd.qcut(df["fnlwgt"], q= 4).value_counts().index)
L1 = list(zip(i.left, i.right))[:3]
fnlwgt_intervals = [y for x in L1 for y in x]
fnlwgt_intervals.extend([-1, float("inf")])
attributeIntervals["fnlwgt"] =fnlwgt_intervals

# #Split on given intervals
nonZeroMean = df[df['capital.gain'] >= 60.0].mean()
capital_gain_bounds = [-1, df["capital.gain"].mean(), nonZeroMean["capital.gain"],9999999]
attributeIntervals["capital.gain"] = capital_gain_bounds

#Split on the median
median = df["hours.per.week"].median()
hrs_per_wk_bounds = [-1, median-1, 99]
attributeIntervals["hours.per.week"] = hrs_per_wk_bounds

# #Split on given intervals
nonZeroMean = df[df['capital.loss'] >= 10.0].mean()
capital_loss_bounds = [-1, df["capital.loss"].mean(), nonZeroMean["capital.loss"],99999]
attributeIntervals["capital.loss"] = capital_loss_bounds


#Unknown in workclass replaced by mode
unknownReplacements["workclass"] = df["workclass"].mode()
#Unknown in education replaced by mode
unknownReplacements["education"]= df["education"].mode()
#Unknown in marital status replaced by mode
unknownReplacements["marital.status"] =  df["marital.status"].mode()
#Unknown in occupation replaced by mode
unknownReplacements["occupation"] = df["occupation"].mode()
#Unknown in relationship replaced by mode
unknownReplacements["relationship"] = df["relationship"].mode()
#Unknown in race replaced by mode
unknownReplacements["race"] =  df["race"].mode()
#Unknown in sex replaced by mode
unknownReplacements["sex"] =  df["sex"].mode()
#Unknown in sex replaced by mode
unknownReplacements["native.country"] =  df["native.country"].mode()





df_test = pd.read_csv('test_final.csv')
print("test before")
print(df_test)
for attribute in attributeIntervals:
    bounds = list(set(attributeIntervals[attribute]))
    list.sort(bounds)
    df_test[attribute] = pd.cut(df_test[attribute], bounds)
    df[attribute] = pd.cut(df[attribute], bounds)

#for attribute in unknownReplacements:
    #df_test[attribute].replace(to_replace=['?'], value=unknownReplacements[attribute], inplace=True)
    #df[attribute].replace(to_replace=['?'], value=unknownReplacements[attribute], inplace=True)


df_test.to_csv("test_processed.csv", sep=',', index=False, encoding='utf-8')
df.to_csv("train_processed.csv", sep=',', index=False, encoding='utf-8')
print(attributeIntervals)
print(unknownReplacements)
print("processed data")