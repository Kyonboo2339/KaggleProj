import ID3
import DataSet
import sys
import csv
import pandas as pd

def readFile(CSVfile):
    termList = []
    attributeMap = {}
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        attributeRead = False
        for line in csv.reader(file, skipinitialspace=True):
            if not attributeRead:
                attributeRead = True
                for i in range(len(line)):
                    attributeMap[line[i]] = i

            else:
                termList.append(line)        

    print(attributeMap)
    print(termList[0])
    return attributeMap, termList

def predictOnFile(decisionTree, testList, attributeMap):
    incorrectPrediction = 0

    for test in testList:
        prediction= decisionTree.predictLabel(test, attributeMap) 
        # print(str(prediction) + "    :    " + str(test[-1]))  
        # print(prediction != test[-1])
        if str(prediction) != str(test[-1]):
            incorrectPrediction += 1

    return str(incorrectPrediction/len(testList))

def makePrediction(decisionTree, testList, attributeMap):
    rowID = 1
    with open('predictions.csv', 'w') as f:
        print("ID,Prediction", file=f)
        for test in testList:
            prediction= decisionTree.predictLabel(test, attributeMap) 
            line = str(rowID) +"," + str(prediction)
            print(line, file=f)
            rowID += 1


def results(decisionTree, file, testMap):
    #Read test file
    testError = predictOnFile(decisionTree, file, testMap)
    return testError

def __main__():    
    #Build decision tree

    trainingFile_car = pd.read_csv('train_processed.csv')
    attributeTrainMap, trainingFileTest_car = readFile("train_processed.csv")
    attributeTestMap, testFile_car = readFile('test_processed.csv')

    dataSet_car = DataSet.DataSet(trainingFile_car)
    print("Car results:\n")
     
    
    depthResults = []
    decisionTree = ID3.ID3Tree(dataSet_car,"informationGain",  4)
    #depthResults.append((results(decisionTree,trainingFileTest_car, attributeTrainMap))
    print("Depth\tTraining Error\tTest Error")

    #print("\t" + str(depthResults[0][0]) + "\t\t" + str(depthResults[0][1]))

    print("\nResults for bank, unknown is attribute:")

    makePrediction(decisionTree,testFile_car,attributeTestMap)
    print("finished")
    '''
    Based on the results for car.csv, the training error cannot exceed the test error.
    '''

__main__()