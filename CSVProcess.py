import sys
import pandas as pd
import numpy as np
import csv
df = pd.read_csv('train_final.csv')
print(df)
attributeIntervals = {}
unknownReplacements = {}

#Age by quartile
i = pd.IntervalIndex(pd.qcut(df["age"], q= 5).value_counts().index)
L1 = list(zip(i.left, i.right))[:4]
age_intervals = [y for x in L1 for y in x]
age_intervals.extend([-1, 99])
attributeIntervals["age"] = age_intervals
print(df.groupby("age").size())

#fnlwgt by quartile
i = pd.IntervalIndex(pd.qcut(df["fnlwgt"], q= 5).value_counts().index)
L1 = list(zip(i.left, i.right))[:4]
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
    print(bounds)
    _labels = [i for i in range(len(bounds) - 1)]
    df_test[attribute] = pd.cut(df_test[attribute], bounds, labels= _labels)
    df[attribute] = pd.cut(df[attribute], bounds, labels= _labels)

for attribute in unknownReplacements:
    df_test[attribute].replace(to_replace=['?'], value=unknownReplacements[attribute], inplace=True)
    df[attribute].replace(to_replace=['?'], value=unknownReplacements[attribute], inplace=True)
    # df_test[attribute].replace(to_replace=['?'], value="50", inplace=True)
    # df[attribute].replace(to_replace=['?'], value="50", inplace=True)
    
#bank_data['default'].map({'no':0,'yes':1,'unknown':0})
df["workclass"] = df["workclass"].map({"Private":0, "Self-emp-not-inc":1, "Self-emp-inc":2, "Federal-gov":3, "Local-gov":4, "State-gov":5, "Without-pay":6, "Never-worked":7, "?":50})
df["marital.status"] = df["marital.status"].map({"Married-civ-spouse":0,"Divorced":1, "Never-married":2, "Separated":3, "Widowed":4, "Married-spouse-absent":5, "Married-AF-spouse":6, "?":50})
df["occupation"] = df["occupation"].map({"Tech-support":0, "Craft-repair":1, "Other-service":2, "Sales":3, "Exec-managerial":4, "Prof-specialty":5, "Handlers-cleaners":6, "Machine-op-inspct":7, "Adm-clerical":8, "Farming-fishing":9, "Transport-moving":10, "Priv-house-serv":11, "Protective-serv":12, "Armed-Forces":13, "?":50})
df["relationship"] = df["relationship"].map({"Wife":0, "Own-child":1, "Husband":2 ,"Not-in-family":3, "Other-relative":4, "Unmarried":5, "?":50})
df["race"] = df["race"].map({"White":0, "Asian-Pac-Islander":1, "Amer-Indian-Eskimo":2, "Other":3, "Black":4, "?":50})
df["sex"] = df["sex"].map({"Female":0, "Male":1, "?":50})

df["education"] = df["education"].map({"Bachelors":0, "Some-college":1, "11th":2, "HS-grad":3, "Prof-school":4, "Assoc-acdm":5, "Assoc-voc":6, "9th":7, "7th-8th":8, "12th":9, "Masters":10, "1st-4th":11, "10th":12, "Doctorate":13, "5th-6th":14, "Preschool":15, "?":50})
countries = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada","Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]
m6 = {countries[i]:i for i in range(len(countries))} 
m6["?"] = 50
df["native.country"] = df["native.country"].map(m6)

df_test["workclass"] = df_test["workclass"].map({"Private":0, "Self-emp-not-inc":1, "Self-emp-inc":2, "Federal-gov":3, "Local-gov":4, "State-gov":5, "Without-pay":6, "Never-worked":7, "?":50})
df_test["marital.status"] = df_test["marital.status"].map({"Married-civ-spouse":0,"Divorced":1, "Never-married":2, "Separated":3, "Widowed":4, "Married-spouse-absent":5, "Married-AF-spouse":6, "?":50})
df_test["occupation"] = df_test["occupation"].map({"Tech-support":0, "Craft-repair":1, "Other-service":2, "Sales":3, "Exec-managerial":4, "Prof-specialty":5, "Handlers-cleaners":6, "Machine-op-inspct":7, "Adm-clerical":8, "Farming-fishing":9, "Transport-moving":10, "Priv-house-serv":11, "Protective-serv":12, "Armed-Forces":13, "?":50})
df_test["relationship"] = df_test["relationship"].map({"Wife":0, "Own-child":1, "Husband":2 ,"Not-in-family":3, "Other-relative":4, "Unmarried":5, "?":50})
df_test["race"] = df_test["race"].map({"White":0, "Asian-Pac-Islander":1, "Amer-Indian-Eskimo":2, "Other":3, "Black":4, "?":50})
df_test["sex"] = df_test["sex"].map({"Female":0, "Male":1, "?":50})

df_test["education"] = df_test["education"].map({"Bachelors":0, "Some-college":1, "11th":2, "HS-grad":3, "Prof-school":4, "Assoc-acdm":5, "Assoc-voc":6, "9th":7, "7th-8th":8, "12th":9, "Masters":10, "1st-4th":11, "10th":12, "Doctorate":13, "5th-6th":14, "Preschool":15, "?":50})
countries = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada","Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]
m6 = {countries[i]:i for i in range(len(countries))} 
m6["?"] = 50
df_test["native.country"] = df_test["native.country"].map(m6)

df_test.to_csv("test_processed.csv", sep=',', index=False, encoding='utf-8')
df.to_csv("train_processed.csv", sep=',', index=False, encoding='utf-8')
print(attributeIntervals)
print(unknownReplacements)
print("processed data")