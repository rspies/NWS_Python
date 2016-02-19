#Created on July 7, 2014
#@author: rspies
# Python 2.7
# This script plots a correlation plot of observed vs. simulated daily streamflow. A polynomial
# trend line is fitted to the data and the equation of the line is displayed on the plot.
# A csv file is output calculating the % bias within a range of defined bins

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import collections # needed for ordered Dictionary
import copy # needed for deepcopy of dictionary
maindir = os.getcwd()[:-6]

############################### User input ###################################
##############################################################################
##### IMPORTANT: Make sure to call the correct CHPS .csv output columns ######
#####    and specify the calibration period in next section 
add_obs_Q_plot = 'yes' # yes/no to create a subplot of the observed data for same period
basin_ids = ['TIDT2'] # run individual basin(s) instead of all basins in dir -> else leave empty []
sim_type = 'working' # choices: initial (prior to calib), final (final calib), working (currently in calib process)
RFC = 'WGRFC'
weights = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
resolution = 350 #350->(for report figs) 100->for CHPS fx help tab display (E19)
################  Define the corresponding column of data in the csv file  #################
call_QME = 2
call_obs = 3
yr_start = 1950; yr_end = 2010 #

########### find all basin QME vs SQME .csv files ############
if len(basin_ids) == 0:
    basin_ids = []
    all_files = os.listdir(maindir +RFC+ os.sep + 'Calibration_TimeSeries'+ os.sep + sim_type + os.sep)
    for each in all_files:
        if each.endswith(".csv"):
            basin_ids.append(each[:6].rstrip('_'))
        
for basin_id in basin_ids:
    print basin_id
    calib_read = open(maindir + RFC + os.sep + 'Calibration_TimeSeries' + os.sep +sim_type + os.sep + basin_id + '_Simulation_TimeSeries.csv', 'r') #test!!!
    # output figure directory
    out_dir = maindir + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type+ os.sep
    
    ###### tab delimitted CHPS calibrated AND Observed dishcarge text file into panda arrays ###########
    ### replaces hour time stamp with zero to create a mean daily value -> match obs data
    test = pd.read_csv(calib_read,sep=',',skiprows=2,
            usecols=[0,call_QME,call_obs],parse_dates=['date'],names=['date', 'QME', 'OBS'])
    ### assign column data to variables
    print 'Populating data arrays for calibrated dishcarge... and converting to daily values'
    
    date_calib = test['date'].tolist()                  # convert to list (indexible)
    Q_calib = test['QME'].tolist()
    discharge = test['OBS'].tolist()
    date_Q = []; count = 0                              # read the data into a dictionary (more efficient processing)
    date_Q_calib = []; count = 0                        # read the data into a dictionary (more efficient processing)
    for each_day in date_calib:
        if yr_start <= int(each_day.year) <= yr_end:
            if float(Q_calib[count]) >= 0 and float(discharge[count]) >= 0:          # ignore data less than 0 
                date_Q_calib.append(Q_calib[count])
                date_Q.append(float(discharge[count]))
        count += 1

    ####### Calculate % bias bin values #######
    print 'Calculating bin bias...'
    out_csv = open(out_dir + os.sep + 'bias_bins' + os.sep + basin_id + '_bias_bins.csv','w')
    out_csv.write(basin_id + '\n')
    out_csv.write('bin range (cms),' + '# of values in bin,' + 'mean bin (cms),' + 'mean bin (cfs),'+ 'mean obs (cfs),' + 'mean sim (cfs),' + '% bias (%),')
    for weight in weights:
        out_csv.write('CHPS lookup table format (weight = ' + str(weight) +'),')
    out_csv.write('\n')
    # define bins below
    all_bins = (('0.0,0.01',[]),('0.01,0.1',[]),('0.1,0.3',[]),('0.3,0.5',[]),('0.5,1.0',[]),('1.0,2.0',[]),('2.0,4.0',[]),('4.0,6.0',[]),('6.0,8.0',[]),('8.0,10.0',[]),
            ('10.0,15.0',[]),('15.0,20.0',[]),('20.0,30.0',[]),('30.0,40.0',[]),('40.0,50.0',[]),('50.0,75.0',[]),
            ('75.0,100.0',[]),('100.0,150.0',[]),('150.0,200.0',[]),('200.0,300.0',[]),('300.0,500.0',[]),
            ('500.0,800.0',[]),('800.0,1200.0',[]),('1200.0,1600.0',[]),('1600.0,2000.0',[]))
    all_bins = collections.OrderedDict(all_bins) # keeps dictionary in the specified order
    all_bins_calb = copy.deepcopy(all_bins) # create copy of first dictionary for simulated data
    all_count = 0
    for obs_value in date_Q:
        for bins in all_bins:
            min_bin = float(bins.split(',')[0])
            max_bin = float(bins.split(',')[1])
            if obs_value > min_bin and obs_value <= max_bin:
                all_bins[bins].append(obs_value)
                all_bins_calb[bins].append(date_Q_calib[all_count])
                break
        all_count += 1
    
    for bins in all_bins:
        min_bin = float(bins.split(',')[0])
        max_bin = float(bins.split(',')[1])
        mean_bin = str(round(((min_bin + max_bin)/2),2))
        mean_bin_cfs = str(round(float(mean_bin)* 35.3147,2)) # convert to cfs
        mean_bin_obs = str(round(np.mean(all_bins[bins]) * 35.3147,2))
        mean_bin_sim = str(round(np.mean(all_bins_calb[bins])* 35.3147,2))
        mean_bin_bias = ((np.mean(all_bins_calb[bins])/np.mean(all_bins[bins]))-1)
        mean_bin_pbias = mean_bin_bias*100
        if min_bin == 0.0:
            mean_bin_obs = '0.01'; mean_bin_sim = '0.01'; mean_bin_bias = 0.0
        out_csv.write(str(min_bin) + ' - ' + str(max_bin) + ',' + str(len(all_bins[bins])) + ',' + mean_bin + ',' + mean_bin_cfs + ','+ mean_bin_obs + ',' + mean_bin_sim + ',' + str(mean_bin_pbias)+ ',')
        for weight in weights:
            if mean_bin_bias <= 0.0:
                adj_bin_cfs = mean_bin_sim
                chps_fmt = '<lookupTableRow input="' + str(mean_bin_sim) + '" output="' + str(adj_bin_cfs) + '"></lookupTableRow>'
                out_csv.write(chps_fmt + ',')
            else:
                adj_bin_cfs = str(round(float(mean_bin_obs) * weight,2))
                mean_bin_sim_weight = str(round(float(mean_bin_sim) * weight,2))
                chps_fmt = '<lookupTableRow input="' + str(mean_bin_sim_weight) + '" output="' + str(adj_bin_cfs) + '"></lookupTableRow>'
                out_csv.write(chps_fmt + ',')
        out_csv.write('\n')
    out_csv.close()
    ############################# create plot(s) ##########################################
    #######################################################################################        
    ### create image: aspect set to auto (creates a square plot with any data)
    ### vmin->sets values less than 0 to missing
    fig, ax1 = plt.subplots()
    ax1.plot(date_Q, date_Q_calib, linestyle='None', marker='+',ms=5)
        
    #### axis properties ###
    ax1.tick_params(axis='y', which='major', labelsize=8)
    ax1.tick_params(axis='x', which='major', labelsize=8)
    
    #### axis adjustments ####
    ax1.xaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')
    ax1.yaxis.grid(b=True, which='major', color='0.6', linestyle='--',linewidth='0.5')
    max_ax = max(ax1.axis())
    ax1.axis([0,max_ax,0,max_ax])
    fig.gca().set_aspect('equal', adjustable='box')
    
    #### add one to one series to plot ####
    best_line = range(0,int(max_ax)+50,10)
    ax1.plot(best_line, best_line, linestyle='-', color='k', linewidth='1')
    
    #### fit polynomial curve ####
    z = np.polyfit(date_Q, date_Q_calib, 2)
    f = np.poly1d(z)
    # calculate new x's and y's
    x_new = np.linspace(0, int(max_ax), 1000)
    y_new = f(x_new)
    ax1.plot(x_new,y_new,color='red', lw = 1.5,)
    
    #### text box with trend line equation ####
    eq_components = 'y='
    comp_num = len(f)
    counter = 0
    for each in f:
        if counter < comp_num:
            eq_components = eq_components + (str(round(each,6))) + r'$x^{}$'.format(comp_num - counter) + ' + '
        else:
            eq_components= eq_components + (str(round(each,6)))
        counter += 1
    ax1.text(0.95, 0.06, eq_components,
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax1.transAxes,
        color='red', fontsize=8)
    
    ### set tick marks properties
    #ax1.tick_params(which='minor', length=5,width=1.5)
    #ax1.tick_params(axis='x',which='major', length=0,width=0)
   
    #### axis and title properties ###
    ax1.set_ylabel('Simulated Daily Discharge (cms)',fontsize=10)
    ax1.set_xlabel('Observed Daily Discharge (cms)',fontsize=10)
    ax1.set_title(basin_id + ': ' + str(yr_start) + '-' + str(yr_end),fontsize=12)

    fig_out = out_dir + os.sep + 'correlation_plots' + os.sep + basin_id + '_daily_correlation.png'
    plt.savefig(fig_out, dpi=resolution, bbox_inches='tight')
    #print 'Figure saved to: ' + out_dir  + 'correlation_plots\\' + basin_id + '_daily_correlation.png'
print 'Finished!'