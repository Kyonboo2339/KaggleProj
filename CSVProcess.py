import sys
import pandas as pd
import numpy as np
import csv
df = pd.read_csv('train_final.csv')
print(df)
attributeIntervals = {}
unknownReplacements = {}

#Age by quartile
df["age"] = pd.qcut(df["age"], q= 4)
i = pd.IntervalIndex(df["age"].value_counts().index)
L1 = list(zip(i.left, i.right))[:3]
age_intervals = [y for x in L1 for y in x]
age_intervals.extend([-1, 99])
attributeIntervals["age"] = age_intervals
#print(attributeIntervals["age"])

#fnlwgt by quartile
df["fnlwgt"] = pd.qcut(df["fnlwgt"], q= 4)
i = pd.IntervalIndex(df["fnlwgt"].value_counts().index)
L1 = list(zip(i.left, i.right))[:3]
fnlwgt_intervals = [y for x in L1 for y in x]
fnlwgt_intervals.extend([-1, float("inf")])
attributeIntervals["fnlwgt"] =fnlwgt_intervals

# #Split on given intervals
nonZeroMean = df[df['capital.gain'] >= 60.0].mean()
capital_gain_bounds = [-1, df["capital.gain"].mean(), nonZeroMean["capital.gain"],9999999]
df["capital.gain"] = pd.cut(df["capital.gain"], capital_gain_bounds)

attributeIntervals["capital.gain"] = capital_gain_bounds

#Split on the median
median = df["hours.per.week"].median()
hrs_per_wk_bounds = [-1, median-1, 99]
df["hours.per.week"] = pd.cut(df["hours.per.week"], hrs_per_wk_bounds)
attributeIntervals["hours.per.week"] = hrs_per_wk_bounds

# #Split on given intervals
nonZeroMean = df[df['capital.loss'] >= 10.0].mean()
capital_loss_bounds = [-1, df["capital.loss"].mean(), nonZeroMean["capital.loss"],99999]
df["capital.loss"] = pd.cut(df["capital.loss"], capital_loss_bounds)
attributeIntervals["capital.loss"] = capital_loss_bounds


#Unknown in workclass replaced by mode
unknownReplacements["workclass"] = df["workclass"].mode()
df["workclass"].replace(to_replace=['?'], value=unknownReplacements["workclass"], inplace=True)

#Unknown in education replaced by mode
unknownReplacements["education"]= df["education"].mode()
df["education"].replace(to_replace=['?'], value=unknownReplacements["education"], inplace=True)

#Unknown in marital status replaced by mode
unknownReplacements["marital.status"] =  df["marital.status"].mode()
df["marital.status"].replace(to_replace=['?'], value=unknownReplacements["marital.status"], inplace=True)

#Unknown in occupation replaced by mode
occupation_mode = df["occupation"].mode()
df["occupation"].replace(to_replace=['?'], value=occupation_mode, inplace=True)
unknownReplacements["occupation"] = occupation_mode

#Unknown in relationship replaced by mode
unknownReplacements["relationship"] = df["relationship"].mode()
df["relationship"].replace(to_replace=['?'], value=unknownReplacements["relationship"], inplace=True)

#Unknown in race replaced by mode
unknownReplacements["race"] =  df["race"].mode()
df["race"].replace(to_replace=['?'], value=unknownReplacements["race"], inplace=True)

#Unknown in sex replaced by mode
unknownReplacements["sex"] =  df["sex"].mode()
df["sex"].replace(to_replace=['?'], value=unknownReplacements["sex"], inplace=True)

#Unknown in sex replaced by mode
unknownReplacements["native.country"] =  df["native.country"].mode()
df["native.country"].replace(to_replace=['?'], value=unknownReplacements["native.country"], inplace=True)


df.to_csv("train_processed.csv", sep=',', index=False, encoding='utf-8')
df_processed = pd.read_csv('train_processed.csv')
print("processed data")


df_test = pd.read_csv('test_final.csv')
print("test before")
print(df_test)
for attribute in attributeIntervals:
    bounds = list(set(attributeIntervals[attribute]))
    list.sort(bounds)
    df_test[attribute] = pd.cut(df_test[attribute], bounds)

for attribute in unknownReplacements:
    df_test[attribute].replace(to_replace=['?'], value=unknownReplacements[attribute], inplace=True)


df_test.to_csv("test_processed.csv", sep=',', index=False, encoding='utf-8')
print("test after")
print(df_test)

pd.read_csv('train_processed.csv')