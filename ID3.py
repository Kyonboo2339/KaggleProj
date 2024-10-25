import Heuristics
import DataSet
import sys
import pandas as pd

class ID3Tree:
    def __init__(self, dataSet, heuristic= "informationGain", depthLimit= 6):
        if heuristic not in dir(Heuristics):
            raise AttributeError("Heuristic not found")

        self.heuristic = getattr(Heuristics, heuristic)
        self.data = dataSet
        self.depthLimit = depthLimit
        self.rootNode = self.ID3(dataSet, 0)
        print("Split on " + str(self.rootNode.attribute))



    def predictLabel(self, datum, attributeMap):
        currNode = self.rootNode
        
        while True: 
            value = datum[attributeMap[currNode.attribute]]
            if isinstance(currNode.branches[value], ID3Tree.ID3Node):
                currNode = currNode.branches[value]
            else:
                return currNode.branches[value]

    def ID3(self, dataSet, currDepth):
        if dataSet.hasSameLabel() or currDepth >= self.depthLimit:   
            return dataSet.mostCommonLabel()
        
        #Create a root node 
        root = self.ID3Node(self.chooseAttribute(dataSet))
        attributeValues = self.data.getAttributeValues(root.attribute)

        for attributeValue in attributeValues:     
            subset = dataSet.setSplit(root.attribute, attributeValue)
            if subset.Count == 0:
                root.branches[attributeValue] = dataSet.mostCommonLabel()
            else: 
                root.branches[attributeValue] = self.ID3(subset, currDepth + 1)

        return root

    #Calulate the purity of the set split on a certain attribute
    def calculateGain(self, attributeID, dataSet):
        setHeuristic = self.heuristic(dataSet.labelProportions())
        attributeSum = 0
        attributeProportions = dataSet.attributeValueProportions(attributeID)
        for value in attributeProportions:
            attribute_weighted_average = dataSet.attributeValueWeighted_Average(attributeID, value)
            heuristic = self.heuristic(attributeProportions[value])
            prop = attribute_weighted_average*heuristic
            attributeSum += prop

        return setHeuristic - attributeSum
    
    #Choose the best attribute to split the set
    def chooseAttribute(self, dataSet):
        bestAttribute = None
        maxGain = float("-inf")
        for attributeID in dataSet.getAttributes():
            attributeGain = self.calculateGain(attributeID, dataSet)
            if attributeGain > maxGain:
                bestAttribute = attributeID
                maxGain = attributeGain

        return bestAttribute
    
    #Node for the ID3 tree
    class ID3Node:
        def __init__(self, attribute):
            #Possible values on splitting attribute
            self.branches = {}
            #The attribute the node splits data on
            self.attribute = attribute



