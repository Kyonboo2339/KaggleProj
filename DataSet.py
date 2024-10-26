#Manages the counts of each attribute in the set
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
import pandas as pd
import numpy as np
#label
class DataSet():
    def __init__(self, _dataframe):
        self.df = _dataframe 
        #Memoize the proportions as they're calculated
        self.attribute_counts = pd.DataFrame(columns=["attribute, label.proportion"])
        self.df_counts = None
        self.Count = len(self.df.index)

    #Return a new DataSet split on given attributeID and attributeValue
    def setSplit(self, attribute, value):
        return DataSet(self.df.loc[self.df[attribute] == value])
    
    def mostCommonLabel(self):
        stats = self.df.groupby("income>50K").size()
        if 1 not in stats.keys():
            return 0
        return stats[1]/self.Count
    
    def hasSameLabel(self):
        return len(self.df["income>50K"].unique()) == 1
    
    #Return percentage of rows assigned to each label for the set
    def labelProportions(self):
        if self.df_counts == None:
            value_counts = self.df.groupby("income>50K").size()
            self.df_counts = {label: value_counts[label]/self.Count for label in value_counts.keys()}
        return self.df_counts
    
    #Returns the percentage of rows with an attribute value 
    def attributeValueWeighted_Average(self, attribute, attributeValue):
        attributeCount = self.df.groupby(attribute).size()
        return  attributeCount[attributeValue]/self.Count
    

    #Returns a dict of label distributions based on attribute value subsets
    def attributeValueProportions(self, attribute):
        
        #Number of rows in each attribute value
        attributeValues = self.df[attribute].unique()
        #Proportion of label to attribute value subset
        attributeLabelCount = {}

        for value in attributeValues:
            attributeValue = value
            rows_with_value = self.df.loc[self.df[attribute] == value]
            attributeValueCount = len(rows_with_value.index)
            attributeLabelCount[attributeValue] = {}

            attributeValueLabelCount = rows_with_value.groupby("income>50K").size()
            for label in attributeValueLabelCount.keys():
                attributeLabelCount[attributeValue][label] = None
                
                if attributeValueCount > 0:
                    attributeLabelCount[attributeValue][label] = attributeValueLabelCount[label]/attributeValueCount
                else: 
                    attributeLabelCount[attributeValue][label] = 0

      
        return attributeLabelCount
    
    def getAttributes(self):
        attributes = self.df.columns.values.tolist()
        attributes.remove("income>50K")

        return attributes
    
    def getAttributeValues(self, attribute):
        return self.df[attribute].unique()
    
    def rowsSum(self, rowTuples):
        labelTotal = 0
        for rowTuple in rowTuples:
            labelTotal += self.D_weights[rowTuple[0]]

        return labelTotal