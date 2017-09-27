# loading packages
import numpy as np
import pandas as pd

def ToWeight(y):
    '''
    function to help calculate root mean square percentage error.
    '''
    w = np.zeros(y.shape, dtype=float)
    ind = y != 0
    w[ind] = 1./(y[ind]**2)
    return w


def rmspe(yhat, y):
    '''
    function to calculate root mean square percentage error for forecasted sales.
    '''
    w = ToWeight(y)
    rmspe = np.sqrt(np.mean( w * (y - yhat)**2 ))
    return rmspe


def rmspe_xg(yhat, y):
    '''
    score function for xgboost which calculates root mean square percentage error.
    '''
    y = y.get_label()
    y = np.exp(y) - 1
    yhat = np.exp(yhat) - 1
    w = ToWeight(y)
    rmspe = np.sqrt(np.mean(w * (y - yhat)**2))
    return "rmspe", rmspe
