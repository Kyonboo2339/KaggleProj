import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.model_selection import GridSearchCV
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
Y = trainingData['income>50K']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)


param_dist = {'n_estimators': [14],
              'max_depth': [380]}


# rf = RandomForestClassifier(bootstrap=False,max_depth=16, min_samples_leaf=2, min_samples_split=10, n_estimators=265)
# rf.fit(X_train,y_train)
# best_rf = rf

rf = RandomForestClassifier()
# rand_search = RandomizedSearchCV(rf, 
#                                  param_distributions = param_dist, 
#                                  n_iter=1, 
#                                  cv=5,
#                                  n_jobs=-1)

# rand_search.fit(X, Y)
# print('Best hyperparameters:',  rand_search.best_params_)
# best_rf = rand_search.best_estimator_

param_grid = {
    'bootstrap': [False, True],
    'max_depth': [12, 14, 15],
    'min_samples_leaf': [40, 60, 80],
    'n_estimators': [600, 800, 1000]
}# Create a based model
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 3, n_jobs = -1)



grid_search.fit(X_train, y_train)
print('Best hyperparameters:',  grid_search.best_params_)
best_rf = grid_search.best_estimator_


# # Print the best hyperparameters


y_pred = best_rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# testData = pd.read_csv('test_processed.csv')
# _testData = testData.drop('ID', axis=1)
# predictions = best_rf.predict_proba(_testData)
# printPrediction(predictions)
