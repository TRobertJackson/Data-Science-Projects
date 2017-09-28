import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy
import seaborn as sns
from seaborn import plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
import time
import math

from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

def pseudo_cross_val_elasticnet_score(df, num_fold, alpha, l1_ratio):
    '''
    function to perform linear regression with elasticnet regularization and cross validation
    '''
    #shuffle the dataframe and separate it into n folds
    df = df.sample(frac=1, random_state = 100).reset_index(drop = True) #shuffle sumple
    num_row_in_fold = len(df.index)//num_fold

    #mannulay do cross validation for n folds
    scores = []
    for i in range(num_fold):
        #the ith fold is test data, the remaining is training data
        test_start = (num_row_in_fold * i)
        test_end = (num_row_in_fold * (i + 1)) + 1

        test = df.iloc[test_start : test_end]
        train = df.drop(df.index[test_start : test_end])

        X_train = train.drop('points', axis = 1)
        y_train = train['points']
        X_test = test.drop('points', axis = 1)
        y_test = test['points']

        #normalize X_train and X_test based on X_train's mean and std,
        scaler = preprocessing.StandardScaler().fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        #perform linear regression with elasticnet regularization
        model= ElasticNet(alpha = alpha, l1_ratio = l1_ratio, max_iter=10000)
        model.fit(X_train_scaled, y_train)
        scores.append(model.score(X_test_scaled, y_test))

    #return the mean score as the cross validation score
    return np.median(scores)

def elasticnet_optimize_parameters(df, alphas, l1_ratios):
    '''
    function to optimize the alpha and l1_ratio for the elasticnet regularization
    '''
    max_score = 0
    optimized_alpha = 0
    optimized_l1_ratio = 0

    #perform linear regression with elasticnet regularization and cross validation
    #for each combination of alpha and l1_ratio
    #get the maximum score and the optimized set of alpha and l1_ratio
    for alpha in alphas:
        for l1_ratio in l1_ratios:
            score = pseudo_cross_val_elasticnet_score(df, 5, alpha, l1_ratio)
            if score > max_score:
                max_score = score
                optimized_alpha = alpha
                optimized_l1_ratio = l1_ratio
    return [max_score, optimized_alpha, optimized_l1_ratio]

def pseudo_cross_val_lasso_score(df, num_fold, alpha):
    '''
    function to perform linear regression with lasso regularization and cross validation
    '''
    #shuffle the dataframe and separate it into n folds
    df = df.sample(frac=1, random_state = 100).reset_index(drop = True) #shuffle sumple
    num_row_in_fold = len(df.index)//num_fold

    scores = []
    #mannulay do cross validation for n folds
    for i in range(num_fold):

        #the ith fold is test data, the remaining is training data
        test_start = (num_row_in_fold * i)
        test_end = (num_row_in_fold * (i + 1)) + 1

        test = df.iloc[test_start : test_end]
        train = df.drop(df.index[test_start : test_end])

        X_train = train.drop('points', axis = 1)
        y_train = train['points']
        X_test = test.drop('points', axis = 1)
        y_test = test['points']

        #normalize X_train and X_test based on X_train's mean and std,
        scaler = preprocessing.StandardScaler().fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

       #perform linear regression with elasticnet regularization
        model= Lasso(alpha = alpha, max_iter=10000)
        model.fit(X_train_scaled, y_train)
        scores.append(model.score(X_test_scaled, y_test))

    #return the mean score as the cross validation score
    return np.median(scores)

def lasso_optimize_alpha(df, alphas):
    '''
    function to optimize the alpha and l1_ratio for the lasso regularization
    '''

    #perform linear regression with elasticnet regularization and cross validation for each alpha
    #get the maximum score and the optimized alpha
    max_score = 0
    optimized_alpha = 0
    for alpha in alphas:
        score = pseudo_cross_val_lasso_score(df, 5, alpha)
        if score > max_score:
            max_score = score
            optimized_alpha = alpha
    return [max_score, optimized_alpha]
