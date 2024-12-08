import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
import csv

# # Create a variable for the best model
def printPrediction(predictions):
    rowID = 1
    with open('predictions.csv', 'w') as f:
        print("ID,Prediction", file=f)
        for prediction in predictions: 
            line = str(rowID) +"," + str(prediction[1])
            print(line, file=f)
            rowID += 1

trainingData = pd.read_csv('train_processed.csv')

# Split the data into features (X) and target (y)
X = trainingData.drop('income>50K', axis=1)
y = trainingData['income>50K']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0)


param_dist = {'n_estimators': randint(50,800),
              'max_depth': randint(1,20)}

rf = RandomForestClassifier()

rand_search = RandomizedSearchCV(rf, 
                                 param_distributions = param_dist, 
                                 n_iter=5, 
                                 cv=5)
rand_search.fit(X_train, y_train)


# # Print the best hyperparameters
# print('Best hyperparameters:',  rand_search.best_params_)
testData = pd.read_csv('test_processed.csv')
_testData = testData.drop('ID', axis=1)
#y_pred = rand_search.predict(X_test)
predictions = rand_search.predict_proba(_testData)
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)
# printPrediction(predictions)