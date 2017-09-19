#Created on 1/23/2015
#@author: rspies
# Python 2.7
# This script reads CHPS csv file from QIN plot display and finds the start and end 
# of the observed hourly QIN record, # of valid data points, and % of total available.
# Outputs summary data to csv file

import os
import sys
import pandas as pd
import numpy as np
import datetime
os.chdir('../')
sys.path.append(os.getcwd() + os.sep + 'modules')
import calc_errors
os.chdir('../')

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
RFC = 'MBRFC_FY2017'
fx_group = '' # leave blank if not processing by fx group
sim_type = 'final-CalibrationPeriod' # choices: initial (prior to calib), final (final calib), working (currently in calib process)

if fx_group == '':
    maindir = os.getcwd() + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries'
else:
    maindir = os.getcwd() + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + fx_group    
csv_loc = maindir + os.sep + sim_type.split('-')[0] + os.sep + 'QIN_SQIN' + os.sep
summary_file = maindir + os.sep + 'statQIN_outflow_csv' 
if not os.path.exists(summary_file):
    os.makedirs(summary_file)
############ End User input ##################################################
    
summary_out = open(summary_file + os.sep + 'statqin_summary_' + sim_type + '.csv','w')
summary_out.write('Basin' + ',' + 'Timestep' + ',' + '#obs' + ',' + 'Avg QIN' + ',' + 'Avg SQIN' + ',' + 'Bias' + ',' + 'Pbias' + ',' 
                + 'MAE' + ',' + 'RMSE' + ',' + 'Corr Coef' + ',' + 'Nash Sut\n')
csv_files = os.listdir(csv_loc)
for csv_file in csv_files:
    basin_name = csv_file.split('_')[0]
    print basin_name

    csv_read = open(csv_loc + os.sep + csv_file,'r')
    ###### tab delimitted CHPS QIN dishcarge CSV file into panda arrays ###########
    test = pd.read_csv(csv_read,sep=',',skiprows=2, header = 1, parse_dates=[0],names=['date','QIN','SQIN'],na_values=[' ','',' \n',-999,'-999'])
    ### assign column data to variables
    date_qin = test['date'].tolist()                  # convert to list (indexible)
    timestep = int((date_qin[1] - date_qin[0]).total_seconds()/3600)  # calculate the timestep between the data points
    all_qin = test['QIN'].tolist()
    all_sqin = test['SQIN'].tolist()
    sqin = []; qin = []; count = 0                 # read the data into a dictionary (more efficient processing)
    missing = 0
    for each in all_qin:
        if float(each) >= 0 and float(all_sqin[count]) >= 0:          # ignore data less than 0          
            qin.append(each)
            sqin.append(all_sqin[count])
        else:
            missing += 1
        count += 1
    csv_read.close() 
        
    ###### calculate stats #####
    if count != missing:
        avg_qin = "%.2f" %  np.mean(qin); avg_sqin = "%.2f" % np.mean(sqin)
        bias = "%.2f" % calc_errors.pct_bias(qin,sqin)[0]
        pbias = "%.2f" % calc_errors.pct_bias(qin,sqin)[1]
        mae = "%.2f" %calc_errors.ma_error(qin,sqin)
        rmse = "%.2f" %calc_errors.rms_error(qin,sqin)[0]
        corr_coef = "%.2f" % calc_errors.corr_coef(qin,sqin)[1][0]
        nash_sut = "%.2f" % calc_errors.nash_sut(qin,sqin)
    else:
        pbias=bias=mae=corr_coef=nash_sut=avg_qin=avg_sqin=rmse= 'na'
    
    ###### write summary to output csv #######
    summary_out.write(basin_name + ',' + str(timestep) + ',' + str(len(qin)) + ',' + str(avg_qin) + ',' + str(avg_sqin) + ',' + str(bias) + ',' 
                + str(pbias) + ',' + str(mae) + ',' + str(rmse) + ',' + str(corr_coef) + ',' + str(nash_sut) + ',' + '\n')
                
summary_out.close()
print 'Finished!'
print 'CHECK UNITS IN ORIGINAL DATA!!!'
print datetime.datetime.now()