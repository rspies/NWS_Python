# created by Ryan Spies 
# 2/19/2015
# Python 2.7
# Description: parse through a summary file of NHDS site info obtained from website
# and split out individual cardfiles for each site. Also creates a summary csv file
# with calculated valid data points and percent of total. Used to display in arcmap

import os
import datetime
import dateutil.parser
import collections

os.chdir("../..")
maindir = os.getcwd()

################### user input #########################
RFC = 'APRFC_FY2017'
state = 'ANAK'
workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep +RFC[:5] + os.sep + RFC + os.sep + 'MAP_MAT_development' + os.sep +'station_data'
variable = 'ptpx'  # choices: 'ptpx', 'tamn', or 'tamx'
timestep = 'daily' # choices: 'hourly' or 'daily'
station_plot = 'on' # creates a summary bar plot for each station -> choices: 'on' or 'off'
summer_thresh = 6; winter_thresh = 5 #precip thresholds (inches) to flag and possibly set to missing
############# files/dir below must exist ####################
station_file =  workingdir + os.sep + 'nhds_' + timestep +os.sep + 'nhds_site_locations_' + timestep + '_' + state + '.txt'
daily_obs_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + 'nhds_site_obs_time_' + state + '.csv'
data_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + variable + os.sep + 'dipper_download' + os.sep + state.lower() + '_' + variable + '_' + timestep + '_1960_2016.txt'
out_dir = workingdir + os.sep + 'nhds_' + timestep +os.sep + variable + os.sep + 'cardfiles' + os.sep + state + os.sep
bad_ptpx_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + 'questionable_ptpx_check_' + timestep + '_' + state + '.txt'
user_bad_data_list = workingdir + os.sep + 'nhds_' + timestep +os.sep + variable + os.sep + 'CHPS_suspect_map.csv'
#################### end user input ########################

if station_plot == 'on':
    print 'Importing plotting modules...'
    import matplotlib
    import matplotlib.pyplot as plt
    plt.ioff()
    import pandas as pd
    import numpy as np

if variable == 'tamn':
    ext = '.tmn'; taplot = 'nhds_' + variable + '.taplot'; tap_open = open(workingdir + os.sep + 'nhds_' + timestep + os.sep + variable + os.sep + taplot, 'wb')
if variable == 'tamx':
    ext = '.tmx'; taplot = 'nhds_' + variable + '.taplot'; tap_open = open(workingdir + os.sep + 'nhds_' + timestep + os.sep + variable + os.sep + taplot, 'wb')
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
summary_file = open(workingdir + os.sep + 'station_summaries' + os.sep + 'nhds_summary_' + variable + '_' + timestep + '_' + state + '.csv','w')
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,MISSING_DATA,TOTAL_DATA,YEARS_DATA,PCT_AVAIL,YEAR_START,YEAR_END\n')
station_summary = {}; elev_list = []; site_name_id = {}
read_stations = open(station_file,'r')
for line in read_stations:
    if line[0] != '#':
        name = line[13:40].strip()      # find the station name
        number = line[40:47].strip()    # find the station id num (6 digit)
        site_id = number.split()[1]     # find the station id num (4 digit)
        total_id = number.replace(' ','') # full station id with no spaces
        split = filter(None,line[47:].strip().split('   ')) # filter out blank entries in list
        lat = split[0]; lon = '-' +split[1]; elev = split[2].strip(); types = split[-1]
        station_summary[site_id] = [name,number,lat,lon,elev]
        site_name_id[name] = total_id
        elev_list.append(float(elev)) # used to fin max/min for taplot header line

### parse observation time csv file for daily data (taplot card) ###        
if timestep == 'daily':
    if variable == 'tamn' or variable == 'tamx':
        daily_obs = {}
        obs_time = open(daily_obs_file,'r')
        for line in obs_time:
            sep = line.split(',')
            if sep[0].strip() != 'LOCATION' and sep[0].strip() != '':
                daily_obs[sep[0]] = sep[8]
        obs_time.close()
        
### taplot header line ###
if variable == 'tamn' or variable == 'tamx':
    if len(station_summary) <= 26:
        total_stations =  len(station_summary)
    else:
        total_stations = 26
    units = 'ENGL'
    desc = "'NW Alaska Stations'"
    max_elev = max(elev_list); min_elev = min(elev_list)
    tap_open.write('@A ')
    tap_open.write('{:2d} {:4s} {:30s} {:4.0f} {:4.0f}'.format(total_stations,units,desc,max_elev,min_elev))
    tap_open.write('\n')
    
### parse data and create individual datacard files ###
read_data = open(data_file,'r') 
site_check = 'xxxx' # dummy site check to ignore first few empty lines
count_all = 0; count_missing = 0; prev_month = 13; day_count = 0     
for each in read_data:
    if each[:8] == 'datacard':
        start_header = each
        header = each.split()
        site_check = header[5]
        site_id_data = header[5].split('-')[1] # find the station id num (4 digit)
    if each[:1] == ' ' or each[:1] == '1': # find the second line of each site's header to start new cardfile
        if len(filter(None,each.split())) <= 7: # ignore station data at end of temp data
            header2 = each.split()
            date_start = header2[0] + header2[1]; date_end = header2[2] + header2[3]
            #cardfile = open(out_dir + header[5] + '_NHDS.' + date_start + '.' + date_end + ext,'wb') # <- name may be too long for MAT input card
            cardfile = open(out_dir + header[5] + '_NHDS' + ext,'wb')            
            cardfile.write(start_header)
            cardfile.write(each)
            plot_dict = {}
            plot_dict = collections.OrderedDict(plot_dict) # ordered dictionary
            
    if variable == 'tamn' or variable == 'tamx': # find the taplot lines for temperature data
        if each[:1] == ' ' or each[:1] == '1' or each[:1] == '@' or each[:1] == '-':
            if each[:2] == '@F':
                name = each[5:25].strip()
                lat_taplot = float(each[29:].split()[0]); lon_taplot = float(each[29:].split()[1]); elev_taplot = int(float(each[29:].split()[3]))
                if site_name_id[name] in daily_obs:
                    time_of_obs = int(daily_obs[site_name_id[name]])/100
                else:
                    print 'Observation time not available for: ' + name + ' -- ' + site_name_id[name] + ' -> using 1700 as estimate'
                    time_of_obs = int(17)
                if len(name) <= 15:
                    tap_open.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+name + ' NHDS'+"'",lat_taplot,lon_taplot,time_of_obs,elev_taplot))
                else:
                    tap_open.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+name +"'",lat_taplot,lon_taplot,time_of_obs,elev_taplot))
                tap_open.write('\n')
            elif each[:2] == '@G' or each[:2] == '@H': # find taplot lines at end of data
                tap_open.write(each.rstrip() + ' ')
            elif len(filter(None,each.split())) >= 7:
                tap_open.write(' '.join(each.split()))
                tap_open.write('\n')
    if each[:1] != '$' and each[:11] == site_check: # find data lines corresponding to the current site id
        parse = each[20:].strip().split() # parse through data in columns 4-9 in each line of data
        if len(each[:20].split()[1]) < 6:
            parse_month = int((each[:20].split()[1])[:-2])
            parse_year = int((each[:20].split()[1])[-2:])
        else:
            parse_month = int((each[:20].split()[1])[:-6])
            parse_year = int((each[:20].split()[1])[-6:-4])
        if parse_year <= 16: # parse all 2000+ years up to 2016
            parse_year = parse_year + 2000
        else:
            parse_year = parse_year + 1900
        if parse_month >=4 and parse_month <= 9:
            thresh = summer_thresh
        else:
            thresh = winter_thresh
        for value in parse:
            count_all += 1
            if value == '-999.00':
                count_missing += 1
        if variable == 'ptpx':
            check_list = []
            for value in parse:
                check_list.append(float(value))
            if any(check >= thresh for check in check_list) == True: # check if any values in line are >= thresh (inches)
                bad_ptpx_summary.write(each) # write instance to questionable_ptpx_check_.txt 
                if any(check >= thresh for check in check_list) == True: # replace values with new_value = value/10
                    cardfile.write(each[:22])
                    for value in parse:
                        if parse_month == prev_month:
                            day_count += 1
                        else:
                            day_count = 1
                            prev_month = parse_month
                        if timestep == 'daily':
                            day_check = datetime.datetime(parse_year,parse_month,day_count)
                        if timestep == 'hourly':
                            hour_count = datetime.timedelta(hours=day_count)
                            day_check = datetime.datetime(parse_year,parse_month,1) + hour_count
                        if float(value) >= thresh:
                            #new_value = float(value)/10 # in cold climates use this when assuming precip was recorded as snow depth
                            new_value = -999.00 # replace erroneous values with missing
                            cardfile.write("%7.2f" % new_value)
                            cardfile.write('  ')
                            #plot_dict[day_check] = float(new_value)
                        else:
                            cardfile.write("%7.2f" % float(value))
                            cardfile.write('  ')
                            if float(value) >= 0.0:
                                plot_dict[day_check] = float(value)
                    cardfile.write('\n')
            else:
                if timestep == 'daily' or timestep == 'hourly':
                    cardfile.write(each[:22])
                    for value in parse:
                        if parse_month == prev_month:
                            day_count += 1
                        else:
                            day_count = 1
                            prev_month = parse_month
                        if timestep == 'daily':
                            day_check = datetime.datetime(parse_year,parse_month,day_count)
                        if timestep == 'hourly':
                            hour_count = datetime.timedelta(hours=day_count)
                            day_check = datetime.datetime(parse_year,parse_month,1) + hour_count
                        if day_check.date in set_miss_dates:
                            if float(value) >= (thresh):
                                new_value = -999.00
                                cardfile.write("%7.2f" % new_value)
                                cardfile.write('  ')
                                bad_ptpx_summary.write(site_check + ' ' + str(day_check.date) + ' old_value: ' + str(value) + ' new_value: ' + str(new_value) + '\n') # write instance to questionable_ptpx_check_.txt 
                            else:
                                cardfile.write("%7.2f" % float(value))
                                cardfile.write('  ')
                                if float(value) >= 0.0:
                                    plot_dict[day_check] = float(value)
                        else:
                            cardfile.write("%7.2f" % float(value))
                            cardfile.write('  ')
                            if float(value) >= 0.0:
                                plot_dict[day_check] = float(value)
                    cardfile.write('\n')
                else:
                    cardfile.write(each)
        else:
            cardfile.write(each) 
    if each[:1] == '$' and count_all > 0: # find the break btw station data -> calculate site summary
        percent_data = round(((count_all - count_missing)/float(count_all))*100,1)
        station_summary[site_id_data].append(count_missing)
        station_summary[site_id_data].append(count_all-count_missing)
        station_summary[site_id_data].append(round((count_all-count_missing)/year_factor,2))
        station_summary[site_id_data].append(percent_data)
        station_summary[site_id_data].append(date_start[-4:])
        station_summary[site_id_data].append(date_end[-4:])
        count_all = 0; count_missing = 0
        print site_id_data + ' -> ' + str(percent_data) + '%'
        prev_month = 13
        
        if ext == '.ptp' and station_plot == 'on':
            ### save hourly precip data to pandas dataframe, reample, and plot
            print 'Creating plot of daily and monthly station data... '
            df = pd.DataFrame(plot_dict.items(), columns=['Date_Time', 'ptp'])
            #df.reset_index(level=[0, 1], inplace=True)
            #resample_df_daily = df.set_index('Date_Time')['ptp'].resample('D', how='sum')# resample to daily
            resample_df_daily = df.set_index('Date_Time')['ptp'].resample('D', how='sum')# resample to daily
            resample_df_monthly = df.set_index('Date_Time')['ptp'].resample('M', how='sum')# resample to monthly
            plot_dates_monthly = resample_df_monthly.index.to_pydatetime(); plot_data_monthly = resample_df_monthly.values.tolist()
            if timestep == 'daily':     
                plot_dates_daily = resample_df_daily.index.to_pydatetime(); plot_data_daily = resample_df_daily.values.tolist()
                #plot_dates_daily = df.Date_Time; plot_data_daily = df.ptp
            if timestep == 'hourly':
                resample_df_daily = df.set_index('Date_Time')['ptp'].resample('D', how='sum')# resample to monthly
                plot_dates_daily = resample_df_daily.index.to_pydatetime(); plot_data_daily = resample_df_daily.values.tolist()
    
            fig = plt.subplots(figsize=(16,10))
            ax1 = plt.subplot(211)
            ax1.bar(plot_dates_daily, plot_data_daily, color ='k') # plot data
            ax1.set_ylabel('Daily Precip (in)')#; ax1.set_xlabel('Date')
            ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
            plt.xticks(rotation='vertical')
            ax1.grid(True)
            plt.title(station_summary[site_id_data][0] + ' NHDS (' + site_check + ')', fontsize=16)
    
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
            plt.savefig(workingdir + os.sep + 'nhds_' + timestep +os.sep + 'station_data_plots' + os.sep + state + os.sep + site_check)#, bbox_inches='tight')    
            plt.close()
        
### populate summary csv file
for site in station_summary:
    for item in station_summary[site]:
        summary_file.write(str(item) + ',')
    summary_file.write('\n')

summary_file.close()
if variable == 'tamn' or variable == 'tamx':
    tap_open.close() 
if variable == 'ptpx':
    bad_ptpx_summary.close() 
cardfile.close()
read_stations.close()
print 'Completed!'
