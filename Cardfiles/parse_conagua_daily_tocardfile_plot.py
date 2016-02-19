# created by Ryan Spies 
# 3/3/2015
# Python 2.7
# Description: parse through a individual CONAGUA csv files to cardfile
# Features: dms to dd conversion
# Plot features: datelocator for axis, subplots, tick label modifications

import os
import sys
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt
plt.ioff()
import matplotlib.dates

os.chdir('../..')
maindir = os.getcwd()
workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep +'WGRFC_FY2015'+ os.sep +'raw_data'
startTime = datetime.now()
################### user input #########################
variable = 'ptpx'  # choices: 'ptpx' or 'temp'
timestep = 'daily' # choices: 'hourly' 
station_plot = 'on' # creates a summary bar plot for each station -> choices: 'on' or 'off'
state = 'MX'
mx_state = 'Coahuila' # choices: 'Coahuila' or 'Chihuahua'
data_files = workingdir + os.sep + 'CONAGUA' +os.sep + 'ptpx' + os.sep + timestep + os.sep + mx_state
out_dir = workingdir + os.sep + 'CONAGUA' +os.sep + 'ptpx' + os.sep + 'cardfiles'
summary_file = open(workingdir + os.sep + 'CONAGUA_summary_' + variable + '_' + timestep + '_' + mx_state.lower() + '.csv','w')
bad_ptpx_file = workingdir + os.sep + 'CONAGUA' + os.sep + 'questionable_ptpx_check_' + timestep + '.txt'
elev_file = workingdir + os.sep + 'CONAGUA' +os.sep + 'station_elev_extract.csv'
########################################################

### read through the metadata file for station info ###
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')

### define temp and precip variable info ###        
if variable == 'ptpx':
    data_type = {'.ptp':'PTPX'}; dim = 'L'; unit = 'IN'; exts = ['.ptp']
    thresh = 200.0 # max precip set to 8in
    set_miss_dates = [] # set specific dates to missing (if known to be bad precip)
    bad_ptpx_summary = open(bad_ptpx_file,'wb')
    station_summary = {}; elev_summary = {}
    elev_site = open(elev_file,'r') # file generated with ArcGIS "extract multi values to points" tool
    for row in elev_site:
        spl = row.split(',')
        if spl[0] != 'FID':
            elev_ft = float(spl[15].rstrip())*3.28084 # GTOP0_1K elevation converted from meters to feet
            elev_summary[spl[2]]=("%.0f" % elev_ft)

sys.path.append(os.getcwd() + os.sep + 'Python' + os.sep + 'modules')
import conversions    

### loop through data files with 1983-2004 data
for data_file in os.listdir(data_files):
    print 'Parsing raw data files...'
    read_data = open(data_files + os.sep + data_file,'r') 
    count_all = 0; count_missing = 0
    site_data = {}  
    site_data_daily = {}
    for each in read_data:
        count_all += 1
        line = each.split(',')
        if count_all == 1: # header 1st line
            sep1 = line[0].split('(')
            name = (sep1[0].rstrip()).strip('"') # station name in header
            site_id = sep1[1][:5].upper()
            print site_id
            # parse DMS in header line
            sep2 = sep1[2].replace('\xb0',',')
            sep2 = sep2.replace("'",',')
            sep2 = sep2.replace(")",'')
            sep2 = sep2.split(',')
            sep2 = filter(None,sep2)
            # use conversion module for dms to dd
            lat = str("%.3f" % (conversions.dms_to_dd(sep2[0],sep2[1],sep2[2],'N')))
            lon = str("%.3f" % (conversions.dms_to_dd(sep2[3],sep2[4],sep2[5],'W')))
            if mx_state == 'Coahuila':
                elev_summary[site_id] = str("%.0f" % (int(line[1].strip('"'))*3.28084))
            station_summary[site_id] = [name,lat,lon,elev_summary[site_id]]
        if count_all >= 3:
            data = line[1]
            date_time = datetime.strptime(line[0],'%d/%m/%Y')      

            if str(data) != '' and str(data) != '\n': # ignore missing data -> filled in below (-999)
                if variable == 'ptpx':
                    if float(data) < thresh and float(data) >= 0.0: # QA/QC bad precip values
                        if date_time.date() not in set_miss_dates:
                            site_data[date_time]=[float(data)/25.4]
                        else:
                            if float(data) == 0.00:
                                site_data[date_time]=[float(data)]
                    if float(data) >= thresh:
                        bad_ptpx_summary.write(str(site_id) + '  ' + str(date_time) + '  ' + str(data) + '\n')
    read_data.close()
    
    print 'Writing data to cardfile...'
    # NOTE: UNIX requires a binary file to properly read end line formats - 'wb'
    for ext in exts:
        print 'Creating -> ' + ext + ' file'
        min_date = min(site_data); max_date = max(site_data); iter_date = min_date
        # need to be sure that the first data point starts on day 1 hour 1
        if iter_date.day != 1 or iter_date.hour != 1:
            iter_date = iter_date + relativedelta(months=+1)
            iter_date = dt.datetime(iter_date.year,iter_date.month,1,0,0)
            min_date = iter_date
        month_count = 0; previous_month = 13 # use these for calculating line number for month/year lines
        if timestep == 'hourly':
            site_label = state + '-' + site_id + '-HLY'
            step_time = 1
            year_factor = float(24*365)
        else:
            site_label = state + '-' + site_id + '-DLY'
            step_time = 24
            year_factor = float(365)
        #cardfile = open(out_dir + site_label + '_RAWS.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb')
        cardfile = open(out_dir + os.sep +site_label + '_CONA' + ext,'wb')
        ###### header info ######        
        cardfile.write('$ Data provided by CONAGUA\n')
        cardfile.write('$ Data processed from hourly text files using python script\n')
        cardfile.write('$ Ryan Spies rspies@lynkertech.com\n')
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
            if iter_date in site_data:
                valid_count += 1
                out_data = np.mean(site_data[iter_date])
            else:
                out_data = -999
                miss_count += 1
            if out_data != -999 :
                plot_dict[iter_date] = float(out_data) # apped data to plot dictionary
                    
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
            plt.title(station_summary[site_id][0] + ', MX - CONAGUA (' + site_id + ')', fontsize=16)
    
            ax2 = plt.subplot(212, sharex=ax1)
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
            plt.savefig(workingdir + os.sep + 'CONAGUA' + os.sep + 'station_data_plots_' + timestep + os.sep + site_label, bbox_inches='tight')    
            plt.close()
        
        ### write to summary csv files and taplot files ###
        print 'Writing summary and taplot files...'
        if ext == '.tpt' or ext == '.ptp':
            summary_file.write(station_summary[site_id][0]+','+str(site_id)+','+station_summary[site_id][1]+','+station_summary[site_id][2]+','+station_summary[site_id][3]+
            ','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year) +',' + str(max_date.year) + '\n')


if variable == 'ptpx':
    bad_ptpx_summary.close() 
summary_file.close() 
print 'Completed!'
print 'Running time: ' + str(datetime.now() - startTime)