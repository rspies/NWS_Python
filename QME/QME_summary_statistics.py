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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.ioff()

os.chdir("../..") # change dir to \\AMEC\\NWS
maindir = os.getcwd()

############ User input ################
RFC = 'WGRFC_FY2017'
fx_group = '' # set to '' if not used
data_format = 'nhds' # choices: 'usgs' or 'chps' or 'nhds'
usgs_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data\\daily_discharge' # directory with USGS QME data
chps_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\Calibration_TimeSeries\\initial\\QME_SQME\\' # CHPS csv output files
nhds_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\QME\\' # NHDS data download (cardfiles)
new_file = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\QME\\' # output summary tab delimited file location
########################################

if fx_group != '':
    nhds_files = nhds_files + os.sep + fx_group + os.sep + 'QME_Lynker_download' 
    new_summary = open(new_file + os.sep + fx_group + os.sep + 'QME_data_statistical_summary_'+fx_group+'.csv', 'w')
    figname = new_file + RFC + '_' + fx_group + '_QME_data_timeline.png'
else: 
    nhds_files = nhds_files + os.sep + 'QME_Lynker_download' 
    new_summary = open(new_file + 'QME_data_statistical_summary.csv', 'w')
    figname = new_file + RFC + '_' + 'QME_data_timeline.png'
new_summary.write('Basin/Gauge' + ',' + 'Daily Count' + ',' + 'Start Date' + ',' + 'End Date' 
+ ',' + 'Mean Daily QME' + ',' + 'Max Daily QME' + ',' + 'Min Daily QME' +','+ 'Standard Deviation' 
+ ',' + 'Date Max' + ','  + 'Date Min' + '\n')

########## define data timeline figure ###
fig, ax1 = plt.subplots(figsize=(11,9))        
plt.title('QME Data Availability Timeline',fontsize=14)
basins_list = []; count = 0
years = mdates.YearLocator()   # every year

if data_format == 'usgs':
    QMEs = [f for f in os.listdir(usgs_files) if os.path.isfile(os.path.join(usgs_files, f))]
if data_format == 'chps':
    QMEs = [f for f in os.listdir(chps_files) if os.path.isfile(os.path.join(chps_files, f))]
if data_format == 'nhds':
    QMEs = [f for f in os.listdir(nhds_files) if os.path.isfile(os.path.join(nhds_files, f))]
    
for QME in QMEs:
    print QME
    count += 1
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
                if len(sep) > 0: # ignore blank lines
                    if len(sep) < 4 and len(sep[-1]) < 10: # some QME files (from RFC) may not have gage/basin id as 1st index
                        sep.insert(0,'0000')
                    ### parse date columns
                    month = str(sep[1])[:-2]
                    year = str(sep[1])[-2:]
                    if int(year) <= 15:
                        year = int(year) + 2000 # assume years <= 14 are in the 2000s
                    else:
                        year = int(year) + 1900
                    day = str(sep[2])
                    if len(sep[-1]) > 10: # check for large streamflow values that get combined with day column
                        day = str(sep[2])[:-10]
                    full_date = datetime.datetime(year,int(month),int(day))
                    date.append(full_date)
                    if line_count == 12:
                        site_num = sep[0]
                    discharge.append(float(sep[-1][-10:]))
            line_count += 1
        csv_read.close()

    Q_mask = np.ma.masked_less(discharge,0)     # mask values less than 0 to ignore
    #Q_mask = np.ma.masked_invalid(np.asarray(discharge))    # mask missing and 'nan' instances
    date_mask = np.ma.masked_where(np.ma.getmask(Q_mask) == True, date) # mask dates containing missing discharge data
    Q_data = np.ma.compressed(Q_mask).tolist()          # create list with only valid dishcharge data
    final_date = np.ma.compressed(date_mask).tolist()   # create list with corresponding date
    
    if len(final_date) != len(Q_data):
        print 'WARNING -- Date and Discharge Data not the same length'
    
    basin_gauge = QME.split('_')[0].rstrip('.qme').upper() # basin/gage name
    basins_list.append(basin_gauge)
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
    
    ###### create plot of dates of data availability
    print 'Adding basin data to plot...'
    y_pos = [count] * len(final_date)
    ax1.plot(final_date, y_pos, '|',mew=0.5,ms=7)
    #if basin_gauge == 'DCTN1':
    #    break
    
print 'Adding plot attributes...'
ax1.xaxis.set_major_locator(mdates.YearLocator(5))
ax1.xaxis.set_minor_locator(years)
plt.yticks(range(1,len(basins_list)+1),basins_list)
plt.xlabel('Date (1960-2016)') 
plt.ylim(0,len(basins_list)+0.5)
plt.xlim(datetime.datetime(1960,1,1), datetime.datetime(2016,1,1))
plt.savefig(figname, dpi=200,bbox_inches='tight')   
plt.close()
    
new_summary.close()
print 'Completed!!'