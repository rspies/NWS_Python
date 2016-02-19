#Created on July 7, 2014
#@author: rspies
# Python 2.7
# This script plots a correlation plot of observed vs. simulated daily streamflow. A polynomial
# trend line is fitted to the data and the equation of the line is displayed on the plot.
# A csv file is output calculating the % bias within a range of defined bins
# Units should be in cms (required for lookup table)

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
basin_ids = ['FRRT2'] # run individual basin(s) instead of all basins in dir -> else leave empty []
sim_type = 'final' # choices: initial (prior to calib), final (final calib), working (currently in calib process)
RFC = 'WGRFC'
weights = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.05]
resolution = 350 #350->(for report figs) 100->for CHPS fx help tab display (E19)
################  Define the corresponding column of data in the csv file  #################
call_SQIN = 2
call_obs = 4
yr_start = 1950; yr_end = 2014 #

########### find all basin SQIN vs QIN .csv files ############
if len(basin_ids) == 0:
    basin_ids = []
    all_files = os.listdir(maindir +RFC+ os.sep + 'Calibration_TimeSeries'+ os.sep + sim_type + os.sep + 'QIN_timeseries' + os.sep)
    for each in all_files:
        if each.endswith(".csv"):
            basin_ids.append(each[:6].rstrip('_'))
        
for basin_id in basin_ids:
    print basin_id
    calib_read = open(maindir + RFC + os.sep + 'Calibration_TimeSeries' + os.sep +sim_type + os.sep + 'QIN_timeseries' + os.sep + basin_id + '_Simulation_TimeSeries.csv', 'r') #test!!!
    # output figure directory
    out_dir = maindir + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type+ os.sep
    
    ###### tab delimitted CHPS calibrated AND Observed dishcarge text file into panda arrays ###########
    ### replaces hour time stamp with zero to create a mean daily value -> match obs data
    test = pd.read_csv(calib_read,sep=',',skiprows=2,
            usecols=[0,call_SQIN,call_obs],parse_dates=['date'],names=['date', 'SQIN', 'OBS'])
    ### assign column data to variables
    print 'Populating data arrays for calibrated dishcarge... and converting to daily values'
    
    date_calib = test['date'].tolist()                  # convert to list (indexible)
    Q_calib = test['SQIN'].tolist()
    discharge = test['OBS'].tolist()
    date_Q = []; count = 0                              # read the data into a dictionary (more efficient processing)
    date_Q_calib = []; new_date = []; count = 0                        # read the data into a dictionary (more efficient processing)
    for each_day in date_calib:
        if yr_start <= int(each_day.year) <= yr_end:
            if float(Q_calib[count]) >= 0 and float(discharge[count]) >= 0:          # ignore data less than 0 
                date_Q_calib.append(Q_calib[count])
                date_Q.append(float(discharge[count]))
                new_date.append(each_day)
        count += 1
    
    ####### Find the time step of obs/sim data comparison #########
    step = str(int(abs((new_date[0] - new_date[1]).total_seconds())/3600))
    if step != '6' and step != '24' and step != '1':
        step = str(int(abs((new_date[100] - new_date[101]).total_seconds())/3600))
    if step != '6' and step != '24' and step != '1':
        step = str(int(abs((new_date[200] - new_date[201]).total_seconds())/3600))
    print 'simulation interval = ' + step
    
    ####### Calculate % bias bin values #######
    print 'Calculating bin bias...'
    out_csv = open(out_dir + os.sep + 'bias_bins' + os.sep + basin_id + '_bias_bins_'+step+'hr.csv','w')
    out_csv.write(basin_id + '\n')
    out_csv.write('bin range (cms),' + '# of values in bin,' + 'mean bin (cms),' + 'mean bin (cms),'+ 'mean obs (cms),' + 'mean sim (cms),' + '% bias (%),')
    for weight in weights:
        out_csv.write('CHPS lookup table format (weight = ' + str(weight) +'),')
    out_csv.write('\n')
    # define bins below
    all_bins = (('0.0,0.01',[]),('0.01,0.1',[]),('0.1,0.2',[]),('0.2,0.3',[]),('0.3,0.5',[]),('0.5,1.0',[]),('1.0,2.0',[]),('2.0,4.0',[]),('4.0,6.0',[]),('6.0,8.0',[]),('8.0,10.0',[]),
            ('10.0,15.0',[]),('15.0,20.0',[]),('20.0,30.0',[]),('30.0,40.0',[]),('40.0,50.0',[]),('50.0,75.0',[]),
            ('75.0,100.0',[]),('100.0,150.0',[]),('150.0,200.0',[]),('200.0,300.0',[]),('300.0,500.0',[]),
            ('500.0,800.0',[]),('800.0,1200.0',[]),('1200.0,1600.0',[]),('1600.0,2000.0',[]),('2000.0,2500.0',[]),('2500.0,5000.0',[]))
    all_bins = collections.OrderedDict(all_bins) # keeps dictionary in the specified order
    all_bins_calb = copy.deepcopy(all_bins) # create copy of first dictionary for simulated data
    all_count = 0
    for obs_value in date_Q:
        for bins in all_bins:
            min_bin = float(bins.split(',')[0])
            max_bin = float(bins.split(',')[1])
            if obs_value > min_bin and obs_value <= max_bin:
                outlier_catch = (obs_value-date_Q_calib[all_count])/obs_value
                #!!!!!! below: catch outlier sim differences -> +- 500% diff limits !!!!!#
                if outlier_catch <= 10.0 and outlier_catch >= -10.0: 
                    all_bins[bins].append(obs_value)
                    all_bins_calb[bins].append(date_Q_calib[all_count])
                    break
        all_count += 1
    bin_prev = 0.0
    for bins in all_bins:
        min_bin = float(bins.split(',')[0])
        max_bin = float(bins.split(',')[1])
        mean_bin = str(round(((min_bin + max_bin)/2),2))
        mean_bin_cms = str(round(float(mean_bin),2))
        mean_bin_obs = str(round(np.mean(all_bins[bins]) ,2))
        mean_bin_sim = str(round(np.mean(all_bins_calb[bins]),2))
        mean_bin_bias = ((np.mean(all_bins_calb[bins])/np.mean(all_bins[bins]))-1)
        mean_bin_pbias = mean_bin_bias*100
        
        # calculate the desired lookup table transformations
        if float(mean_bin_sim) > bin_prev or min_bin == 0.0: # data must be asscending -> ignore out of order bins
            if min_bin == 0.0:
                mean_bin_obs = '0.01'; mean_bin_sim = '0.01'; mean_bin_bias = 0.0
            out_csv.write(str(min_bin) + ' - ' + str(max_bin) + ',' + str(len(all_bins[bins])) + ',' + mean_bin + ',' + mean_bin_cms + ','+ mean_bin_obs + ',' + mean_bin_sim + ',' + str(mean_bin_pbias)+ ',')
            for weight in weights:
                # isolate bins with less than 10 values and bins with negative bias (can't add water)
                if mean_bin_bias <= 0.0 or len(all_bins[bins]) < 10:
                    if mean_bin_obs == '0.01':
                        adj_bin_cms = '0.01'; mean_bin_sim_weight = '0.01' #leave first bin = 0.01 to 0.01
                    elif float(mean_bin_obs) <= 1.0 and mean_bin_bias >= 0.0:
                        adj_bin_cms = str(round(float(mean_bin_obs) * weight,2))
                        mean_bin_sim_weight = str(round(float(mean_bin_sim) * weight,2))
                    else: # negative bias bins are set to in sim = out sim
                        adj_bin_cms = str(round(float(mean_bin_sim) * weight,2))
                        mean_bin_sim_weight = str(round(float(mean_bin_sim) * weight,2))
                else:
                    adj_bin_cms = str(round(float(mean_bin_obs) * weight,2))
                    mean_bin_sim_weight = str(round(float(mean_bin_sim) * weight,2))
                chps_fmt = '<lookupTableRow input="' + str(mean_bin_sim_weight) + '" output="' + str(adj_bin_cms) + '"></lookupTableRow>'
                out_csv.write(chps_fmt + ',')
            out_csv.write('\n')
            bin_prev = float(mean_bin_sim)
        else:
            print 'Bin out of order: ' + str(min_bin) + ' - ' + str(max_bin) + ',' + str(len(all_bins[bins])) + ',' + mean_bin + ',' + mean_bin_cms + ','+ mean_bin_obs + ',' + mean_bin_sim + ',' + str(mean_bin_pbias)

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
    if step != '6' and step != '24' and step != '1':
        print 'Did not find time step...'
    ax1.set_ylabel('Simulated ' + step + '-hour Discharge (cms)',fontsize=10)
    ax1.set_xlabel('Observed ' + step + '-hour Discharge (cms)',fontsize=10)
    ax1.set_title(basin_id + ': ' + str(min(new_date).year) + '-' + str(max(new_date).year),fontsize=12)

    fig_out = out_dir + os.sep + 'correlation_plots' + os.sep + basin_id + '_' + step + 'hour_correlation.png'
    plt.savefig(fig_out, dpi=resolution, bbox_inches='tight')
    #print 'Figure saved to: ' + out_dir  + 'correlation_plots\\' + basin_id + '_daily_correlation.png'
print 'Finished!'