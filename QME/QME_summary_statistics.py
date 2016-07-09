#Created on July 22, 2014
#@author: rspies
# Python 2.7
# This script calculates summary statistics for multiple QME data files
# input RFC to process and location of files
# Note: input must be in the native USGS (NWIS download format) -> daily data

import os
import numpy as np
import datetime
from dateutil import parser
os.chdir("../..") # change dir to \\AMEC\\NWS
maindir = os.getcwd()

############ User input ################
RFC = 'NCRFC_FY2016'
fx_group = 'DES' # set to '' if not used
data_format = 'nhds' # choices: 'usgs' or 'chps' or 'nhds'
usgs_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data\\daily_discharge' # directory with USGS QME data
chps_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\Calibration_TimeSeries\\initial\\QME_SQME\\' # CHPS csv output files
nhds_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\QME\\' # NHDS data download (cardfiles)
new_file = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\' # output summary tab delimited file location
########################################

if fx_group != '':
    nhds_files = nhds_files + os.sep + fx_group + os.sep + 'QME_combined' 
    new_summary = open(new_file +'QME' + os.sep + fx_group + os.sep + 'QME_data_statistical_summary_'+fx_group+'.csv', 'w')
else: 
    nhds_files = nhds_files + os.sep + 'QME_Lynker_download' 
    new_summary = open(new_file + 'QME_data_statistical_summary.csv', 'w')
new_summary.write('Basin/Gauge' + ',' + 'Daily Count' + ',' + 'Start Date' + ',' + 'End Date' 
+ ',' + 'Mean Daily QME' + ',' + 'Max Daily QME' + ',' + 'Min Daily QME' +','+ 'Standard Deviation' 
+ ',' + 'Date Max' + ','  + 'Date Min' + '\n')

if data_format == 'usgs':
    QMEs = [f for f in os.listdir(usgs_files) if os.path.isfile(os.path.join(usgs_files, f))]
if data_format == 'chps':
    QMEs = [f for f in os.listdir(chps_files) if os.path.isfile(os.path.join(chps_files, f))]
if data_format == 'nhds':
    QMEs = [f for f in os.listdir(nhds_files) if os.path.isfile(os.path.join(nhds_files, f))]
    
for QME in QMEs:
    print QME
    if data_format == 'usgs': 
        csv_read = open(usgs_files + '\\' + QME, 'r')
        discharge = []; date = []
        ### read card file formatted .txt files lists
        line_count = 0
        for line in csv_read:
            if line_count >= 9: # ignore header lines
                sep = line.split()
                ### parse date columns
                month = str(sep[1])[:-2]
                year = str(sep[1])[-2:]
                if int(year) <= 14:
                    year = int(year) + 2000 # assume years <= 14 are in the 2000s
                else:
                    year = int(year) + 1900
                day = str(sep[2])
                full_date = datetime.datetime(year,int(month),int(day))
                date.append(full_date)
                if line_count == 12:
                    site_num = sep[0]
                discharge.append(float(sep[3]))
            line_count += 1
        csv_read.close()
    if data_format == 'chps': 
        csv_read = open(chps_files + '\\' + QME, 'r')
        discharge = []; date = []
        ### read card file formatted .txt files lists
        line_count = 0
        for line in csv_read:
            if line_count >= 2: # ignore header lines
                sep = line.split(',')
                full_date = parser.parse(sep[0])
                date.append(full_date.date())
                discharge.append(float(sep[3]))
            line_count += 1
        csv_read.close()
    if data_format == 'nhds': 
        csv_read = open(nhds_files + '\\' + QME, 'r')
        discharge = []; date = []
        ### read card file formatted .txt files lists
        line_count = 0
        for line in csv_read:
            if line_count >= 9: # ignore header lines
                sep = line.split()
                if len(sep) < 4: # some QME files (from RFC) may not have gage/basin id as 1st index
                    sep.insert(0,'0000')
                ### parse date columns
                month = str(sep[1])[:-2]
                year = str(sep[1])[-2:]
                if int(year) <= 15:
                    year = int(year) + 2000 # assume years <= 14 are in the 2000s
                else:
                    year = int(year) + 1900
                day = str(sep[2])
                full_date = datetime.datetime(year,int(month),int(day))
                date.append(full_date)
                if line_count == 12:
                    site_num = sep[0]
                discharge.append(float(sep[3]))
            line_count += 1
        csv_read.close()

    Q_mask = np.ma.masked_less(discharge,0)     # mask values less than 0 to ignore
    #Q_mask = np.ma.masked_invalid(np.asarray(discharge))    # mask missing and 'nan' instances
    date_mask = np.ma.masked_where(np.ma.getmask(Q_mask) == True, date) # mask dates containing missing discharge data
    Q_data = np.ma.compressed(Q_mask).tolist()          # create list with only valid dishcharge data
    final_date = np.ma.compressed(date_mask).tolist()   # create list with corresponding date
    
    if len(final_date) != len(Q_data):
        print 'WARNING -- Date and Discharge Data not the same length'
    
    basin_gauge = QME.split('_')[0]
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