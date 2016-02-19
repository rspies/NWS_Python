#Created on 1/22/2015
#@author: rspies
# Python 2.7
# This script reads CHPS csv file from QIN plot display and finds the start and end 
# of the observed hourly QIN record, # of valid data points, and % of total available.
# Outputs summary data to csv file

import os
import sys
import pandas as pd
import datetime
os.chdir("../..")
maindir = os.getcwd()

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
RFC = 'WGRFC_FY2015'
#csv_loc = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + 'hourly' + os.sep + 'csv_from_chps'
csv_loc = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + 'initial' + os.sep + 'QIN_SQIN'
summary_out = open(maindir + os.sep + 'Calibration_NWS' + os.sep + RFC + os.sep + 'raw_data' + os.sep + 'chps_output' + os.sep + 'QIN_availability_summary.csv','w')
################  Define the corresponding column of data in the csv file  #################
call_date = 0
call_qin = 4
############ End User input ##################################################
summary_out.write('Basin' + ',' + 'Record Start' + ',' + 'Record End' + ',' + '# of hourly obs' + ',' + '% of available data\n')
csv_files = os.listdir(csv_loc)
for csv_file in csv_files:
    basin_name = csv_file.split('_')[0]
    print basin_name
    csv_read = open(csv_loc + os.sep + csv_file,'r')
    ###### tab delimitted CHPS QIN dishcarge CSV file into panda arrays ###########
    test = pd.read_csv(csv_read,sep=',',skiprows=2,
            usecols=[call_date,call_qin],parse_dates=['date'],names=['date', 'QIN'])
    ### assign column data to variables
    
    date_qin = test['date'].tolist()                  # convert to list (indexible)
    all_qin = test['QIN'].tolist()
    date_qin_filtered = {}; count = 0                 # read the data into a dictionary (more efficient processing)
    missing = 0
    for each_day in date_qin:
        if float(all_qin[count]) >= 0:          # ignore data less than 0 
            date_qin_filtered[each_day] = all_qin[count]
        else:
            missing += 1
        count += 1
    csv_read.close() 
    perct_qin = float(len(date_qin_filtered))/(float(len(date_qin_filtered))+missing)
    min_date = min(date_qin_filtered).date()
    max_date = max(date_qin_filtered).date()
    summary_out.write(basin_name + ',' + str(min_date) + ',' + str(max_date) + ',' + str(len(date_qin_filtered)) + ',' + "%.4f" % perct_qin + '\n')

# testing calc_errors module below    
#summary_out.close()
#os.chdir("Python")
#sys.path.append(os.getcwd() + os.sep + 'modules')
#import calc_errors
#aa = [1,2,3,4]
#bb = [8,7,6,5]
#pbias = calc_errors.pct_bias(aa,bb)
#print pbias
print 'Finished!'
print datetime.datetime.now()