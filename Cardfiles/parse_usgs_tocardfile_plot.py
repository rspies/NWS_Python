# created by Ryan Spies 
# 2/19/2015
# Python 2.7
# Description: parse through a summary file of usgs site info obtained from website
# and split out individual cardfiles for each site. Also creates a summary csv file
# with calculated valid data points and percent of total. Used to display in arcmap

import os
import datetime as dt
from dateutil.relativedelta import relativedelta
import dateutil
import dateutil.parser
import glob
import numpy as np

os.chdir("../..")
maindir = os.getcwd()

################### user input #########################
RFC = 'SERFC_FY2016'
state = 'GA'
workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep +RFC[:5] + os.sep + RFC + os.sep +'station_data'
variable = 'ptpx'  # choices: 'ptpx', 'tamn', or 'tamx'
timestep = 'daily' # choices: 'hourly' or 'daily'
dim = 'L'; unit = 'IN'
station_plot = 'off' # creates a summary bar plot for each station -> choices: 'on' or 'off'
summer_thresh = 12; winter_thresh = 12 #precip thresholds (inches) to flag and set missing
############# files/dir below must exist ####################
station_file =  workingdir + os.sep + 'usgs_' + timestep +os.sep + 'usgs_site_locations_' + timestep + '_' + state + '.txt'
#daily_obs_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + 'nhds_site_obs_time_' + state + '.csv'
data_dir = workingdir + os.sep + 'usgs_' + timestep +os.sep + variable + os.sep + 'download_data' + os.sep + state.upper()
out_dir = workingdir + os.sep + 'usgs_' + timestep +os.sep + variable + os.sep + 'cardfiles' + os.sep + state.upper() + os.sep
bad_ptpx_file = workingdir + os.sep + 'usgs_' + timestep +os.sep + 'questionable_ptpx_check_' + timestep + '_' + state + '.txt'
user_bad_data_list = workingdir + os.sep + 'usgs_' + timestep +os.sep + 'CHPS_suspect_map.csv'
#################### end user input ########################

if variable == 'tamn':
    ext = '.tmn'; taplot = 'usgs_' + variable + '.taplot'; tap_open = open(workingdir + os.sep + 'usgs_' + timestep + os.sep + variable + os.sep + taplot, 'wb')
if variable == 'tamx':
    ext = '.tmx'; taplot = 'usgs_' + variable + '.taplot'; tap_open = open(workingdir + os.sep + 'usgs_' + timestep + os.sep + variable + os.sep + taplot, 'wb')
if variable == 'ptpx':
    ext = '.ptp'
    bad_ptpx_summary = open(bad_ptpx_file,'wb')
    check_chps = open(user_bad_data_list,'r')
    set_miss_dates = []    
    for line in check_chps:     # check csv file with dates of suspect MAP data (from CHPS)
        date_chps = dateutil.parser.parse(line)
        set_miss_dates.append(date_chps.date())
if timestep == 'hourly':
    year_factor = float(24*365)
if timestep == 'daily':
    year_factor = float(365)

### parse summary file for station info ###
summary_file = open(workingdir + os.sep + 'station_summaries' + os.sep + 'usgs_summary_' + variable + '_' + timestep + '_' + state + '.csv','w')
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,TOTAL_DATA,YEARS_DATA,PCT_AVAIL,YEAR_START,YEAR_END\n')
station_summary = {}; elev_list = []
read_stations = open(station_file,'r')
for line in read_stations:
    if line[0] != '#':
        name = line[13:40].strip()      # find the station name
        number = line[40:47].strip()    # find the station id num (6 digit)
        site_id = number.split()[1]     # find the station id num (4 digit)
        split = filter(None,line[47:].strip().split('   ')) # filter out blank entries in list
        lat = split[0]; lon = '-' +split[1]; elev = split[2].strip(); types = split[5]
        station_summary[site_id] = [name,number,lat,lon,elev]
        elev_list.append(float(elev)) # used to fin max/min for taplot header line
        
### taplot header line ###
if variable == 'tamn' or variable == 'tamx':
    if len(station_summary) <= 26:
        total_stations =  len(station_summary)
    else:
        total_stations = 26
    units = 'ENGL'
    desc = "'Rio Grande'"
    max_elev = max(elev_list); min_elev = min(elev_list)
    tap_open.write('@A ')
    tap_open.write('{:2d} {:4s} {:30s} {:4.0f} {:4.0f}'.format(total_stations,units,desc,max_elev,min_elev))
    tap_open.write('\n')
    
### parse data and create individual datacard files ###
for data_file in glob.glob(data_dir+'/*.txt'):
    print os.path.basename(data_file)
    name = os.path.basename(data_file)[:-4] # get the actual file name from the path
    site_num = name.split('.')[0]
    read_data = open(data_file,'r') 
    count_all = 0; count_missing = 0
    site_data = {}; site_data_daily = {}
    site_tamx_monthly = {}; site_tamn_monthly = {}
    print 'Parsing raw data file...'
    for each in read_data:
        if each[:4] == 'USGS':
            line = each.split('\t')
            data = line[3]
            date_time = dateutil.parser.parse(line[2])
            changemin = date_time.minute
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if str(data) != 'M' and str(data) != '': # ignore missing data -> filled in below (-999)
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
                    ### also store temp data in daily lists within site_data_daily dictionary -> tmax and tmin calculations
                if variable == 'temp':
                    if round_dt.replace(hour=1,minute=0) in site_data_daily:
                        site_data_daily[round_dt.replace(hour=1,minute=0)].append(float(data))
                    else:
                        site_data_daily[round_dt.replace(hour=1,minute=0)] = [float(data)]
    read_data.close()
    print 'Writing data to cardfile...'
    # NOTE: UNIX requires a binary file to properly read end line formats - 'wb'
    print 'Creating -> ' + variable + ' file'
    min_date = min(site_data); max_date = max(site_data); iter_date = min_date
    # need to be sure that the first data point starts on day 1 hour 1
    if iter_date.day != 1 or iter_date.hour != 1:
        iter_date = iter_date + relativedelta(months=+1)
        iter_date = dt.datetime(iter_date.year,iter_date.month,1,0,0)
        min_date = iter_date
    month_count = 0; previous_month = 13 # use these for calculating line number for month/year lines
    if timestep == 'hourly':
        site_label = state + '-' + site_num + '-HLY'
    if timestep == 'daily':
        site_label = state + '-' + site_num + '-DLY'
    if timestep == 'hourly':
        step_time = 1
        year_factor = float(24*365)
    if timestep == 'daily': # daily tmax and tmin cardfiles
        step_time = 24
        year_factor = float(365)
    #cardfile = open(out_dir + site_label + '_ASOS.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb')
    cardfile = open(out_dir + site_label + ext,'wb')
    ###### header info ######        
    cardfile.write('$ Data downloaded from http://maps.waterdata.usgs.gov/mapper\n')
    cardfile.write('$ Data processed from downloaded text files\n')
    cardfile.write('$ Ryan Spies rspies@lynkertech.com\n')
    cardfile.write('$ Data Generated: ' + str(dt.datetime.now())[:19] + '\n')
    cardfile.write('$ Symbol for missing data = -999\n')
    cardfile.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('datacard', 'PTPX', dim,unit,int(step_time),site_label,name.upper()+'USGS'))
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
    if variable == 'ptpx':
        summary_file.write(station_summary[name][0]+','+station_summary[name][1]+','+station_summary[name][2]+','+station_summary[name][3]+','+station_summary[name][4]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)[-4:] +','+ str(max_date.year)[-4:] + '\n')
#    if variable == 'tmx':
#        taplot.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+str(name + ' ASOS')+"'",abs(float(lat)),abs(float(lon)),obs_time,int(site_elev[site_id])))
#        taplot.write('\n')            
#        taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@G',weighting_factor,np.average(site_tamx_monthly[1]),np.average(site_tamx_monthly[2]),np.average(site_tamx_monthly[3]),np.average(site_tamx_monthly[4]),np.average(site_tamx_monthly[5]),np.average(site_tamx_monthly[6]),
#        np.average(site_tamx_monthly[7]),np.average(site_tamx_monthly[8]),np.average(site_tamx_monthly[9]),np.average(site_tamx_monthly[10]),np.average(site_tamx_monthly[11]),np.average(site_tamx_monthly[12])))
#        taplot.write('\n')             
#        summary_tmx.write(str(name)+','+str(site_id)+','+str(lat)+','+str(lon)+','+str(site_elev[site_id])+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)[-4:] +','+ str(max_date.year)[-4:] + '\n')
#    if variable == 'tmn':
#        taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@H',weighting_factor,np.average(site_tamn_monthly[1]),np.average(site_tamn_monthly[2]),np.average(site_tamn_monthly[3]),np.average(site_tamn_monthly[4]),np.average(site_tamn_monthly[5]),np.average(site_tamn_monthly[6]),
#        np.average(site_tamn_monthly[7]),np.average(site_tamn_monthly[8]),np.average(site_tamn_monthly[9]),np.average(site_tamn_monthly[10]),np.average(site_tamn_monthly[11]),np.average(site_tamn_monthly[12])))
#        taplot.write('\n')             
#        summary_tmn.write(str(name)+','+str(site_id)+','+str(lat)+','+str(lon)+','+str(site_elev[site_id])+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)[-4:] +','+ str(max_date.year)[-4:] + '\n')
#
#if taplot != 'na':
#    taplot.close()
#if summary_tmx != 'na' and summary_tmn != 'na':
#    summary_tmx.close(); summary_tmn.close()
summary_file.close() 
print 'Completed!'
