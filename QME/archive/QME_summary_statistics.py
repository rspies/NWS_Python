#Created on July 22, 2014
#@author: rspies
# Python 2.7
# This script calculates summary statistics for multiple QME data files
# input RFC to process and location of files
# Note: input must be in the native USGS (NWIS download format) -> daily data

import os
import numpy as np
import pandas as pd
maindir = os.getcwd()[:-6]

############ User input ################
RFC = 'SERFC'
raw_files = 'P:\\NWS\\Calibration_NWS\\' + RFC + '\\data\\daily_discharge' # directory with USGS QME data
new_file = 'P:\\NWS\\Calibration_NWS\\' + RFC + '\\data\\' # output summary tab delimited file location
########################################
QMEs = os.listdir(raw_files)
new_summary = open(new_file + 'QME_data_summary.csv', 'w')
new_summary.write('Basin/Gauge' + ',' + 'Daily Count' + ',' + 'Start Date' + ',' + 'End Date' 
+ ',' + 'Mean Daily QME' + ',' + 'Max Daily QME' + ',' + 'Min Daily QME' +','+ 'Standard Deviation' 
+ ',' + 'Date Max' + ','  + 'Date Min' + '\n')

for QME in QMEs:
    csv_read = open(raw_files + '\\' + QME, 'r')
    
    ### read tab delimitted USGS obs discharge file into panda arrays
    data = pd.read_csv(csv_read,sep='\t',skiprows=28,
            usecols=[0,1,2,3,4],parse_dates=['date'],names=['agency', 'site_num', 'date', 'Q', 'flag'])
    
    ### assign column data to variables
    print QME
    agency = data['agency']
    site_num = data['site_num']
    date = data['date'].tolist() # convert to list (indexible)
    discharge = data['Q'].tolist()
    csv_read.close()
    
    Q_mask = np.ma.masked_less(discharge,0)     # mask values less than 0 to ignore
    Q_mask = np.ma.masked_invalid(discharge)    # mask missing and 'nan' instances
    date_mask = np.ma.masked_where(np.ma.getmask(Q_mask) == True, date) # mask dates containing missing discharge data
    Q_data = np.ma.compressed(Q_mask).tolist()          # create list with only valid dishcharge data
    final_date = np.ma.compressed(date_mask).tolist()   # create list with corresponding date
    
    if len(final_date) != len(Q_data):
        print 'WARNING -- Date and Discharge Data not the same length'
    
    basin_gauge = QME[:-4]
    day_count = str(len(Q_data))            # number of valid daily data values
    start_date = str(min(final_date))       # date of first measurement
    end_date = str(max(final_date))         # date of last measurement
    mean_Q = str(np.average(Q_data))        # mean of all QME data
    max_Q = np.max(Q_data)                  # maximum of all QME
    max_index = Q_data.index(max_Q)         # index of the max daily QME value
    date_max = str(final_date[max_index])   # date of maximum discharge
    min_Q = np.min(Q_data)                  # minimum of all QME
    min_indices = [i for i, x in enumerate(Q_data) if x == min_Q]
    if len(min_indices) > 1:                # if more than 1 occurence of Q_min return "numerous"
        date_min = 'Numerous'
    else:
        min_index = Q_data.index(min_Q)     # index of the minimum daily QME value
        date_min = str(final_date[min_index])   # date of minimum discharge
    sd = str(np.std(Q_data))                # standard deviation of QME data

    new_summary.write(basin_gauge+','+day_count+','+start_date+','+end_date+','+mean_Q+','
    +str(max_Q)+','+str(min_Q)+','+sd+','+date_max+','+date_min+'\n')    
    
new_summary.close()
print 'Completed!!'