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
# Features: day of year coversion to date, padded zero integer format, dict to pandas dataframe, resample dataframe
# Plot features: datelocator for axis, subplots, tick label modifications

import os
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil.parser
import numpy as np
import glob
import pandas as pd
import collections
import matplotlib.pyplot as plt
plt.ioff()
import matplotlib.dates

maindir = os.getcwd()
workingdir = maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep +'raw_data'
startTime = datetime.now()
################### user input #########################
variable = 'ptpx'  # choices: 'ptpx' or 'temp'
timestep = 'hourly' # choices: 'hourly' 
station_plot = 'on' # creates a summary bar plot for each station -> choices: 'on' or 'off'
state = 'AK'
data_files = workingdir + os.sep + 'raws_' + timestep +os.sep + 'raw_data' + os.sep 
station_file = workingdir + os.sep + 'raws_' + timestep +os.sep + '18593-METADATA.txt'
out_dir = workingdir + os.sep + 'raws_' + timestep +os.sep + 'cardfiles_' + variable + os.sep
summary_file = open(workingdir + os.sep + 'raws_summary_' + variable + '_' + timestep + '.csv','w')
bad_ptpx_file = workingdir + os.sep + 'raws_' + timestep +os.sep + 'questionable_ptpx_check_' + timestep + '.txt'
########################################################

### read through the metadata file for station info ###
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
station_summary = {}; all_elev = []
read_stations = open(station_file,'r')
for line in read_stations:
    if line[0] != '+' and line[:2] != '| ':
        sep = filter(None,line.split('|'))
        name = sep[0].strip()
        number = sep[6].strip()
        site_id = sep[5].strip()
        lat = sep[7].strip(); lon = sep[8].strip(); elev = sep[9].strip()
        station_summary[site_id] = [name,number,lat,lon,elev]
        all_elev.append(float(elev))
read_stations.close()

### define temp and precip variable info ###        
if variable == 'temp':
    data_type = {'.tmx':'TAMX','.tmn':'TAMN','.tpt':'TEMP'}; dim = 'TEMP'; unit = 'DEGF'; inter = '1'; exts = ['.tmx','.tmn','.tpt']
    card_label = '@A'; unit_type = 'ENGL'; info_header = "'KUSKOWIM BASINS SW ALASKA'"; max_elev = max(all_elev); min_elev = min(all_elev)
    weighting_factor = 20.; obs_time = 24 # obs time set to noon (using 24 hours of data)    
    if len(station_summary) <= 24:
        num_stations = len(station_summary)
    else:
        num_stations = 26
        print 'Warning -> more than 26 stations (taplot accepts a max of 26)'
    taplot = open(workingdir + os.sep + 'taplot_input' +os.sep + 'raws.taplot', 'wb')
    taplot.write('{:2s} {:2d} {:4s} {:30s} {:4d} {:4d}'.format(card_label,num_stations,unit_type,info_header,int(max_elev),int(min_elev)))
    taplot.write('\n')    
    summary_tmx = open(workingdir + os.sep + 'raws_summary_tamx' + '_' + timestep + '.csv','w')
    summary_tmn = open(workingdir + os.sep + 'raws_summary_tamn' + '_' + timestep + '.csv','w')
    summary_tmx.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
    summary_tmn.write('NAME,SITE_ID,LAT,LON,ELEV,NUMBER,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
else:
    taplot = 'na' # define as na to determine if file needs to be closed later
    summary_tmx = 'na'
if variable == 'ptpx':
    data_type = {'.ptp':'PTPX'}; dim = 'L'; unit = 'IN'; inter = '1'; exts = ['.ptp']
    bad_ptpx_summary = open(bad_ptpx_file,'wb')
    check_chps = open(maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep + 'CHPS_suspect_map.csv','r')
    set_miss_dates = []    
    for line in check_chps:     # check csv file with dates of suspect MAP data (from CHPS)
        date_chps = dateutil.parser.parse(line)
        set_miss_dates.append(date_chps.date())

### loop through data files with 1983-2004 data
for data_file in glob.glob(data_files+'/*vDec05.dat'):
    print 'Parsing raw data files...'
    print os.path.basename(data_file)
    read_data = open(data_file,'r') 
    count_all = 0; count_missing = 0
    site_data = {}  
    site_data_daily = {}; site_tamx_monthly = {}; site_tamn_monthly = {}
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
            # set hourly precip threshold based on season
            if date_time.day >=4 and date_time.day <= 9:
                thresh = 2.0
            else:
                thresh = 1.0
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if str(data) != 'M' and str(data) != 'M\n': # ignore missing data -> filled in below (-999)
                if variable == 'temp':
                    if float(data) != -32.0 and float(data) < 100.0: # QA/QC for temperature data
                        if round_dt in site_data:
                            site_data[round_dt].append(float(data))
                        else:
                            site_data[round_dt] = [float(data)]
                        ### also store temp data in daily lists within site_data_daily dictionary -> tmax and tmin calculations
                        if round_dt.replace(hour=1,minute=0) in site_data_daily:
                            site_data_daily[round_dt.replace(hour=1,minute=0)].append(float(data))
                        else:
                            site_data_daily[round_dt.replace(hour=1,minute=0)] = [float(data)]
                if variable == 'ptpx':
                    if float(data) < thresh and float(data) >= 0.0: # QA/QC bad precip values
                        if round_dt.date() not in set_miss_dates:
                            site_data[round_dt]=[float(data)]
                        else:
                            if float(data) == 0.00:
                                site_data[round_dt]=[float(data)]
                    if float(data) >= thresh:
                        bad_ptpx_summary.write(str(site_id) + '  ' + str(round_dt) + '  ' + str(data) + '\n')

   ######################## open 2nd file containing data for 2004+ ###########################
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
            # set hourly precip threshold based on season
            if date_time.day >=4 and date_time.day <= 9:
                thresh = 2.0
            else:
                thresh = 1.0
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if variable == 'temp':
                data = line[7].strip()
                if round_dt not in site_data and data != 'M': # only add data to list if doesn't already have data for a date-time
                    if float(data) != -32.0 and float(data) < 100.0: # QA/QC for temperature data
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
                            if data < thresh and data >= 0.0: # QA/QC bad precip values
                                if round_dt.date() not in set_miss_dates:
                                    site_data[round_dt]=[float(data)]
                                else:
                                    if float(data) == 0.00:
                                        site_data[round_dt]=[float(data)]
                            if data >= thresh:
                                bad_ptpx_summary.write(str(site_id) + '  ' + str(round_dt) + '  ' + str(data) + '\n')
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
        #cardfile = open(out_dir + site_label + '_RAWS.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb')
        cardfile = open(out_dir + site_label + '_RAWS' + ext,'wb')
        ###### header info ######        
        cardfile.write('$ Data downloaded from WRCC and RAWS download website\n')
        cardfile.write('$ Data processed from hourly text files using python script\n')
        cardfile.write('$ Ryan Spies ryan.spies@amecfw.com\n')
        cardfile.write('$ Data Generated: ' + str(datetime.now())[:10] + '\n')
        cardfile.write('$\n')
        cardfile.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('datacard', data_type[ext], dim,unit,int(step_time),site_label,station_summary[site_id][0].upper()))
        cardfile.write('\n')
        cardfile.write('{:2d}  {:4d} {:2d}   {:4d} {:2d}   {:8s}'.format(int(min_date.month), int(min_date.year), int(max_date.month),int(max_date.year),1,'F9.2'))
        cardfile.write('\n')
        ###### write formatted data #####
        valid_count = 0; miss_count = 0; plot_dict = {}
        plot_dict = collections.OrderedDict(plot_dict) # ordered dictionary
        
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
                if out_data != -999 :
                    plot_dict[iter_date] = float(out_data) # apped data to plot dictionary
                    
            ### convert hourly temp to daily tmin and tmax        
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
        
        if ext == '.ptp' and station_plot == 'on':
            ### save hourly precip data to pandas dataframe, reample, and plot
            print 'Creating plot of daily and monthly station data... '
            df = pd.DataFrame(plot_dict.items(), columns=['Date_Time', 'ptp'])
            #df.reset_index(level=[0, 1], inplace=True)
            resample_df_daily = df.set_index('Date_Time')['ptp'].resample('D', how='sum')# resample to daily
            resample_df_monthly = df.set_index('Date_Time')['ptp'].resample('M', how='sum')# resample to monthly
            plot_dates_daily = resample_df_daily.index.to_pydatetime(); plot_data_daily = resample_df_daily.values.tolist()
            plot_dates_monthly = resample_df_monthly.index.to_pydatetime(); plot_data_monthly = resample_df_monthly.values.tolist()
    
            fig = plt.subplots(figsize=(16,10))
            ax1 = plt.subplot(211)
            ax1.bar(plot_dates_daily, plot_data_daily, color ='k') # plot data
            ax1.set_ylabel('Daily Precip (in)')#; ax1.set_xlabel('Date')
            ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
            plt.xticks(rotation='vertical')
            ax1.grid(True)
            plt.title(station_summary[site_id][0] + ' RAWS (' + site_id + ')', fontsize=16)
    
            ax2 = plt.subplot(212)
            ax2.bar(plot_dates_monthly, plot_data_monthly, color ='k') # plot data
            ax2.set_ylabel('Monthly Precip (in)'); ax2.set_xlabel('Date')
            plt.xticks(rotation='vertical')
            ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator())
            mean_annual_ppt = 'Mean Annual Precip: ' + "%.2f" % (np.nanmean(plot_data_monthly)*12) + ' in'
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax2.text(0.75, 0.95, mean_annual_ppt, fontsize=13, transform=ax2.transAxes,
                    verticalalignment='top', bbox=props)
            #ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
            #ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%m'))
            #ax.tick_params(axis='x',labelsize=8, which = 'minor')
            ax2.grid(True)
            plt.savefig(workingdir + os.sep + 'raws_' + timestep +os.sep + 'station_data_plots' + os.sep + site_label)#, bbox_inches='tight')    
            plt.close()
        
        ### write to summary csv files and taplot files ###
        print 'Writing summary and taplot files...'
        if ext == '.tpt' or ext == '.ptp':
            summary_file.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year) +',' + str(max_date.year) + '\n')
        if ext == '.tmx':
            taplot.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+station_summary[site_id][0] + ' RAWS'+"'",abs(float(station_summary[site_id][2])),abs(float(station_summary[site_id][3])),obs_time,int(station_summary[site_id][4])))
            taplot.write('\n')            
            taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@G',weighting_factor,np.average(site_tamx_monthly[1]),np.average(site_tamx_monthly[2]),np.average(site_tamx_monthly[3]),np.average(site_tamx_monthly[4]),np.average(site_tamx_monthly[5]),np.average(site_tamx_monthly[6]),
            np.average(site_tamx_monthly[7]),np.average(site_tamx_monthly[8]),np.average(site_tamx_monthly[9]),np.average(site_tamx_monthly[10]),np.average(site_tamx_monthly[11]),np.average(site_tamx_monthly[12])))
            taplot.write('\n')             
            summary_tmx.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year) +',' + str(max_date.year) + '\n')
        if ext == '.tmn':
            taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@H',weighting_factor,np.average(site_tamn_monthly[1]),np.average(site_tamn_monthly[2]),np.average(site_tamn_monthly[3]),np.average(site_tamn_monthly[4]),np.average(site_tamn_monthly[5]),np.average(site_tamn_monthly[6]),
            np.average(site_tamn_monthly[7]),np.average(site_tamn_monthly[8]),np.average(site_tamn_monthly[9]),np.average(site_tamn_monthly[10]),np.average(site_tamn_monthly[11]),np.average(site_tamn_monthly[12])))
            taplot.write('\n')             
            summary_tmn.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][2]+','+station_summary[site_id][3]+','+station_summary[site_id][4]+','+
            station_summary[site_id][1]+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year) +',' + str(max_date.year) + '\n')

if taplot != 'na':
    taplot.close()
if summary_tmx != 'na' and summary_tmn != 'na':
    summary_tmx.close(); summary_tmn.close()
if variable == 'ptpx':
    bad_ptpx_summary.close() 
summary_file.close() 
print 'Completed!'
print 'Running time: ' + str(datetime.now() - startTime)