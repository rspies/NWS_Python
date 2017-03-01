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

os.chdir("../..")
maindir = os.getcwd()
startTime = datetime.now()

################### user input #########################
RFC = 'APRFC_FY2017'
region = 'ANAK' # region used for grouping basin -> leave blank '' if not using
variable = 'ptpx'  # choices: 'ptpx' or 'temp'
timestep = 'hourly' # choices: 'hourly' or 'daily'
state = 'AK'
station_plot = 'on' # creates a summary bar plot for each station -> choices: 'on' or 'off'

workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep +RFC[:5] + os.sep + RFC+ os.sep +'MAP_MAT_development' + os.sep + 'station_data' 
if region == '':
    data_files = workingdir + os.sep + 'asos_' + timestep +os.sep + 'raw_data' + os.sep 
    out_dir = workingdir + os.sep + 'asos_' + timestep +os.sep + 'cardfiles_' + variable + os.sep
    bad_ptpx_file = workingdir + os.sep + 'asos_' + timestep +os.sep + 'questionable_ptpx_check_' + timestep + '.txt'
    summary_out = workingdir + os.sep + 'station_summaries' + os.sep + 'asos_summary_' + variable + '_' + timestep + '.csv'
else:
    data_files = workingdir + os.sep + 'asos_' + timestep +os.sep + 'raw_data' + os.sep + region + os.sep
    out_dir = workingdir + os.sep + 'asos_' + timestep +os.sep + 'cardfiles_' + variable + os.sep + region + os.sep
    bad_ptpx_file = workingdir + os.sep + 'asos_' + timestep +os.sep + region + '_questionable_ptpx_check_' + timestep + '.txt'
    summary_out = workingdir + os.sep + 'station_summaries' + os.sep + region + '_asos_summary_' + variable + '_' + timestep + '.csv'
elev_file = open(workingdir + os.sep + 'asos_' + timestep + os.sep + 'station_elev.csv','r')

########################################################
if station_plot == 'on':
    import matplotlib.pyplot as plt
    plt.ioff()
    import matplotlib.dates
    import pandas as pd
    import collections
if variable == 'ptpx':
    bad_ptpx_summary = open(bad_ptpx_file,'wb')

### read through the metadata file for station info ###
summary_file = open(summary_out,'w')
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,TOTAL_DATA,YEARS_DATA,PCT_AVAIL,YEAR_START,YEAR_END\n')

### read elev data file
all_elev = []; site_elev = {}; all_lat = {}; all_lon = {}; site_name = {}
for entry in elev_file:
    split = entry.split(',')
    if split[0] != 'SITE_ID':
        site = split[0]
        site_name[site] = split[1]
        all_elev.append(float(split[3]))
        site_elev[split[0]] = float(split[3])
        lon = float(split[5]); lat = float(split[4]) 
        all_lat[site] = lat; all_lon[site] = lon
    
### define temp and precip variable info ###
if variable == 'temp':
    data_type = {'.tmx':'TAMX','.tmn':'TAMN','.tpt':'TEMP'}; dim = 'TEMP'; unit = 'DEGF'; inter = '1'; exts = ['.tmx','.tmn','.tpt']
    card_label = '@A'; unit_type = 'ENGL'; info_header = "'FY17 CALB BASINS'"; max_elev = max(all_elev); min_elev = min(all_elev)
    weighting_factor = 20.; obs_time = 24 # obs time set to noon (using 24 hours of data)    
    if len(all_elev) <= 26:
        num_stations = len(all_elev)
    else:
        num_stations = 26
        print 'Warning -> more than 26 stations (taplot accepts a max of 26)'
    taplot = open(workingdir + os.sep + 'taplot_input' +os.sep + 'asos.taplot', 'wb')
    taplot.write('{:2s} {:2d} {:4s} {:30s} {:4d} {:4d}'.format(card_label,num_stations,unit_type,info_header,int(max_elev),int(min_elev)))
    taplot.write('\n')    
    summary_tmx = open(workingdir + os.sep + 'asos_summary_tamx' + '_' + timestep + '.csv','w')
    summary_tmn = open(workingdir + os.sep + 'asos_summary_tamn' + '_' + timestep + '.csv','w')
    summary_tmx.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
    summary_tmn.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,VALID_DATA,YEARS_VALID,PCT_AVAIL,YEAR_START,YEAR_END\n')
else:
    taplot = 'na' # define as na to determine if file needs to be closed later
    summary_tmx = 'na'
if variable == 'ptpx':
    data_type = {'.ptp':'PTPX'}; dim = 'L'; unit = 'IN'; inter = '1'; exts = ['.ptp']
    
# loop through data files
for data_file in glob.glob(data_files+'/*.txt'):
    print os.path.basename(data_file)
    #name = os.path.basename(data_file)[5:-4] # get the actual file name from the path
    read_data = open(data_file,'r') 
    count_all = 0; count_missing = 0
    site_data = {}; site_data_daily = {}
    site_tamx_monthly = {}; site_tamn_monthly = {}
    print 'Parsing raw data file...'
    for each in read_data:
        if each[:1] != '#' and each[:7] != 'station':
            line = each.split(',')
            site_id = line[0] 
            if variable == 'temp':
                data = line[-2]
            if variable == 'ptpx':
                data = line[-1]
            date_time = dateutil.parser.parse(line[1])
            changemin = date_time.minute
            if date_time.month >=4 and date_time.month <= 9: # set seasonal thresholds for potentially bad precip
                thresh = 5.0
            else:
                thresh = 3.0
            # round sub-hourly data points up to nearest hour
            if int(changemin) != 0:
                changet = dt.timedelta(minutes=(60-int(changemin)))
                round_dt = date_time + changet
            else:
                round_dt = date_time
            if str(data) != 'M' and str(data) != 'M\n': # ignore missing data -> filled in below (-999)
                if variable == 'ptpx' and float(data) < thresh and float(data) >= 0.0:  # QA/QC remove unrealistic precip values              
                    if round_dt in site_data:
                        site_data[round_dt].append(float(data))
                    else:
                        site_data[round_dt] = [float(data)]
                if variable == 'ptpx' and float(data) >= thresh:
                    bad_ptpx_summary.write(str(site_id) + '  ' + str(round_dt) + '  ' + str(data) + '\n')
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
        #cardfile = open(out_dir + site_label + '_ASOS.' + str(min_date.month) + str(min_date.year) + '.' + str(max_date.month) + str(max_date.year) + ext,'wb')
        cardfile = open(out_dir + site_label + '_ASOS' + ext,'wb')
        ###### header info ######        
        cardfile.write('$ Data downloaded from Iowa Environmental Mesonet (ASOS/AWOS)\n')
        cardfile.write('$ Data processed from hourly/sub-hourly text files\n')
        cardfile.write('$ Ryan Spies rspies@lynkertech.com\n')
        cardfile.write('$ Data Generated: ' + str(datetime.now())[:19] + '\n')
        cardfile.write('$ Symbol for missing data = -999\n')
        cardfile.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('datacard', data_type[ext], dim,unit,int(step_time),site_label,site_name[site_id].upper()))
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
                        plot_dict[iter_date] = float(out_data) # apped data to plot dictionary
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
            plt.title(site_name[site_id] + ' ASOS (' + site_id + ')', fontsize=16)
    
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
            plt.savefig(workingdir + os.sep + 'asos_' + timestep +os.sep + 'station_data_plots' + os.sep + site_label)#, bbox_inches='tight')    
            plt.close()
        
        ### write to summary csv files and taplot files ###
        if ext == '.tpt' or ext == '.ptp':
            summary_file.write(str(site_name[site_id])+','+str(site_id)+','+str(all_lat[site_id])+','+str(all_lon[site_id])+','+str(site_elev[site_id])+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)[-4:] +','+ str(max_date.year)[-4:] + '\n')
        if ext == '.tmx':
            taplot.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+str(site_name[site_id] + ' ASOS')+"'",abs(float(all_lat[site_id])),abs(float(all_lon[site_id])),obs_time,int(site_elev[site_id])))
            taplot.write('\n')            
            taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@G',weighting_factor,np.average(site_tamx_monthly[1]),np.average(site_tamx_monthly[2]),np.average(site_tamx_monthly[3]),np.average(site_tamx_monthly[4]),np.average(site_tamx_monthly[5]),np.average(site_tamx_monthly[6]),
            np.average(site_tamx_monthly[7]),np.average(site_tamx_monthly[8]),np.average(site_tamx_monthly[9]),np.average(site_tamx_monthly[10]),np.average(site_tamx_monthly[11]),np.average(site_tamx_monthly[12])))
            taplot.write('\n')             
            summary_tmx.write(str(site_name[site_id])+','+str(site_id)+','+str(all_lat[site_id])+','+str(all_lon[site_id])+','+str(site_elev[site_id])+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)[-4:] +','+ str(max_date.year)[-4:] + '\n')
        if ext == '.tmn':
            taplot.write('{:2s} {:3.0f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:4.1f}'.format('@H',weighting_factor,np.average(site_tamn_monthly[1]),np.average(site_tamn_monthly[2]),np.average(site_tamn_monthly[3]),np.average(site_tamn_monthly[4]),np.average(site_tamn_monthly[5]),np.average(site_tamn_monthly[6]),
            np.average(site_tamn_monthly[7]),np.average(site_tamn_monthly[8]),np.average(site_tamn_monthly[9]),np.average(site_tamn_monthly[10]),np.average(site_tamn_monthly[11]),np.average(site_tamn_monthly[12])))
            taplot.write('\n')             
            summary_tmn.write(str(site_name[site_id])+','+str(site_id)+','+str(all_lat[site_id])+','+str(all_lon[site_id])+','+str(site_elev[site_id])+','+str(miss_count)+','+str(valid_count)+','+str(round((valid_count/year_factor),2))+','+str((float(valid_count)/(miss_count+valid_count))*100)+','+str(min_date.year)[-4:] +','+ str(max_date.year)[-4:] + '\n')

if taplot != 'na':
    taplot.close()
if summary_tmx != 'na' and summary_tmn != 'na':
    summary_tmx.close(); summary_tmn.close()
summary_file.close() 
bad_ptpx_summary.close()
print 'Completed!'
print 'Running time: ' + str(datetime.now() - startTime)