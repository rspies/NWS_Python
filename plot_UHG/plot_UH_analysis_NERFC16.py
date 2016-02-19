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
import numpy.ma as ma
os.chdir("../..")
maindir = os.getcwd() + os.sep + 'Calibration_NWS' 

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
basin_ids = [] # run individual basin(s) -> otherwise leave empty []
sim_type = 'initial' # choices: "initial", "final", "working", "draft"
RFC = 'NERFC_FY2016'
variable = 'QIN_SQIN'#'QME_SQME' 
resolution = 350 #350->(for report figs) 100->for CHPS fx help tab display (E19)
plt.ioff()  #Turn interactive plot mode off (don't show figures)
yr_start  = 1978; yr_end = 2013 # specify the first and last year to analyze
csv_loc = maindir + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type + os.sep + variable + os.sep
out_dir = maindir + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type+ os.sep + 'UH_analysis_plots' +  os.sep + variable + os.sep 
out_list = maindir + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type + os.sep + 'UH_analysis_plots' + os.sep + variable + os.sep + 'uhg_event_analysis.txt'
################  Define the corresponding column of data in the csv file  #################
write_date_list = open(out_list,'w') 
ignore_basins = []
if basin_ids == []:
    csv_files = os.listdir(csv_loc)
    for csv_file in csv_files:
        basin_name = csv_file[:6].rstrip('_')
        if basin_name not in ignore_basins:
            basin_ids.append(basin_name)
#basin_ids = ['ADDM8'] # <- use this to run individual basin
if variable == 'QIN_SQIN':
    step = 6 # data time step
    period = 12
if variable == 'QME_SQME':
    step = 24 # data time step
    period = 3
############################################################            
high_flows = []
midhigh_flows = ['GEOV1']
mid_flows = ['JVLV1']
midlow_flows = ['CFDM1']
low_flows = ['NWFM1']
###########################################################
for basin_id in basin_ids:
    print basin_id
    write_date_list.write(basin_id + '\t')
    calib_read = open(csv_loc + basin_id + '_' + variable + '.csv', 'r') #test!!!
    # output figure directory
    if basin_id in high_flows:
        #step = 6    # time step (1 or 6 hour)
        #period = 20 # number of time steps to examine before and after event peak
        thresh= 1500 # cutoff for events to examine
    elif basin_id in midhigh_flows:
        thresh = 400
    elif basin_id in mid_flows:
        thresh = 250
    elif basin_id in midlow_flows:
        thresh = 110    
    elif basin_id in low_flows : # low flows
        thresh= 60
    else: 
        thresh= 50

    ###### tab delimitted CHPS calibrated AND Observed dishcarge text file into panda arrays ###########
    ### replaces hour time stamp with zero to create a mean daily value -> match obs data
    test = pd.read_csv(calib_read,sep=',',skiprows=2,
            usecols=[0,1,2],parse_dates=['date'],names=['date', 'OBS', 'SQIN'])
    ### assign column data to variables
    print 'Populating data arrays for calibrated dishcarge... and converting to daily values'
    
    date_calib = test['date'].tolist()                  # convert to list (indexible)
    Q_calib = test['SQIN'].tolist()
    discharge = test['OBS'].tolist()
    date_Q = []; date_Q_calib = []; new_date = []; count = 0                        # read the data into a dictionary (more efficient processing)
    for each_day in date_calib:
        if yr_start <= int(each_day.year) <= yr_end:
            if float(Q_calib[count]) >= 0:# or float(discharge[count]) >= 0:          # ignore periods with sim and obs missing data (less than 0) 
                date_Q_calib.append(Q_calib[count])
                date_Q.append(float(discharge[count]))
                new_date.append(each_day)
        count += 1
     
    #### iterate through obs streamflow data and pull out events that meet thresh criteria ####       
    # create blank arrays for future calcs
    obs_matrix = np.empty((0,(period*2+1)),dtype=float)
    sim_matrix = np.empty((0,(period*2+1)),dtype=float)
    
    actual_index = 0; tot_events = 0
    for obs in date_Q:
        #### find streamflow values > than set threshold (isolate larger events)
        #### also ignore peak events at the very begining of analysis period
        if obs > thresh and actual_index >= period:
            #### find event peak within the window period specified above
            #### e.g. value at time1 must be > all values within +- 5 time steps
            if obs >= max(date_Q[actual_index + 1:actual_index + period]) and obs > max(date_Q[actual_index - period: actual_index]):
                #print obs
                event = np.array(date_Q[actual_index-period:(actual_index+period+1)])
                #event = ma.masked_less(event,6)
                event_sim = np.array(date_Q_calib[actual_index-period:(actual_index+period+1)])
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
                    obs_matrix = ma.masked_less(obs_matrix,1)
                    sim_matrix = np.vstack((sim_matrix,event_sim))
                    tot_events += 1
                    print new_date[actual_index]
                    write_date_list.write(str(new_date[actual_index]) + ', ')
        actual_index += 1
    print 'Number of events analyzed: ' + str(tot_events)
    write_date_list.write('\n')
    
    # matrix calculations
    matrix_pbias = ((sim_matrix - obs_matrix)/obs_matrix)*100
    array_pbias = np.mean(matrix_pbias, axis=0)
    
    # column mean for obs and sim
    obs_mean = []; sim_mean = []
    for col in obs_matrix.T:
        avg_obs = col.mean()
        obs_mean.append(avg_obs)
    for col in sim_matrix.T:
        avg_sim = col.mean()
        sim_mean.append(avg_sim)

    # create x array to use for labels (6hr or 1hr timestep)
    x = range(period*-1,period+1,1)
    x_labels = []
    for each in x:
        x_labels.append(each*step)
        
    ############################# create plot(s) ##########################################
    #######################################################################################        
    ### create image: aspect set to auto (creates a square plot with any data)
    ### vmin->sets values less than 0 to missing
    #fig, ax1 = plt.subplots()
    fig = plt.figure()
    fig.subplots_adjust(hspace=.2)
    ax1 = fig.add_subplot(211)
    if step == 24:
        ax1.bar(x_labels, array_pbias, color='b', width=8)#,align='center')
    else:
        ax1.bar(x_labels, array_pbias, color='b', width=4)#,align='center')
        
    #### axis properties ###
    ax1.tick_params(axis='y', which='major', labelsize=8)
    ax1.tick_params(axis='x', which='major', labelsize=7)
    
    #### axis adjustments ####
    ax1.xaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')
    ax1.yaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')

    #### modify xaxis ticks to daily ticks
    if step == 6 or step == 24:
        daily_ticks = np.arange((period*-step)-24,(period*step)+48,24)
        if 0 not in daily_ticks:
            daily_ticks = np.arange((period*-step)-12,(period*step)+36,24)
    if step == 1:
        daily_ticks = np.arange((period*-step),(period*step)+6,6)
    plt.xticks(daily_ticks)
    
    #### plot vertical line at 0 (time of peak)
    min_yax = (ax1.axis())[2]
    max_yax = (ax1.axis())[3]
    ax1.set_autoscale_on(False) # have to turn off autoscale otherwise xlims change
    plt.plot((0,0),(min_yax,max_yax),'r-',linewidth = '1.0')
    plt.plot((min(daily_ticks),max(daily_ticks)),(0,0),'k-',linewidth = '1.25')
    
    #### axis and title properties ###
    #ax1.set_xlabel('Time from Peak (hrs)',fontsize=8)
    ax1.set_ylabel('Simulated Mean Percent Bias (%)',fontsize=7)
    ax1.set_title(basin_id + ': ' + str(yr_start) + '-' + str(yr_end) + ' (analyzed ' + str(tot_events) + ' events >= ' + str(thresh) + ' CMS)',fontsize=11)
    ##################################################################
    ### obs/sim mean
    ax2 = fig.add_subplot(212)
    # plot spaghetti of all events
    row_count = 0
    for row in sim_matrix:
        row_count += 1
        if row_count == 1:
            ax2.plot(x_labels,row,lw='0.1',color='blue', label='simulated events')
        else:
            ax2.plot(x_labels,row,lw='0.1',color='blue')
    ax2.plot(x_labels,obs_mean,'orange',lw=2,label='observed mean')
    ax2.plot(x_labels,sim_mean,'blue',lw=2,label='simulated mean')
    
    #### axis adjustments ####
    ax2.xaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')
    ax2.yaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')
    #### axis properties ###
    ax2.tick_params(axis='y', which='major', labelsize=8)
    ax2.tick_params(axis='x', which='major', labelsize=7)
    
    #### modify xaxis ticks to daily ticks
    plt.xticks(daily_ticks)
    #### plot vertical line at 0 (time of peak)
    min_yax = (ax2.axis())[2]
    max_yax = (ax2.axis())[3]
    ax2.set_autoscale_on(False) # have to turn off autoscale otherwise xlims change
    plt.plot((0,0),(min_yax,max_yax),'r-',linewidth = '1.0')
    
    #### axis and title properties ###
    ax2.set_xlabel('Time from Peak (hrs)',fontsize=8)
    ax2.set_ylabel('Streamflow (CMSD)',fontsize=7)
    ax2.legend(loc="upper left",shadow=True,fontsize=6)

    fig_out = out_dir + basin_id + '_UH_analysis_highres.png'
    plt.savefig(fig_out, dpi=resolution, bbox_inches='tight')
    plt.clf()
    #print 'Figure saved to: ' + out_dir  + 'correlation_plots\\' + basin_id + '_daily_correlation.png'
write_date_list.close()
print 'Finished!'