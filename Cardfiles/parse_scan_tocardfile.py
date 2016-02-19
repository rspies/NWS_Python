# created by Ryan Spies 
# 3/3/2015
# Python 2.7
# Description: parse through a individual SCAN data files from NRCS SCAN website 
# and generate formatted cardfile. Also creates a summary csv file
# with calculated valid data points and percent of total. Used to display in arcmap
# datacard format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part7/_pdf/72datacard.pdf
# SCAN site: http://www.wcc.nrcs.usda.gov/scan/
# Features: accumulated to hourly conversion

import os
import datetime as dt
from datetime import datetime
import dateutil
from dateutil.relativedelta import relativedelta
import numpy as np
import glob
maindir = os.getcwd()
workingdir = maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep +'raw_data'
startTime = datetime.now()

################### user input #########################
variable = 'temp'  # choices: 'ptpx' or 'temp'
timestep = 'hourly' # choices: 'hourly' 
state = 'AK'
data_files = workingdir + os.sep + 'scan_' + timestep + os.sep + variable + os.sep
station_file = workingdir + os.sep + 'scan_' + timestep +os.sep + 'METADATA.txt'
out_dir = workingdir + os.sep + 'scan_' + timestep + os.sep + 'cardfiles_' + variable + os.sep
summary_file = open(workingdir + os.sep + 'scan_summary_' + variable + '_' + timestep + '.csv','w')
########################################################

summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
station_summary = {}; all_elev = []
read_stations = open(station_file,'r')
for line in read_stations:
    if line[0] != '+' and line[:2] != '| ':
        sep = filter(None,line.split('|'))
        name = sep[0].strip()
        number = sep[6].strip()
        site_id = sep[5].strip()
        print site_id
        lat = sep[7].strip(); lon = sep[8].strip(); elev = sep[9].strip()
        station_summary[site_id] = [name,number,lat,lon,elev]
        all_elev.append(float(elev))
read_stations.close()
        
if variable == 'temp':
    data_type = {'.tmx':'TAMX','.tmn':'TAMN','.tpt':'TEMP'}; dim = 'TEMP'; unit = 'DEGF'; inter = '1'; exts = ['.tmx','.tmn','.tpt']
    card_label = '@A'; unit_type = 'ENGL'; info_header = "'KUSKOWIM BASINS SW ALASKA'"; max_elev = max(all_elev); min_elev = min(all_elev)
    weighting_factor = 20.; obs_time = 24 # obs time set to noon (using 24 hours of data)    
    if len(station_summary) <= 26:
        num_stations = len(station_summary)
    else:
        num_stations = 26
        print 'Warning -> more than 26 stations (taplot accepts a max of 26)'
    taplot = open(workingdir + os.sep + 'taplot_input' +os.sep + 'scan.taplot', 'wb')
    taplot.write('{:2s} {:2d} {:4s} {:30s} {:4d} {:4d}'.format(card_label,num_stations,unit_type,info_header,int(max_elev),int(min_elev)))
    taplot.write('\n')    
    summary_tmx = open(workingdir + os.sep + 'scan_summary_tamx' + '_' + timestep + '.csv','w')
    summary_tmn = open(workingdir + os.sep + 'scan_summary_tamn' + '_' + timestep + '.csv','w')
    summary_tmx.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
    summary_tmn.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
else:
    taplot = 'na' # define as na to determine if file needs to be closed later
    summary_tmx = 'na'
if variable == 'ptpx':
    data_type = {'.ptp':'PTPX'}; dim = 'L'; unit = 'IN'; inter = '1'; exts = ['.ptp']

### loop through data files with 1983-2004 data
for site_id in station_summary:
    site_data = {}; site_data_daily = {}
    site_tamx_monthly = {}; site_tamn_monthly = {}
    for data_file in glob.glob(data_files+'/'+site_id + '*'):
        print 'Parsing raw data files...'
        print os.path.basename(data_file)
        read_data = open(data_file,'r') 
        count_all = 0; count_missing = 0
        accum_prec = 'M' # set to missing to ignore fist hour of data (no previous value to calculate accum change)
        for each in read_data:
            line = each.split(',')
            if line[0].strip() == site_id:
                data = line[3].strip()
                date_time = dateutil.parser.parse(line[1] + ' ' + line[2])      
                changemin = date_time.minute
                # round sub-hourly data points up to nearest hour
                if int(changemin) != 0:
                    changet = dt.timedelta(minutes=(60-int(changemin)))
                    round_dt = date_time + changet
                else:
                    round_dt = date_time
                if variable == 'temp':
                    if round_dt not in site_data and data != 'M': # only add data to list if doesn't already have data for a date-time
                        site_data[round_dt] = [float(data)]
                        ### also store temp data in daily lists within site_data_daily dictionary -> tmax and tmin calculations
                        if round_dt.replace(hour=1,minute=0) in site_data_daily:
                            site_data_daily[round_dt.replace(hour=1,minute=0)].append(float(data))
                        else:
                            site_data_daily[round_dt.replace(hour=1,minute=0)] = [float(data)]
                if variable == 'ptpx':
                    test_prec = data
                    if str(test_prec) != 'M' and str(test_prec) != 'M\n': # ignore missing data -> filled in below (-999)
                        if accum_prec != 'M': # ignore fist hour of data file (no previous value to calculate accum change)
                            if test_prec >= accum_prec: # calculate the hourly precip value from the accumulation values from current and previous hour
                                data = float(test_prec) - float(accum_prec)
                            else:
                                data = float(test_prec) # date-time value set to accum value after accum has reset from previous timestep
                            accum_prec = test_prec # set accum_prec for next hours calculation
                            if round_dt not in site_data: # only add data to list if doesn't already have data for a date-time
                                if float(data) <= 4.0: # QA/QC hourly precip accum to be less than 4in/hr                                
                                    site_data[round_dt]=[float(data)]
                                else:
                                    print 'Set ppt to missing: ' + str(date_time) + ' -> ' + str(data)
                        else:
                            accum_prec = test_prec
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
        if timestep == 'hourly' or variable == 'ptpx' or ext == '.tpt':
            site_label = state + '-' + site_id + '-HLY'
        else:
            site_label = state + '-' + site_id + '-DLY'
        if ext == '.ptp' or ext == '.tpt':
            step_time = 1
            year_factor = float(24*365)
        else: # daily tmax and tmin cardfiles
            step_time = 24
            year_factor = float(365)
        #cardfile = open(out_dir + site_label + '_SCAN.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb') 
        cardfile = open(out_dir + site_label + '_SCAN' + ext,'wb')
        ###### header info ######        
        cardfile.write('$ Data downloaded from NRCS SCAN website\n')
        cardfile.write('$ Data processed from hourly/sub-hourly text files\n')
        cardfile.write('$ Ryan Spies ryan.spies@amecfw.com\n')
        cardfile.write('$ Data Generated: ' + str(datetime.now())[:19] + '\n')
        cardfile.write('$ Symbol for missing data = -999\n')
        cardfile.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('datacard', data_type[ext], dim,unit,int(step_time),site_label,name.upper()))
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
                if iter_date in site_data_daily and len(site_data_daily[iter_date]) >= 20:
                    valid_count += 1
                    if ext == '.tmx':
                        out_data = np.max(site_data_daily[iter_date])
                        if int(iter_date.month) in site_tamx_monthly:
                            site_tamx_monthly[int(iter_date.month)].append(out_data)
                        else:
                            site_tamx_monthly[int(iter_date.month)] = [out_data]
                    if ext == '.tmn':
                        out_data = np.min(site_data_daily[iter_date])
                        if int(iter_date.month) in site_tamn_monthly:
                            site_tamn_monthly[int(iter_date.month)].append(out_data)
                        else:
                            site_tamn_monthly[int(iter_date.month)] = [out_data]
                else:
                    out_data = -999
                    miss_count += 1
            cardfile.write('{:12s}{:2d}{:02d}{:4d}{:9.2f}'.format(site_label,int(iter_date.month),int(str(iter_date.year)[-2:]),month_count,float(out_data)))
            cardfile.write('\n')
            previous_month = int(iter_date.month)
            iter_date = iter_date + dt.timedelta(hours=step_time)
        cardfile.close()
        ### write to summary csv files and taplot files ###
        if ext == '.tpt' or ext == '.ptp':
            summary_file.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)+','+str(max_date.year)+'\n')
        if ext == '.tmx':
            taplot.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+station_summary[site_id][0]+"'",abs(float(station_summary[site_id][2])),abs(float(station_summary[site_id][3])),obs_time,int(station_summary[site_id][4])))
            taplot.write('\n')            
            taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@G',weighting_factor,np.average(site_tamx_monthly[1]),np.average(site_tamx_monthly[2]),np.average(site_tamx_monthly[3]),np.average(site_tamx_monthly[4]),np.average(site_tamx_monthly[5]),np.average(site_tamx_monthly[6]),
            np.average(site_tamx_monthly[7]),np.average(site_tamx_monthly[8]),np.average(site_tamx_monthly[9]),np.average(site_tamx_monthly[10]),np.average(site_tamx_monthly[11]),np.average(site_tamx_monthly[12])))
            taplot.write('\n')             
            summary_tmx.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)+','+str(max_date.year)+'\n')
        if ext == '.tmn':
            taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@H',weighting_factor,np.average(site_tamn_monthly[1]),np.average(site_tamn_monthly[2]),np.average(site_tamn_monthly[3]),np.average(site_tamn_monthly[4]),np.average(site_tamn_monthly[5]),np.average(site_tamn_monthly[6]),
            np.average(site_tamn_monthly[7]),np.average(site_tamn_monthly[8]),np.average(site_tamn_monthly[9]),np.average(site_tamn_monthly[10]),np.average(site_tamn_monthly[11]),np.average(site_tamn_monthly[12])))
            taplot.write('\n')             
            summary_tmn.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)+','+str(max_date.year)+'\n')

if taplot != 'na':
    taplot.close()
if summary_tmx != 'na' and summary_tmn != 'na':
    summary_tmx.close(); summary_tmn.close()
summary_file.close() 
print 'Completed!'
print 'Running time: ' + str(datetime.now() - startTime)