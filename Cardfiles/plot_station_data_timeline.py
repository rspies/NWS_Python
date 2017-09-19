#Created on February 23, 2017
#@author: rspies@lynkertech.com
# Python 2.7
# This script creates an horizontal bar chart of station data availability 
# for precip/temp data sites

import os
import numpy as np
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.ioff()

os.chdir("../..") # change dir to \\AMEC\\NWS
maindir = os.getcwd()

############ User input ################
variable = 'temp'       # choices: 'ptpx'
RFC = 'APRFC_FY2017'
fxgroup = 'NWAK'
plot_stations = 'all'   # choices: 'all' or 'pxpp_input' ### pxpp_input will ignore the stations in the ignore_file and not plot
networks = ['nhds_daily','raws_hourly']  # choices: 'raws_hourly','asos_hourly','nhds_daily','nhds_hourly','scan_hourly','CONAGUA'
workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep + RFC[:5] + os.sep + RFC + os.sep + 'MAP_MAT_development' + os.sep +'station_data'
figname =  workingdir + os.sep + 'station_summaries' + os.sep + 'data_timeline_plots' + os.sep + RFC + '_' + fxgroup + '_' + variable + '_' + plot_stations + '.png'
yearstart = 1960; yearend = 2016;  # start and end years for plotting
########################################

########## define data timeline figure ###
fig, ax1 = plt.subplots(figsize=(11,9))        
plt.title(variable.upper() + ' Station Data Availability Timeline',fontsize=14)
basins_list = []; count = 0
years = mdates.YearLocator()   # every year

for network in networks:
    print '\n**** ' + network + ' stations:'
    timestep = network.split('_')[1]
    ignore_sites = []
    if network[:4] == 'raws' or network[:4] == 'asos' or network[:4] == 'scan':
        card_dir = workingdir + os.sep + network +os.sep + 'cardfiles_' + variable + os.sep + fxgroup + os.sep
        station_file =   workingdir + os.sep + 'station_summaries' + os.sep + fxgroup + '_' + network[:4] + '_summary_' + variable + '_' + timestep + '.csv'
        ignore_file = workingdir + os.sep + network + os.sep + fxgroup  + '_ignore_stations.csv'
    if network[:4] == 'nhds' or network[:4] == 'usgs':
        if variable == 'temp' and network == 'nhds_daily':
            card_dir = workingdir + os.sep + network[:4] + '_' + timestep +os.sep + 'tamx' + os.sep + 'cardfiles' + os.sep + fxgroup + os.sep
            station_file =  workingdir + os.sep + 'station_summaries' + os.sep + network[:4] + '_summary_tamx_' + timestep + '_' + fxgroup + '.csv'
        else:
            card_dir = workingdir + os.sep + network[:4] + '_' + timestep +os.sep + variable + os.sep + 'cardfiles' + os.sep + fxgroup + os.sep
            station_file =  workingdir + os.sep + 'station_summaries' + os.sep + network[:4] + '_summary_' + variable + '_' + timestep + '_' + fxgroup + '.csv'
        ignore_file = workingdir + os.sep + network + os.sep + fxgroup  + '_ignore_stations.csv'
    if network[:4] == 'CONA':
        card_dir = workingdir + os.sep + 'CONAGUA'  + os.sep + variable + os.sep + 'cardfiles' + os.sep + timestep + os.sep
        station_file =  workingdir + os.sep + network.split('_')[0] + '_summary_' + variable + '_' + timestep + '.csv'
        ignore_file = workingdir + os.sep + network.split('_')[0] + '_all'  + '_ignore_stations.csv'

    if variable == 'temp':
        cards = [f for f in os.listdir(card_dir) if os.path.isfile(os.path.join(card_dir, f)) and f.endswith('.tmx')]
    else:
        cards = [f for f in os.listdir(card_dir) if os.path.isfile(os.path.join(card_dir, f))]
    print cards
    ## read list of stations to ignore if plotting only pxpp input sites
    if plot_stations == 'pxpp_input':
        read_ignore = open(ignore_file,'r')
        for site in read_ignore:
            ignore_sites.append(site.rstrip('\n')[-4:])
        read_ignore.close()

    for card in cards:
        if card.split('-')[1].upper() not in ignore_sites:
            print card
            count += 1
            if network[:4] == 'raws' or network[:4] == 'asos': 
                csv_read = open(card_dir + '\\' + card, 'r')
                data = []; date = []
                ### read card file formatted .txt files lists
                line_count = 0
                for line in csv_read:
                    if line_count >= 7: # ignore header lines
                        if line_count == 8:
                            sep = line.split()
                            ### parse date columns
                            month = str(sep[1])[:-2]
                            year = str(sep[1])[-2:]
                            if int(year) <= 17:
                                year = int(year) + 2000 # assume years <= 17 are in the 2000s
                            else:
                                year = int(year) + 1900
                            hour = int(sep[2])
                            day = 1
                            full_date = datetime.datetime(year,int(month),int(day),int(hour))
                            date.append(full_date)
                            data.append(float(sep[-1][-10:]))
                        else:
                            sep = line.split()
                            if len(sep) > 0: # ignore blank lines
                                if variable == 'temp':
                                    full_date += timedelta(days=1)
                                else:
                                    full_date += timedelta(hours=1)
                                date.append(full_date)
                                data.append(float(sep[-1][-10:]))
                    line_count += 1
                csv_read.close()
            if network[:4] == 'nhds': 
                csv_read = open(card_dir + '\\' + card, 'r')
                data = []; date = []; last_month = 13; mday_count = 1
                ### read card file formatted .txt files lists
                line_count = 0
                for line in csv_read:
                    if line_count >= 3: # ignore header lines
                        sep = line.split()
                        if len(sep) > 0: # ignore blank lines
                            if len(sep) < 4 and len(sep[-1]) < 10: # some QME files (from RFC) may not have gage/basin id as 1st index
                                sep.insert(0,'0000')
                            ### parse date columns
                            month = str(sep[1])[:-2]
                            year = str(sep[1])[-2:]
                            if int(year) <= 17:
                                year = int(year) + 2000 # assume years <= 17 are in the 2000s
                            else:
                                year = int(year) + 1900
                            if timestep == 'daily':
                                day = str(sep[2])
                                if len(sep[-1]) > 10: # check for large streamflow values that get combined with day column
                                    day = str(sep[2])[:-10]
                                if month != last_month:
                                    last_month = month
                                    mday_count = 1
                                for each in sep[3:]:
                                    day = mday_count 
                                    full_date = datetime.datetime(year,int(month),int(day))
                                    date.append(full_date)
                                    data.append(float(sep[-1][-10:]))
                                    mday_count += 1
                            if timestep == 'hourly':
                                if line_count == 3:
                                    month = str(sep[1])[:-2]
                                    year = str(sep[1])[-2:]
                                    if int(year) <= 17:
                                        year = int(year) + 2000 # assume years <= 17 are in the 2000s
                                    else:
                                        year = int(year) + 1900
                                    day = 1; hour = 1
                                    full_date = datetime.datetime(year,int(month),int(day),int(hour))
                                for each in sep[3:]:
                                    date.append(full_date)
                                    data.append(float(each))
                                    full_date += timedelta(hours=1)
                                                                      
                    line_count += 1
                csv_read.close()
        
            Q_mask = np.ma.masked_less(data,0)     # mask values less than 0 to ignore
            #Q_mask = np.ma.masked_invalid(np.asarray(discharge))    # mask missing and 'nan' instances
            date_mask = np.ma.masked_where(np.ma.getmask(Q_mask) == True, date) # mask dates containing missing discharge data
            Q_data = np.ma.compressed(Q_mask).tolist()          # create list with only valid dishcharge data
            final_date = np.ma.compressed(date_mask).tolist()   # create list with corresponding date
            
            if len(final_date) != len(Q_data):
                print 'WARNING -- Date and Discharge Data not the same length'
            
            basin_gauge = card.split('.')[0].upper() # basin/gage name
            basins_list.append(basin_gauge)
            day_count = str(len(Q_data))            # number of valid daily data values
            start_date = str(min(final_date))       # date of first measurement
            end_date = str(max(final_date))         # date of last measurement
            
        
            #new_summary.write(basin_gauge+','+day_count+','+start_date+','+end_date+','+mean_Q+','
            #+str(max_Q)+','+str(min_Q)+','+sd+','+date_max+','+date_min+'\n')    
            
            ###### create plot of dates of data availability
            print 'Adding site data to plot...'
            y_pos = [count] * len(final_date)
            ax1.plot(final_date, y_pos, '|',mew=0.5,ms=14)
    
print 'Adding plot attributes...'
ax1.xaxis.set_major_locator(mdates.YearLocator(5))
ax1.xaxis.set_minor_locator(years)
plt.yticks(range(1,len(basins_list)+1),basins_list)
plt.xlabel('Date (1960-2016)')
plt.ylabel('Station ID')
plt.ylim(0,len(basins_list)+0.5)
plt.xlim(datetime.datetime(yearstart,1,1), datetime.datetime(yearend,1,1))
plt.savefig(figname, dpi=200,bbox_inches='tight')   
plt.close()
    
print 'Completed!!'