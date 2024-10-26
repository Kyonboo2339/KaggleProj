import pandas as pd
df =  pd.read_csv('train_processed.csv')
# print(df)
# #Memoize the proportions as they're calculated
# df_counts = pd.DataFrame(columns=["attribute, label.proportion"])
# Count = len(df.index)
# value_counts = df.groupby("income>50K").size()
# labelCount = {label: value_counts[label]/Count for label in value_counts.keys()}
# print(value_counts[0])
# print(labelCount)

# #Number of rows in each attribute value
# attribute = df["relationship"].unique()
# print(attribute)
# #Proportion of label to attribute value subset
# attributeLabelCount = {}

# for value in attribute:
#     attributeValue = value
#     rows_with_value = df.loc[df["relationship"] == value]
#     attributeValueCount = len(rows_with_value.index)
#     print(attributeValueCount)
#     attributeLabelCount[attributeValue] = {}

#     attributeValueLabelCount = rows_with_value.groupby("income>50K").size()
#     for label in attributeValueLabelCount.keys():
#         attributeLabelCount[attributeValue][label] = None
        
#         if attributeValueCount > 0:
#             attributeLabelCount[attributeValue][label] = attributeValueLabelCount[label]/attributeValueCount
#         else: 
#             attributeLabelCount[attributeValue][label] = 0

print(df["fnlwgt"].unique())
