#Created on January 6, 2015
#@author: rspies
# Python 2.7
# This script plots the mean pbias for the period surrounding an event of a specified magnitude.
# Numerous events are chosen at each basin based on the criteria that eliminate smaller events
# and events that may be impacted by multiple events.

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
maindir = os.getcwd()[:-7]

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
add_obs_Q_plot = 'yes' # yes/no to create a subplot of the observed data for same period
basin_ids = ['FGOG1','VDSG1','ADLG1','QUTG1','OKAG1','WORF1','PINF1','COCF1']
#basin_ids = ['ADLG1'] # run individual basin(s) instead of all basins above
sim_type = 'final' # choices: initial (prior to calib), final (final calib), working (currently in calib process)
RFC = 'SERFC'
resolution = 350 #350->(for report figs) 100->for CHPS fx help tab display (E19)
plt.ioff()  #Turn interactive plot mode off (don't show figures)
################  Define the corresponding column of data in the csv file  #################
call_SQIN = 2
call_obs = 4

for basin_id in basin_ids:
    print basin_id
    calib_read = open(maindir + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type + os.sep +'QIN_timeseries' + os.sep + basin_id + '_Simulation_TimeSeries.csv', 'r') #test!!!
    # output figure directory
    out_dir = maindir + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type+ os.sep + 'UH_analysis_plots' + os.sep
    if basin_id == 'FGOG1':
        yr_start = 1950; yr_end = 2010 # specify the first and last year to analyze
        period = 20 # number of 6 hour time steps to examine before and after event peak
        thresh= 100 # cutoff for events to examine
    if basin_id == 'VDSG1':
        yr_start = 1988; yr_end = 2010
        period = 20 
        thresh= 100
    if basin_id == 'ADLG1':
        yr_start = 1950; yr_end = 2010 #
        period = 20 
        thresh= 100
    if basin_id == 'QUTG1':
        yr_start = 1988; yr_end = 2010
        period = 20 
        thresh= 200
    if basin_id == 'OKAG1':
        yr_start = 1979; yr_end = 2010
        period = 20 
        thresh= 100
    if basin_id == 'PINF1':
        yr_start = 1950; yr_end = 2010
        period = 20 
        thresh= 300
    if basin_id == 'WORF1':
        yr_start = 1950; yr_end = 2010
        period = 20 
        thresh= 100
    if basin_id == 'COCF1':
        yr_start = 1953; yr_end = 2010
        period = 30 
        thresh= 100
    ###### tab delimitted CHPS calibrated AND Observed dishcarge text file into panda arrays ###########
    ### replaces hour time stamp with zero to create a mean daily value -> match obs data
    test = pd.read_csv(calib_read,sep=',',skiprows=2,
            usecols=[0,call_SQIN,call_obs],parse_dates=['date'],names=['date', 'SQIN', 'OBS'])
    ### assign column data to variables
    print 'Populating data arrays for calibrated dishcarge... and converting to daily values'
    
    date_calib = test['date'].tolist()                  # convert to list (indexible)
    Q_calib = test['SQIN'].tolist()
    discharge = test['OBS'].tolist()
    date_Q = []; date_Q_calib = []; count = 0                        # read the data into a dictionary (more efficient processing)
    for each_day in date_calib:
        if yr_start <= int(each_day.year) <= yr_end:
            if float(Q_calib[count]) >= 0 and float(discharge[count]) >= 0:          # ignore data less than 0 
                date_Q_calib.append(Q_calib[count])
                date_Q.append(float(discharge[count]))
        count += 1
     
    #### iterate through obs streamflow data and pull out events that meet thresh criteria ####       
    # create blank arrays for future calcs
    obs_matrix = np.empty((0,(period*2)+1),dtype=float)
    sim_matrix = np.empty((0,(period*2)+1),dtype=float)
    
    actual_index = 0; tot_events = 0
    for obs6 in date_Q:
        #### find streamflow values > than set threshold (isolate larger events)
        #### also ignore peak events at the very begining of analysis period
        if obs6 > thresh and actual_index >= period:
            #### find event peak within the window period specified above
            #### e.g. value at time1 must be > all values within +- 5days
            if obs6 >= max(date_Q[actual_index + 1:actual_index + period]) and obs6 >= max(date_Q[actual_index - period: actual_index]):
                #print obs6
                event = np.array(date_Q[actual_index-period:(actual_index+period)+1])
                event_sim = np.array(date_Q_calib[actual_index-period:(actual_index+period)+1])
                list_index = 0
                #### perform check to see if there are any dips in hydrograph indicating multiple events impacting the hydrograph
                for each in event:
                    if list_index != 0:
                        if each > thresh:
                            status = 'ok'    
                        elif max(event[list_index:]) > thresh and max(event[0:list_index]) > thresh:
                            status = 'nogo'
                            break
                    list_index += 1
                #print status
                if status == 'ok':
                    obs_matrix = np.vstack((obs_matrix,event))
                    sim_matrix = np.vstack((sim_matrix,event_sim))
                    tot_events += 1
        actual_index += 1
    print 'Number of events analyzed: ' + str(tot_events)
    
    # matrix calculations
    matrix_pbias = ((sim_matrix - obs_matrix)/obs_matrix)*100
    array_pbias = np.mean(matrix_pbias, axis=0)

    # create x array to use for lables (6hr timestep)
    x = range(period*-1,period+1,1)
    x_lables = []
    for each in x:
        x_lables.append(each*6)
        
    ############################# create plot(s) ##########################################
    #######################################################################################        
    ### create image: aspect set to auto (creates a square plot with any data)
    ### vmin->sets values less than 0 to missing
    fig, ax1 = plt.subplots()
    ax1.bar(x_lables, array_pbias, color='b')
        
    #### axis properties ###
    ax1.tick_params(axis='y', which='major', labelsize=8)
    ax1.tick_params(axis='x', which='major', labelsize=8)
    
    #### axis adjustments ####
    ax1.xaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')
    ax1.yaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')

    #### modify xaxis ticks to daily ticks
    daily_ticks = np.arange((period*-6)-24,(period*6)+48,24)
    if 0 not in daily_ticks:
        daily_ticks = np.arange((period*-6)-12,(period*6)+36,24)
    plt.xticks(daily_ticks)
    
    #### plot vertical line at 0 (time of peak)
    min_yax = (ax1.axis())[2]
    max_yax = (ax1.axis())[3]
    ax1.set_autoscale_on(False) # have to turn off autoscale otherwise xlims change
    plt.plot((0,0),(min_yax,max_yax),'r-',linewidth = '1.0')
    
    #### axis and title properties ###
    ax1.set_xlabel('Time from Peak (hrs)',fontsize=10)
    ax1.set_ylabel('Simulated Mean Percent Bias (%)',fontsize=10)
    ax1.set_title(basin_id + ': ' + str(yr_start) + '-' + str(yr_end) + ' (# of events: ' + str(tot_events) + ')',fontsize=12)

    fig_out = out_dir + basin_id + '_UH_analysis.png'
    plt.savefig(fig_out, dpi=resolution, bbox_inches='tight')
    #print 'Figure saved to: ' + out_dir  + 'correlation_plots\\' + basin_id + '_daily_correlation.png'
print 'Finished!'