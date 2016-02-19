# created by Ryan Spies 
# 3/2/2015
# Python 2.7
# Description: parse through a individual data files from IEM website
# (e.g. hourly ASOS) and generate formatted cardfile. Also creates a summary csv file
# with calculated valid data points and percent of total. Used to display in arcmap
# datacard format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part7/_pdf/72datacard.pdf

import os
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil
import numpy as np
import glob
maindir = os.getcwd()
workingdir = maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep +'raw_data'

################### user input #########################
variable = 'ptpx'  # choices: 'ptpx' or 'temp'
timestep = 'hourly' # choices: 'hourly' or 'daily'
state = 'AK'
data_files = workingdir + os.sep + 'asos_' + timestep +os.sep 
out_dir = workingdir + os.sep + 'asos_' + timestep +os.sep + 'cardfiles_' + variable + os.sep
########################################################
summary_file = open(workingdir + os.sep + 'asos_summary_' + variable + '_' + timestep + '.csv','w')
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL\n')

if variable == 'temp':
    data_type = variable.upper(); dim = 'D'; unit = 'F'; inter = '1'; ext = '.tpt'
if variable == 'ptpx':
    data_type = variable.upper(); dim = 'L'; unit = 'IN'; inter = '1'; ext = '.ptp'
if timestep == 'hourly':
    year_factor = float(24*365)
if timestep == 'daily':
    year_factor = float(365)
    
# loop through data files
for data_file in glob.glob(data_files+'/*.txt'):
    print os.path.basename(data_file)
    name = os.path.basename(data_file)[5:-4] # get the actual file name from the path
    read_data = open(data_file,'r') 
    count_all = 0; count_missing = 0
    site_data = {}  
    print 'Parsing raw data file...'
    for each in read_data:
        if each[:1] != '#' and each[:7] != 'station':
            line = each.split(',')
            site_id = line[0]; lon = line[2]; lat = line[3]; elev=''
            if variable == 'temp':
                data = line[4]
            if variable == 'ptpx':
                data = line[5]
            date_time = dateutil.parser.parse(line[1])
            changemin = date_time.minute
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if str(data) != 'M' and str(data) != 'M\n': # ignore missing data -> filled in below (-999)
                if variable == 'ptpx' and float(data) < 12.0 and float(data) >= 0.0:  # QA/QC remove unrealistic precip values              
                    if round_dt in site_data:
                        site_data[round_dt].append(float(data))
                    else:
                        site_data[round_dt] = [float(data)]
                if variable == 'temp':
                    if round_dt in site_data:
                        site_data[round_dt].append(float(data))
                    else:
                        site_data[round_dt] = [float(data)]
    read_data.close()
    min_date = min(site_data); max_date = max(site_data); iter_date = min_date
    # need to be sure that the first data point starts on day 1 hour 1
    if iter_date.day != 1 or iter_date.hour != 1:
        iter_date = iter_date + relativedelta(months=+1)
        iter_date = dt.datetime(iter_date.year,iter_date.month,1,1,0)
        min_date = iter_date
    month_count = 0; previous_month = 13 # use these for calculating line number for month/year lines
    if timestep == 'hourly':
        site_label = state + '-' + site_id + '-HLY'
    print 'Writing data to cardfile...'
    cardfile = open(out_dir + site_label + '.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb')
    ###### header info ######        
    cardfile.write('$ Data downloaded from Iowa Environmental Mesonet (ASOS/AWOS)\n')
    cardfile.write('$ Data processed from hourly/sub-hourly text files\n')
    cardfile.write('$ Ryan Spies ryan.spies@amecfw.com\n')
    cardfile.write('$ Data Generated: ' + str(datetime.now())[:19] + '\n')
    cardfile.write('$ Symbol for missing data = -999\n')
    cardfile.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('datacard', variable.upper(), dim,unit,int(inter),site_label,name))
    cardfile.write('\n')
    cardfile.write('{:2d}  {:4d} {:2d}   {:4d} {:2d}   {:8s}'.format(int(min_date.month), int(min_date.year), int(max_date.month),int(max_date.year),1,'F9.2'))
    cardfile.write('\n')
    ###### write formatted data #####
    valid_count = 0; miss_count = 0
    while iter_date <= max_date:
        if int(iter_date.month) == previous_month:
            month_count += 1
        else:
            month_count = 1
        if iter_date in site_data:
            valid_count += 1
            if variable == 'ptpx':
                out_data = max(site_data[iter_date]) # sub-hourly precip accumulates up to end of hour???
            if variable == 'temp':
                out_data = np.mean(site_data[iter_date]) 
        else:
            out_data = -999
            miss_count += 1
        cardfile.write('{:12s}{:2d}{:02d}{:4d}{:9.2f}'.format(site_label,int(iter_date.month),int(str(iter_date.year)[-2:]),month_count,float(out_data)))
        cardfile.write('\n')
        previous_month = int(iter_date.month)
        iter_date = iter_date + dt.timedelta(hours=1)
    cardfile.close()
    summary_file.write(str(name)+','+str(site_id)+','+str(lat)+','+str(lon)+','+str(elev)+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+'\n')

summary_file.close() 
print 'Completed!'
