import ID3
import DataSet
import sys
import pandas as pd

def readFile(CSVfile):
    termList = []
    attributeMap = {}
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        attributeRead = False
        for line in file:
            if not attributeRead:
                attributeRead = True
                attributes = line.strip().split(',')
                for i in range(len(attributes)):
                    attributeMap[attributes[i]] = i

            else:
                termList.append(line.strip().split(','))        

    return attributeMap, termList

def predictOnFile(decisionTree, testList, attributeMap):
    incorrectPrediction = 0

    for test in testList:
        prediction= decisionTree.predictLabel(test, attributeMap)     
        if prediction != test[-1]:
            incorrectPrediction += 1

    return str(incorrectPrediction/len(testList))

def results(decisionTree, testFile, trainingFile,  trainMap, testMap):
    #Read test file
    testError = predictOnFile(decisionTree, testFile, testMap)
    trainingError = predictOnFile(decisionTree, trainingFile, trainMap)
    return testError, trainingError

def __main__():    
    #Build decision tree

    trainingFile_car = pd.read_csv('train.csv')
    attributeTrainMap, trainingFileTest_car = readFile("train.csv")
    attributeTestMap, testFile_car = readFile('test.csv')

    dataSet_car = DataSet.DataSet(trainingFile_car)
    heuristics = ["informationGain", "giniIndex", "majorityError"]
    print("Car results:\n")
     
    for heuristic in heuristics:
        depthResults = []
        for i in range(1,7):
            decisionTree = ID3.ID3Tree(dataSet_car, heuristic,  i)
            depthResults.append(results(decisionTree, testFile_car, trainingFileTest_car, attributeTrainMap,attributeTestMap))
        print("\nHeuristic: " + heuristic)
        print("Depth\tTest Error\t\tTraining Error")
        for i in range(6):
            print("  " + str(i + 1) + "\t" + str(depthResults[i][0]) + "\t" + str(depthResults[i][1]))

    print("\nResults for bank, unknown is attribute:")

            
    '''
    Based on the results for car.csv, the training error cannot exceed the test error.
    '''

__main__()