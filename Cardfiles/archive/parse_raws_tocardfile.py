# created by Ryan Spies 
# 3/3/2015
# Python 2.7
# Description: parse through a individual RAWS data files from WRCC 
# and generate formatted cardfile. Also creates a summary csv file
# with calculated valid data points and percent of total. Used to display in arcmap
# Stitches together data prior to 2004 (WRCC RAWS) and post 2004 data (RAWS site)
# datacard format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part7/_pdf/72datacard.pdf
# WRCC RAWS data: http://www.wrcc.dri.edu/cgi-bin/fpa_stations.pl?map=AK
# RAWS site: http://www.raws.dri.edu/index.html
# Features: day of year coversion to date, padded zero integer format

import os
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import glob
maindir = os.getcwd()
workingdir = maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep +'raw_data'

################### user input #########################
variable = 'temp'  # choices: 'ptpx' or 'temp'
timestep = 'hourly' # choices: 'hourly' 
state = 'AK'
data_files = workingdir + os.sep + 'raws_' + timestep +os.sep 
station_file = workingdir + os.sep + 'raws_' + timestep +os.sep + '18593-METADATA.txt'
out_dir = workingdir + os.sep + 'raws_' + timestep +os.sep + 'cardfiles_' + variable + os.sep
summary_file = open(workingdir + os.sep + 'raws_summary_' + variable + '_' + timestep + '.csv','w')
########################################################

summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL\n')
station_summary = {}
read_stations = open(station_file,'r')
for line in read_stations:
    if line[0] != '+' and line[:2] != '| ':
        sep = filter(None,line.split('|'))
        name = sep[0].strip()
        number = sep[6].strip()
        site_id = sep[5].strip()
        lat = sep[7].strip(); lon = sep[8].strip(); elev = sep[9].strip()
        station_summary[site_id] = [name,number,lat,lon,elev]
read_stations.close()
        
if variable == 'temp':
    data_type = variable.upper(); dim = 'TEMP'; unit = 'DEGF'; inter = '1'; exts = ['.tmn','.tmx','.tpt']
if variable == 'ptpx':
    data_type = variable.upper(); dim = 'L'; unit = 'IN'; inter = '1'; exts = ['.ptp']
if timestep == 'hourly':
    year_factor = float(24*365)
if timestep == 'daily':
    year_factor = float(365)

### loop through data files with 1983-2004 data
for data_file in glob.glob(data_files+'/*vDec05.dat'):
    print 'Parsing raw data files...'
    print os.path.basename(data_file)
    read_data = open(data_file,'r') 
    count_all = 0; count_missing = 0
    site_data = {}  
    site_data_daily = {}
    for each in read_data:
        if each[:1] != '#' and each[:7] != 'station':
            line = each.split(',')
            site_id = line[0].upper()
            if variable == 'temp':
                data = line[7]
            if variable == 'ptpx':
                data = line[6]
            date_time = dt.datetime(int(line[1]),int(line[3]),int(line[4]),int(str(line[5])[:2]),int(str(line[5])[2:4]))      
            changemin = date_time.minute
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if str(data) != 'M' and str(data) != 'M\n': # ignore missing data -> filled in below (-999)
                if round_dt in site_data:
                    site_data[round_dt].append(float(data))
                else:
                    site_data[round_dt] = [float(data)]
                ### also store temp data in daily lists within site_data_daily dictionary -> tmax and tmin calculations
                if variable == 'temp':
                    if round_dt.replace(hour=1,minute=0) in site_data_daily:
                        site_data_daily[round_dt.replace(hour=1,minute=0)].append(float(data))
                    else:
                        site_data_daily[round_dt.replace(hour=1,minute=0)] = [float(data)]
    
    ### open 2nd file containing data for 2004+
    data_file2 =data_files + site_id + '-2004_2015.dat'
    print os.path.basename(data_file2)
    read_data2 = open(data_file2,'r')
    accum_prec = 'M' # set to missing to ignore fist hour of data (no previous value to calculate accum change)
    for each in read_data2:
        if each[:1] == 'a':
            line = each.split(',')
            site_id = line[0].upper()
            date_time = dt.datetime.strptime(line[1]+ ' ' +line[2] + ' ' +str(line[5])[:2]+ ' ' +str(line[5])[2:], '%Y %j %H %M')     
            changemin = date_time.minute
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if variable == 'temp':
                data = line[7].strip()
                if round_dt not in site_data and data != 'M': # only add data to list if doesn't already have data for a date-time
                    site_data[round_dt]=[float(data)]
                    ### also store temp data in daily lists within site_data_daily dictionary -> tmax and tmin calculations
                    if round_dt.replace(hour=1,minute=0) in site_data_daily:
                        site_data_daily[round_dt.replace(hour=1,minute=0)].append(float(data))
                    else:
                        site_data_daily[round_dt.replace(hour=1,minute=0)] = [float(data)]
            if variable == 'ptpx':
                test_prec = line[6].strip()
                if str(test_prec) != 'M' and str(test_prec) != 'M\n': # ignore missing data -> filled in below (-999)
                    if accum_prec != 'M': # ignore fist hour of data file (no previous value to calculate accum change)
                        if test_prec >= accum_prec: # calculate the hourly precip value from the accumulation values from current and previous hour
                            data = float(test_prec) - float(accum_prec)
                        else:
                            data = float(test_prec) # date-time value set to accum value after accum has reset from previous timestep
                        accum_prec = test_prec # set accum_prec for next hours calculation
                        if round_dt not in site_data: # only add data to list if doesn't already have data for a date-time
                            site_data[round_dt]=[float(data)]
                    else:
                        accum_prec = test_prec

    read_data2.close()
    read_data.close()
    
    print 'Writing data to cardfile...'
    # NOTE: UNIX requires a binary file to properly read end line formats - 'wb'
    for ext in exts:
        print 'Creating -> ' + ext + ' file'
        min_date = min(site_data); max_date = max(site_data); iter_date = min_date
        # need to be sure that the first data point starts on day 1 hour 1
        if iter_date.day != 1 or iter_date.hour != 1:
            iter_date = iter_date + relativedelta(months=+1)
            iter_date = dt.datetime(iter_date.year,iter_date.month,1,1,0)
            min_date = iter_date
        month_count = 0; previous_month = 13 # use these for calculating line number for month/year lines
        if timestep == 'hourly' and variable == 'ptpx':
            site_label = state + '-' + site_id + '-HLY'
        else:
            site_label = state + '-' + site_id + '-DLY'
        cardfile = open(out_dir + site_label + '.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb')
        if ext == '.ptp' or ext == '.tpt':
            timestep = 1
        else: # daily tmax and tmin cardfiles
            timestep = 24
        ###### header info ######        
        cardfile.write('$ Data downloaded from WRCC RAWS download\n')
        cardfile.write('$ Data processed from hourly text files using python script\n')
        cardfile.write('$ Ryan Spies ryan.spies@amecfw.com\n')
        cardfile.write('$ Data Generated: ' + str(datetime.now())[:10] + '\n')
        cardfile.write('$\n')
        cardfile.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('datacard', variable.upper(), dim,unit,int(timestep),site_label,station_summary[site_id][0]))
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
            if ext == '.ptp' or ext == '.tpt':
                if iter_date in site_data:
                    valid_count += 1
                    if ext == '.ptp':
                        out_data = max(site_data[iter_date])
                    if ext == '.tpt':
                        out_data = np.mean(site_data[iter_date])
                else:
                    out_data = -999
                    miss_count += 1
            if ext == '.tmx' or ext == '.tmn':
                if iter_date in site_data_daily:
                    valid_count += 1
                    if ext == '.tmx' and len(site_data_daily[iter_date]) >= 20:
                        out_data = np.max(site_data_daily[iter_date])
                    if ext == '.tmn' and len(site_data_daily[iter_date]) >= 20:
                        out_data = np.min(site_data_daily[iter_date])
                else:
                    out_data = -999
                    miss_count += 1
            cardfile.write('{:12s}{:2d}{:02d}{:4d}{:9.2f}'.format(site_label,int(iter_date.month),int(str(iter_date.year)[-2:]),month_count,float(out_data)))
            cardfile.write('\n')
            previous_month = int(iter_date.month)
            iter_date = iter_date + dt.timedelta(hours=timestep)
        cardfile.close()
        if ext == '.tpt' or ext == '.ptp':
            summary_file.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+'\n')
summary_file.close() 
print 'Completed!'