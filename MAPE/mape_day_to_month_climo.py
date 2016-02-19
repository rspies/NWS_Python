# Ryan Spies
# 12/12/2014
# This script calculates a climatology mean monthly PE timeseries for each basin

#!!!!!!!!!!! Units left in degrees F !!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!! Data must be 6 hour time steps !!!!!!!!!!!!!!!!!!!!!!

import os
import numpy as np
from dateutil import parser
import csv
import datetime
path = os.getcwd()

######################## User Input Section ############################
rfc = 'SERFC'
# give directory of original RFC MAPE .csv files (exported from CHPS)
mape_dir = 'P:\\NWS\\Calibration_NWS\\' + rfc + '\\Calibration_TimeSeries\\mape_test\\from_CHPS'
start_date = datetime.datetime(2010,1,1,0) # only use data after this date
end_date = datetime.datetime(2014,11,30,23) # only use data before this date
###################### End User Input ##################################

rfc_files = os.listdir(mape_dir)
rfc_basins = []
for name in rfc_files:
    if name.endswith('.csv'): # only use text files in diretory
        rfc_basins.append(name)

month_num = [1,2,3,4,5,6,7,8,9,10,11,12]
csvfile = open('P:\\NWS\\Calibration_NWS\\' + rfc + '\\Calibration_TimeSeries\\mape_test\\' + rfc + '_monthly_climo.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['Mean Monthly Climo MAPE (mm/day)'])
writer.writerow(['Basin', 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])

for files in rfc_files:
    basin = files[:6].rstrip('_')
    basin_title = str.upper(basin)
    print basin_title
    output = [basin_title]

    # enter file locations for old and new files
    file1 = mape_dir + '\\' + files              
    month_data= {}
    fg = open(file1,'r')
    count = 0; values = 0
    # create a dictionary with daily data grouped into months
    print 'Creating dictionary with daily data grouped into monthly data...'
    for each in fg:
        if count >1:
            spl = each.split(',')
            date = parser.parse(spl[0])
            mn_index = str(date.month)
            pe_value = spl[1]
            if pe_value != '' and date >= start_date and date <= end_date:
                if float(pe_value) > 0.0:
                    values += 1
                    if mn_index in month_data:
                        month_data[mn_index].append(float(pe_value)*25.4)
                    else:
                        month_data[mn_index] = [float(pe_value)*25.4]
        count += 1
    fg.close()
    print 'Daily data values used: ' + str(values)
    
    # calculate average monthly data (mid_month value)
    print 'Calculating avg MAPE for each month...'
    for each in month_num:
        month_mean = np.mean(month_data[str(each)])
        output.append(str(round(month_mean,2)))

    # write to new csv file: the mean daily values for each month
    print 'writing data to csv file...'
    writer.writerow(output)
    
csvfile.close()
print 'Finito!!!'
