#Created on 1/23/2015
#@author: rspies
# Python 2.7
# This script reads CHPS csv file from QIN plot display and finds the start and end 
# of the observed hourly QIN record, # of valid data points, and % of total available.
# Outputs summary data to csv file

import os
import sys
import pandas as pd
import datetime
maindir = os.getcwd()[:-6]

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
RFC = 'WGRFC_FY2015'
sim_type = 'initial' # choices: initial (prior to calib), final (final calib), working (currently in calib process)
csv_loc = maindir + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type + os.sep + 'QIN_SQIN' + os.sep
summary_out = open(maindir + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type + os.sep + 'SQIN_QIN_stat_summary.txt','w')
basins_1hr = ['JNXT2','BKCT2','CTKT2','CMKT2','TNGT2']
################  Define the corresponding column of data in the csv file  #################
call_date = 0
call_sqin = 2
call_qin = 4
############ End User input ##################################################
summary_out.write('Basin' + '\t' + '# of hourly values analyzed' + '\t' + 'pbias' + '\t' + 'MAE' + '\t' + 'correlation coef.\n')
csv_files = os.listdir(csv_loc)
for csv_file in csv_files:
    basin_name = csv_file.split('_')[0]
    print basin_name
    if basin_name == 'CMKT2':
        call_date = 0
        call_sqin = 3
        call_qin = 5
    elif basin_name == 'TNGT2':
        call_date = 0
        call_sqin = 4
        call_qin = 6
    else:
        call_date = 0
        call_sqin = 2
        call_qin = 4
    if basin_name in basins_1hr:
        csv_read = open(csv_loc + os.sep + csv_file,'r')
        ###### tab delimitted CHPS QIN dishcarge CSV file into panda arrays ###########
        test = pd.read_csv(csv_read,sep=',',skiprows=2,
                usecols=[call_date,call_sqin,call_qin],parse_dates=['date'],names=['date','SQIN','QIN'])
        ### assign column data to variables
        
        date_qin = test['date'].tolist()                  # convert to list (indexible)
        all_qin = test['QIN'].tolist()
        all_sqin = test['SQIN'].tolist()
        sqin = []; qin = []; count = 0                 # read the data into a dictionary (more efficient processing)
        missing = 0
        for each in all_qin:
            if float(each) >= 0 and float(all_sqin[count]) >= 0:          # ignore data less than 0 
                if float(each) >= 0.5:     # ignore low flows below 0.5cms (17cfs)           
                    qin.append(each)
                    sqin.append(all_sqin[count])
            else:
                missing += 1
            count += 1
        csv_read.close() 
        sys.path.append(os.getcwd() + os.sep + 'modules')
        import calc_errors
        pbias = calc_errors.pct_bias(qin,sqin)
        mae = calc_errors.ma_error(qin,sqin)
        corr_coef = calc_errors.corr_coef(qin,sqin)[1][0]
    
        summary_out.write(basin_name + '\t' + str(len(qin)) + '\t' + str("%.2f" % pbias) + '\t' + str("%.2f" % mae) + '\t' + str("%.2f" % corr_coef) + '\n')
summary_out.close()

print 'Finished!'
print datetime.datetime.now()