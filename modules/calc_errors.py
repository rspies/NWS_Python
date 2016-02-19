#Created on 1/23/2015
#@author: rspies
# Python 2.7

######################################################################################################
#This script contains several functions for calculating error statistics:
#1 pct_bias: percent bias
#2 nash_sut: nash sutcliffe
#3 ma_error: mean absolute error
#4 rms_error: root mean squared error and normalized root mean squared error (normalized by obs mean)
#5 corr_coef: correlation coefficient (numpy function)
######################################################################################################

# error statistics
import numpy as np
def pct_bias(obsx,modely):
    print 'Length of sim: ' + str(len(modely))
    print 'Length of obs: ' + str(len(obsx))
    cnt = 0
    a = 0
    b = 0
    for each in modely:
        a = a + (float(modely[cnt]) - obsx[cnt])
        cnt += 1
    b = sum(obsx)
    pbias = (a/b) * 100
    print 'P Bias: ' + str(pbias)
    return pbias
    
    ###### Nash Sutcliffe #####
def nash_sut(obsx,modely):
    cnt = 0
    a = 0
    c = 0
    for each in modely:
        a = a + ((modely[cnt] - obsx[cnt])**2)
        b = sum(obsx)/len(obsx)
        c = c + ((obsx[cnt] - b)**2)
        cnt += 1
    ns = round(1 - (a/c), 2)
    print 'NSE: ' + str(ns)
    return ns
    
    ###### Mean Absolute Error #####
def ma_error(obsx,modely):
    cnt = 0
    a = 0
    for each in modely:
        a = a + (abs(modely[cnt] - obsx[cnt]))
        cnt += 1
    mae = round(a/len(modely),2)
    print 'MAE: ' + str(mae)
    return mae
    
    ###### Normalized (mean obs) Root Mean Squared Error #####
def rms_error(obsx,modely):
    cnt = 0
    a = 0
    
    for each in modely:
        a = a + ((modely[cnt] - obsx[cnt])**2)
        cnt += 1
    mean = sum(obsx)/len(obsx)
    rmse = round((a/len(modely))**.5,2)
    nrmse = round(rmse/mean,2)
    print 'RMSE: ' + str(rmse)
    print 'NRMSE: ' + str(nrmse)
    return rmse, nrmse

    ###### Correlation Coefficient #######
def corr_coef(obsx,modely):
    cc = np.corrcoef(obsx,modely)
    print 'cc: ' + str(cc[1][0]) # call the 3 value in the matrix output
    return cc
    #############################################################################

