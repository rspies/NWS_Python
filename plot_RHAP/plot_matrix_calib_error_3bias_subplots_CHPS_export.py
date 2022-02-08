#Created on July 7, 2014
#@author: rspies
# Python 2.7
# This script plots a raster image of an input stream dischare txt file

# using matplotlib imshow - could use pcolormesh:
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pcolormesh

import os
import matplotlib.pyplot as plt
#Turn interactive plot mode off (don't show figures)
plt.ioff()
import matplotlib.ticker as ticker
from matplotlib import cm
import matplotlib.image as imagei
from matplotlib.colors import LogNorm
import numpy as np
import pandas as pd
import datetime
os.chdir("../..")
maindir = os.getcwd() + os.sep + 'Calibration_NWS' + os.sep

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
RFC = 'WGRFC_2021'
fx_group = ''                   # set to blank '' if not using fx_groups
yr_begin = 2000; yr_final = 2020  # these are the default start/end years for plots
sim_type = 'initial'            # choices: initial (prior to calib) or final (final calib)
error_types = ['bias','accum']  # choices: pbias, bias, NAE (normalized absolute error)
fig_name = '_bias_pbias_' + sim_type    #' Calb Raster Analysis' or '_bias_pbias_test'
resolution = 350                #350->(for report figs) 100->for CHPS fx help tab display (E19)
add_obs_Q_plot = 'yes'          # yes/no to create a subplot of the observed data for same period
basin_ids = []                  # <-- use this to run specific basin(s)
ignore_basins = []

qme_sqme_input = os.path.abspath(r'G:\Shared drives\TWDB-WGRFC Hydro Calb\calibration_results\FINAL_simulation_files\QME_SQME')
out_dir = os.path.abspath(r'G:\Shared drives\TWDB-WGRFC Hydro Calb\calibration_results\FINAL_simulation_files\RHAP') + os.sep
wm_image = os.getcwd() + os.sep + 'Python' + os.sep + 'plot_RHAP' + os.sep + 'Lynker-Primary-Logo-96dpi.jpg' # lynker logo for plot
#log_dir = maindir + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + fx_group + os.sep + sim_type + os.sep + 'raster_hydrograph_plots' + os.sep
############################ End User input ###################################

### create log file to output summary of calibration period
log_file = open(out_dir + 'summary_info.txt','w')
log_file.write('Basin,start_date,end_date,daily_pts\n')
########### find all basin QME vs SQME .csv files ############
if len(basin_ids) == 0:
    basin_ids = []
    all_files = os.listdir(qme_sqme_input)
    for each in all_files:
        if each.endswith(".csv"):
                ch5id = each.split('_')[0]
                if ch5id not in ignore_basins:
                    basin_ids.append(ch5id)
#basin_ids=['APBA4']
########### loop through all desired basins and define min/max errors for plots ############
for basin_id in basin_ids:
    print(basin_id)
    calib_read = open(qme_sqme_input + os.sep + basin_id + '_QME_SQME.csv', 'r') #test!!!
    # output figure directory
    #out_dir = out_dir + os.sep + 'raster_hydrograph_plots' + os.sep 
    
    ###### tab delimitted CHPS calibrated AND Observed dishcarge text file into panda arrays ###########
    ### replaces hour time stamp with zero to create a mean daily value -> match obs data
    test = pd.read_csv(calib_read,sep=',',skiprows=2,
            usecols=[0,1,2],parse_dates=['date'],names=['date', 'QME', 'SQME'])
    ### assign column data to variables
    print('Populating data arrays for calibrated dishcarge... and converting to daily values')
    
    date_calib = test['date'].tolist()                  # convert to list (indexible)
    Q_calib = test['SQME'].tolist()
    date_Q_calib = {}; count = 0                        # read the data into a dictionary (more efficient processing)
    for each_day in date_calib:
        if yr_begin-2 <= int(each_day.year) <= yr_final+2: # find simulated data within 2 year buffer of start/end
            if each_day.replace(hour=0) in date_Q_calib:
                if float(Q_calib[count]) >= 0:          # ignore data less than 0 
                    date_Q_calib[each_day.replace(hour=0)].append(Q_calib[count])
            else:
                if float(Q_calib[count]) >= 0:
                    date_Q_calib[each_day.replace(hour=0)] = [Q_calib[count]]
        count += 1
    
    ###### tab delimitted CHPS observed data text file into panda arrays ###########
    ### replaces hour time stamp with zero to create a mean daily value -> match obs data
    date = test['date'].tolist() # convert to list (indexible)
    discharge = test['QME'].tolist()
    date_Q = {}; count = 0 # read the data into a dictionary (more efficient processing)
    for each_day in date:
        if yr_begin-2 <= int(each_day.year) <= yr_final+2: # find observed data within 2 year buffer of start/end
            if each_day.replace(hour=0) in date_Q:
                if float(discharge[count]) >= 0:
                    date_Q[each_day.replace(hour=0)].append(float(discharge[count]))
            else:
                if float(discharge[count]) >= 0:
                    date_Q[each_day.replace(hour=0)] = [float(discharge[count])]
        count += 1
    calib_read.close()
    
    ### set plot start date to earlist year with obs data or 2005 (largest)
    if len(date_Q) > 0:
        log_file.write(basin_id + ',' + str(min(date_Q).date()) + ',' + str(max(date_Q).date()) + ',') # log summary file output
        if min(date_Q).year > yr_begin:
            print('Obs data begins -> ' + str(min(date_Q).year))
            yr_start = int(min(date_Q).year)
            if int(min(date_Q).year) > 2005:
                yr_start = 2005
        else:
            yr_start = yr_begin
        ### set plot end date to last year with obs data or to default (yr_final)
        if max(date_Q).year > yr_final:
            print('Obs data ends -> ' + str(max(date_Q).year))
            yr_end = int(max(date_Q).year)
        else:
            yr_end = yr_final
    else:
        yr_start = yr_begin; yr_end = yr_final
        log_file.write(basin_id + ',na,na,') # log summary file output
    
    ################## Create matrix of observed and calibrated data #####################
    print('Creating matrix of data...')
    print('Ignoring leap days...')
    start=pd.datetime(yr_start,1,1); end=pd.datetime(yr_end,12,31); delta = datetime.timedelta(days=1)
    gage_Q = []
    print('Parsing daily observed gage dishcarge data...')
    while start <= end:
        date_loop = pd.to_datetime(start)
        #ignore leap year day (maintains equal matrix dimensions)
        if date_loop.month == 2 and date_loop.day == 29: 
            print('Ignoring: ' + str(date_loop))
        else:
            if date_loop in date_Q:
                if float(date_Q[date_loop][0]) < 0.0:       # replace negative Q with nan
                    gage_Q.append(np.nan)
                elif float(date_Q[date_loop][0]) <= 0.1:    # replace Q values btw 0.0 and 0.1 with 0.1 (log plotting issues)
                    gage_Q.append(0.1)
                else:
                    gage_Q.append(float(date_Q[date_loop][0])) # add each day of available data to new list
            else:
                gage_Q.append(np.nan)                       # set missing observed to nan (ignored in plot and analysis)
        start += delta
    
    ### check if any observed data is available - if not do not create a plot
    if np.count_nonzero(~np.isnan(gage_Q)) == 0: # count the non-nan values
        print('NO QME DATA AVIALABLE...')
        log_file.write('0\n') # log summary file output
    else: 
        print('Parsing daily calibrated dishcarge data...')
        log_file.write(str(np.count_nonzero(~np.isnan(gage_Q))) + '\n') # log summary file output
        start=pd.datetime(yr_start,1,1); chps_Q = []
        while start <= end:
            date_loop = pd.to_datetime(start)
            #ignore leap year day (maintains equal matrix dimensions)
            if date_loop.month == 2 and date_loop.day == 29: 
                print('Ignoring: ' + str(date_loop))
            else:
                if date_loop in date_Q_calib:
                    if float(np.average(date_Q_calib[date_loop])) < 0.0:    # replace negative Q with nan
                        chps_Q.append(np.nan)
                    elif float(np.average(date_Q_calib[date_loop])) <= 0.1:
                        chps_Q.append(0.1)
                    else:
                        chps_Q.append(np.average(date_Q_calib[date_loop]))  # add each day of available data to new list
                else:
                    chps_Q.append(np.nan)                                   #set missing observed to nan (ignored in plot and analysis)
            start += delta
        
        ### flip matrix upside down to plot most recent data on top
        ediff = (np.asarray(chps_Q)-np.asarray(gage_Q))#/np.asarray(gage_Q)
        ema = np.ma.masked_invalid(ediff)
        #eadd = np.cumsum(ema)
        error_cum = ema.reshape(int((len(gage_Q)/365)),365)
        obs_Q = np.flipud(np.asarray(gage_Q).reshape(int((len(gage_Q)/365)),365))
        calib_Q = np.flipud(np.asarray(chps_Q).reshape(int((len(chps_Q)/365)),365))
        fig = plt.figure(figsize=(8,10))
        cmap =cm.seismic_r 
        
        ### calculate plot coloring thresholds for bias and accum bias - based on obs data mean
        avg_flow = np.ma.mean(np.ma.masked_invalid(obs_Q))
        print('Mean flow: ' + str(avg_flow))
        if 0 <= avg_flow <= 1:
            cminb = -6; cmaxb = 6
            cmina = -100; cmaxa =100        
        elif 0 <= avg_flow <= 10:
            cminb = -100; cmaxb = 100
            cmina = -1000; cmaxa =1000
        elif 10 < avg_flow <= 20:
            cminb = -100; cmaxb = 100
            cmina = -2000; cmaxa =2000
        elif 20 < avg_flow <= 40:
            cminb = -100; cmaxb = 100
            cmina = -2000; cmaxa =2000
        elif 40 < avg_flow <= 60:
            cminb = -200; cmaxb = 200
            cmina = -3000; cmaxa =3000
        elif 60 < avg_flow <= 100:
            cminb = -200; cmaxb = 200
            cmina = -3000; cmaxa =3000
        elif 100 < avg_flow <= 200:
            cminb = -200; cmaxb = 200
            cmina = -3000; cmaxa =3000
        elif 200 < avg_flow <= 500:
            cminb = -300; cmaxb = 300
            cmina = -4000; cmaxa =4000
        elif 500 < avg_flow <= 1000:
            cminb = -500; cmaxb = 500
            cmina = -10000; cmaxa =10000
        elif 1000 < avg_flow <= 2000:
            cminb = -1000; cmaxb = 1000
            cmina = -20000; cmaxa =20000
        elif 2000 < avg_flow <= 3000:
            cminb = -1000; cmaxb = 1000
            cmina = -50000; cmaxa =50000
        else:
            cminb = -2500; cmaxb = 2500
            cmina = -100000; cmaxa =100000    
        
        ############################# create plot(s) ##########################################
        #######################################################################################
        for error_type in error_types:
            ### set all nan (masked array) values to grey  
            cmap.set_bad('k',0.3) # defining here seems to get applied to all plots?? (color,opacity)
            
            ########################## error calculations #####################################
            #  Bias = (calib-obs)
            if error_type == 'bias':
                error = (calib_Q-obs_Q)
                #error = np.ma.array(error, mask=np.isnan(error))
                text = 'SQME Daily Bias (cms)'
                label = 'Bias'
                #cmin = -50; cmax = 50
                cmin = cminb; cmax = cmaxb
                cmap =cm.seismic_r
                if add_obs_Q_plot == 'yes':
                    ax1 = fig.add_subplot(312)
                else:
                    ax1 = fig.add_subplot(212)     
                print('Creating Bias plot...')
                
            #  Accumulated Bias
            if error_type == 'accum':
                error = np.flipud(np.cumsum(error_cum,axis=1))
                #error = np.cumsum(((calib_Q-obs_Q)/obs_Q),axis=1).reshape((len(gage_Q)/365),365)
                text = 'SQME Annual Accumulated Bias (cms)'
                label = 'Accumbias'
                cmin = cmina; cmax = cmaxa
                cmap =cm.seismic_r
                if add_obs_Q_plot == 'yes':
                    ax1 = fig.add_subplot(313)
                else:
                    ax1 = fig.add_subplot(213)
                print('Creating Accumulated Bias plot...')
            
            #  %Bias = 100 * [(calib-obs)/obs]
            if error_type == 'pbias':
                error = 100*((calib_Q-obs_Q)/obs_Q)
                text = 'SQME Daily Percent Bias (%)'
                label = 'Pbias'
                cmin = -100; cmax = 100
                cmap =cm.seismic_r
                if add_obs_Q_plot == 'yes':
                    ax1 = fig.add_subplot(313)
                else:
                    ax1 = fig.add_subplot(213)
                print('Creating %Bias plot...')
        #    cmap.set_bad('k',0.3)
            
            
            ### create image: aspect set to auto (creates a square plot with any data)
            ### vmin->sets values less than 0 to missing
            image = ax1.imshow(error, cmap=cmap, aspect='auto',interpolation='none')#extent=[1,365,50,-50]
            image.set_clim(cmin,cmax)
            cbar = fig.colorbar(image,format='%.1f')#,extend='min',extendrect=True,extendfrac=.1)
            
            #### color bar and axis properties ###
            #cbar.ax.set_ylabel(text, rotation=270,labelpad=20,fontsize=10)
            cbar.ax.tick_params(labelsize=8)
            ax1.tick_params(axis='y', which='major', labelsize=8)
            ax1.tick_params(axis='x', which='major', labelsize=10)
            
            #### axis adjustments ####
            if yr_end-yr_start > 30: # reduces overcrowding of y-axis tick labels (less frequent ticks with longer data)
                ax1.locator_params(axis='y',nbins=(yr_end-yr_start)/2,tight=True) #set number of y ticks
            else:       
                ax1.locator_params(axis='y',nbins=(yr_end-yr_start),tight=True) #set number of y ticks
            ax1.xaxis.set_minor_locator(ticker.FixedLocator([31,59,90,120,151,181,212,243,273,304,334,365]))
            ax1.xaxis.set_major_locator(ticker.FixedLocator([15,45,74,105,135,166,196,227,258,288,319,349]))
            ax1.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
            ax1.xaxis.grid(b=True, which='minor', color='k', linestyle='--')
            
            ### set tick marks properties
            ax1.tick_params(which='minor', length=5,width=1.5)
            ax1.tick_params(axis='x',which='major', length=0,width=0)
            lala = ax1.yaxis.get_majorticklocs() # find the automatic tick mark locations
            
            # create a list of the years used in plot and add to the appropriate 
            # tick location
            yticks = []; all_years = []; new_labels = []
            start = yr_start
            while start <= yr_end:
                all_years.append(str(start))
                start += 1
            all_years.reverse()
            for each in lala:
                yticks.append(int(each))
            for each in yticks:
                if each < 0 or each == max(yticks):
                    new_labels.append('')
                else:
                    new_labels.append(all_years[each])
            ax1.set_yticklabels(new_labels)
            
            obs_Q = np.ma.masked_invalid(obs_Q)         # mask the observed nan data 
            if np.min(obs_Q) <10.0:
                    cmin = 1
            elif np.min(obs_Q) < 100.0:
                cmin = 10
            elif np.min(obs_Q) < 1000.0:
                cmin = 100
            else:
                cmin = 1000
            ticks_in = []
            tick_labels = []
            cmin_int = cmin
            if cmin <100 and avg_flow > 1000: # set cmin limit higher if avg flow is high
                obs_Q = np.ma.masked_less(obs_Q,100) # mask erroneously low flow values
                cmin_int = 100
            while cmin_int <= np.max(obs_Q):
                ticks_in.append(float(cmin_int))
                tick_labels.append(str(int(cmin_int)))
                cmin_int = cmin_int * 2
                
            #if np.max(obs_Q) > 1.0 and np.max(obs_Q) < 10.0:
            #        cmax = 10
            #if np.max(obs_Q) > 10.0 and np.max(obs_Q) < 100.0:
            #    cmax = 100
            #if np.max(obs_Q)> 100.0 and np.max(obs_Q) < 1000.0:
            #    cmax = 1000
            #if np.max(obs_Q) > 1000 and np.max(obs_Q) < 10000.0:
            #    cmax = 10000
            cmax = int(np.max(obs_Q))
            
            #### axis and title properties ###
            #ax1.set_xlabel('Day of Year')
            ax1.set_ylabel('Calendar Year',fontsize=10)
            ax1.set_title(basin_id + ': ' + text + ' ' + str(yr_start) + '-' + str(yr_end),fontsize=12)
        
        ############# optional: add side-by-side plot of observed dishcarge #################
        if add_obs_Q_plot == 'yes':
            ax2 = fig.add_subplot(311)
            #cmap.set_bad('w',1) 
            cmap=cm.jet_r
            cmap.set_bad('k',0.3)
            image = ax2.imshow(obs_Q, cmap=cmap, aspect='auto', norm=LogNorm(),interpolation='none')#extent=[1,365,50,-50]
            image.set_clim(cmin,cmax)
            cbar = fig.colorbar(image,shrink=0.9,format='%i',ticks = ticks_in,extendfrac=.1)#extend='min', extendrect=True
            cbar.ax.set_yticklabels(tick_labels) 
            #ax1.text(398,39, 'Missing',fontsize = 9)#, style='italic')#,bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
            #ax1.text(380,24, 'Max: ' + str(int(np.max(obs_Q))), fontsize = 9)    
            
            #### color bar properties ###
            text = 'Daily QME (cms)'
            #cbar.ax.set_ylabel(text, rotation=270,labelpad=20)
            
            #### axis adjustments ####
            if yr_end-yr_start > 30: # reduces overcrowding of y-axis tick labels (less frequent ticks with longer data)
                ax2.locator_params(axis='y',nbins=(yr_end-yr_start)/2,tight=True) #set number of y ticks
            else:        
                ax2.locator_params(axis='y',nbins=(yr_end-yr_start),tight=True) #set number of y ticks
            ax2.xaxis.set_minor_locator(ticker.FixedLocator([31,59,90,120,151,181,212,243,273,304,334,365]))
            ax2.xaxis.set_major_locator(ticker.FixedLocator([15,45,74,105,135,166,196,227,258,288,319,349]))
            ax2.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
            
            ### set tick marks properties
            ax2.tick_params(which='minor', length=5,width=1.5)
            ax2.tick_params(axis='x',which='major', length=0,width=0)
            lala = ax2.yaxis.get_majorticklocs() # find the automatic tick mark locations
            ax2.xaxis.grid(b=True, which='minor', color='k', linestyle='--')
            
            # create a list of the years used in plot and add to the appropriate 
            # tick location
            yticks = []; all_years = []; new_labels = []
            start = yr_start
            while start <= yr_end:
                all_years.append(str(start))
                start += 1
            all_years.reverse()
            for each in lala:
                yticks.append(int(each))
            for each in yticks:
                if each < 0 or each == max(yticks):
                    new_labels.append('')
                else:
                    new_labels.append(all_years[each])
            ax2.set_yticklabels(new_labels)
            
            #### colorbar, axis and title properties ###
            cbar.ax.tick_params(labelsize=8)
            ax2.tick_params(axis='y', which='major', labelsize=8)
            ax2.tick_params(axis='x', which='major', labelsize=10)
            ax2.set_ylabel('Calendar Year',fontsize=10)
            ax2.set_title(basin_id + ': Observed ' + text + ' ' + str(yr_start) + '-' + str(yr_end),fontsize=12)
            fig.subplots_adjust(hspace=0.3)
            fig_out = out_dir +  basin_id + fig_name + '.png'
        else:
            fig_out = out_dir + basin_id + fig_name + '_hydrograph.png'

        ### add Lynker logo watermark in plot corner
        im = imagei.imread(wm_image)
        newax = fig.add_axes([0.75,0.82, 0.11, 0.11], anchor='NE') # create axis to place image (x,y,scalex,scaley)
        newax.imshow(im, alpha = 0.3, extent=(0,1,1,1.4)) # location of image  (left, right, bottom, top)
        newax.axis('off')            
        
        plt.savefig(fig_out, dpi=resolution, bbox_inches='tight')
        print('Figure saved to: ' + out_dir + basin_id + '_' + label + '.png')
        plt.close()
log_file.close()
print('Finished!')
print(datetime.datetime.now())