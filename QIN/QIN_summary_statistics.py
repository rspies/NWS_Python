#Created on 1/22/2015
#@author: Ryan Spies (rspies@lynkertech.com)
# Python 2.7
# This script reads CHPS csv file from QIN plot display and finds the start and end 
# of the observed hourly QIN record, # of valid data points, and % of total available.
# Outputs summary data to csv file

import os
import pandas as pd
import numpy as np
import datetime
os.chdir("../..")
maindir = os.path.abspath(os.curdir)

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
RFC = 'NWRFC_FY2017'
fx_group = '' # set to '' if not used
input_type = 'usgs' # choices: 'usgs' or 'chps'
if fx_group != '':
    new_summary = open(maindir + os.sep +'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'data_csv' + os.sep + 'QIN' + os.sep + fx_group + '_QIN_' + input_type + '_statistical_summary.csv','w')
    data_dir = fx_group + os.sep + 'merged_csv'
else:
    new_summary = open(maindir + os.sep +'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'data_csv' + os.sep + 'QIN' + os.sep + 'QIN_' + input_type + '_statistical_summary.csv','w')
    data_dir = 'merged_csv'
############################ End User input ##################################
##############################################################################

################  Define the corresponding column of data in the csv file  #################
call_date = 0
call_qin = 1
############ End User input ##################################################
new_summary.write('Basin/Gauge' + ',' + '# of Obs' + ',' + 'Start Date' + ',' + 'End Date' 
+ ',' + 'Mean QIN (cfs)' + ',' + 'Max QIN (cfs)' + ',' + 'Min QIN (cfs)' +','+ 'Standard Deviation (cfs)' 
+ ',' + 'Date Max' + ','  + 'Date Min' + '\n')

if input_type == 'usgs':
    csv_loc = maindir + os.sep +'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'data_csv' + os.sep + 'QIN' + os.sep + data_dir
    header = 3
if input_type == 'chps':
    csv_loc = maindir + os.sep +'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'data_csv' + os.sep + 'QIN' + os.sep + 'chps_export'
    header = 2

csv_files = os.listdir(csv_loc)
for csv_file in csv_files:
    basin_name = csv_file.split('_')[0]
    print basin_name
    csv_read = open(csv_loc + os.sep + csv_file,'r')
    ###### tab delimitted CHPS QIN dishcarge CSV file into panda arrays ###########
    test = pd.read_csv(csv_read,sep=',',skiprows=header,
            usecols=[call_date,call_qin],parse_dates=['date'],names=['date', 'QIN'])
    ### assign column data to variables
    
    date_qin = test['date'].tolist()                  # convert to list (indexible)
    all_qin = test['QIN'].tolist()

    # find max/min of all data
    Q_mask = np.ma.masked_less(all_qin,0.0)     # mask values less than 0 to ignore
    #Q_mask = np.ma.masked_less(all_qin,'-999')     # mask values less than 0 to ignore
    #Q_mask = np.ma.masked_invalid(all_qin)    # mask missing and 'nan' instances
    date_mask = np.ma.masked_where(np.ma.getmask(Q_mask) == True, date_qin) # mask dates containing missing discharge data
    Q_data = np.ma.compressed(Q_mask).tolist()          # create list with only valid dishcharge data
    final_date = np.ma.compressed(date_mask).tolist()   # create list with corresponding date
    
    if len(final_date) != len(Q_data):
        print 'WARNING -- Date and Discharge Data not the same length'
    if len(final_date) > 0 and len(Q_data) > 0: # check that there is flow data in csv file
        day_count = str(len(Q_data))                                # number of valid daily data values
        start_date = str(min(final_date).strftime('%Y-%m-%d'))      # date of first measurement
        end_date = str(max(final_date).strftime('%Y-%m-%d'))         # date of last measurement
        mean_Q = str(np.average(Q_data))                             # mean of all QME data
        max_Q = np.max(Q_data)                                      # maximum of all QME
        max_index = Q_data.index(max_Q)                             # index of the max daily QME value
        date_max = str(final_date[max_index].strftime('%Y-%m-%d'))   # date of maximum discharge
        min_Q = np.min(Q_data)                                      # minimum of all QME
        min_indices = [i for i, x in enumerate(Q_data) if x == min_Q]
        if len(min_indices) > 1:                                    # if more than 1 occurence of Q_min return "numerous"
            date_min = 'Numerous'
        else:
            min_index = Q_data.index(min_Q)                         # index of the minimum daily QME value
            date_min = str(final_date[min_index].strftime('%Y-%m-%d'))   # date of minimum discharge
        sd = str(np.std(Q_data))                                    # standard deviation of QME data
        new_summary.write(basin_name+','+day_count+','+start_date+','+end_date+','+mean_Q+','
        +str(max_Q)+','+str(min_Q)+','+sd+','+date_max+','+date_min+'\n')
    else:
        print 'No data in the csv file... please check -> ' + basin_name

new_summary.close()
print 'Finished!'
print datetime.datetime.now()