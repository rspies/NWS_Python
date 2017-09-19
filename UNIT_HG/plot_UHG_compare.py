# Created on September 30, 2014
# @author: rspies
# Python 2.7
# This script plots a comparison of the calibrated vs uncalibrated UH ordinates
# UH ordinates must be in the extracted CSV format
import os
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

os.chdir("../..")


################################# User Input #########################################
RFC = 'MBRFC_FY2017'
fx_group = '' # set to blank '' if not using fx_groups
version_compare = 'final_calb' # 'draft_calb' or 'final_calb' will be used to compare results to the pre_calb

if fx_group == '':
    maindir = os.getcwd() + os.sep + 'Extract_Hydro_Params' + os.sep + RFC[:5] + os.sep + RFC
else:
    maindir = os.getcwd() + os.sep + 'Extract_Hydro_Params' + os.sep + RFC[:5] + os.sep + RFC + os.sep + fx_group
calib_csv = open(maindir  + '\\Params_' + version_compare + '\\_' + RFC +'_UHG_Params_' + version_compare + '_slim.csv','r')
initial_csv_file = maindir + '\\Params_pre_calb\\_' + RFC +'_UHG_Params_pre_calb_slim.csv'
######################################################################################
basins = []
UHG_time = []
for each in calib_csv:
    sep = each.split(',')
    if sep[0] != 'BASIN':
        find = str(sep[0].split('_')[1])
        if find != 'BASIN' and find != '':
            if find == 'TOTAL': # MARFC has "Total" second id
                find = str(sep[0].split('_')[0])
            basins.append(find)
        else:
            for value in sep:
                if value != 'BASIN' and value != ' AREA (mi2)' and value != ' Interval (hours)' and value != '\n':
                    UHG_time.append(int(value))
calib_csv.close()

for basin in basins:
    calib_csv = open(maindir + '\\Params_' + version_compare + '\\_' + RFC +'_UHG_Params_' + version_compare + '_slim.csv','r')
    initial_csv = open(initial_csv_file,'r')    
    print 'Plotting: ' + basin + '...'
    UHG_calb_flow = []
    UHG_initial_flow = []; non_zero_cnt_init = 0; non_zero_cnt_calb = 0
    
    for each in calib_csv:
        sep = each.split(',')
        if sep[0] != 'BASIN':
            if str(sep[0].split('_')[1]) == 'TOTAL': # MARFC has "Total" second id
                find = str(sep[0].split('_')[0])
            else:
                find = str(sep[0].split('_')[1])
        else:
            find = 'header'
            ## ch5id added to extract param script 6/2016 (index change + 1 column)
            if sep[2] == 'AREA (mi2)':
                add = 1
            else:
                add = 0
        ## UHG area added to constant baseflow output (index change + 1 column)
            if sep[3] == 'Const Baseflow (cfs)':
                add += 1
        if find == basin:
            interval = int(sep[2+ add])
            count = 0
            for value in sep:
                if count > 4 and value != '\n': #ignoring first 5 values in row (basin, id, area, intveral, const baseflow)
                    UHG_calb_flow.append(value)
                    if float(value) > 0:
                        non_zero_cnt_calb += 1
                if count == 1+add:
                    area = float(value)
                count += 1
    for each in initial_csv:
        sep = each.split(',')
        if sep[0] != 'BASIN':
            if str(sep[0].split('_')[1]) == 'TOTAL': # MARFC has "Total" second id
                find = str(sep[0].split('_')[0])
            else:
                find = str(sep[0].split('_')[1])
        else:
            find = 'header'
            ## UHG area added to extract param script 6/2016 (index change + 1 column)
            if sep[2] == 'AREA (mi2)':
                add = 1
            else:
                add = 0
            ## UHG area added to constant baseflow output (index change + 1 column)
            if sep[3] == 'Const Baseflow (cfs)':
                add += 1
        if find == basin:
            interval_check = int(sep[2+add])
            count = 0
            for value in sep:
                if count > 4 and value != '\n': #ignoring first 5 values in row (basin, id, area, intveral, const baseflow)
                    UHG_initial_flow.append(value) 
                    if float(value) > 0:
                        non_zero_cnt_init += 1
                count += 1
                
    if interval != interval_check:
        print 'Error: mismatched intervals -> ' + basin
        UHG_initial_fix = UHG_initial_flow
        UHG_initial_flow =[]
        for each in UHG_initial_fix:
            UHG_initial_flow.append(float(each)/(interval_check/interval))
    print 'Interval set to: ' + str(interval) + ' hours'
    #Get max UHG time value            
    num_ordinates = max(len(UHG_calb_flow),len(UHG_initial_flow))
    x_calb = range(0,len(UHG_calb_flow)*interval,interval)
    x_initial = range(0,len(UHG_initial_flow)*interval_check,interval_check)
    fig, ax1 = plt.subplots()
    #Plot the data
    ax1.plot(x_calb, UHG_calb_flow, color='green', label='Calibrated UHG', linewidth='3', zorder=5)
    ax1.plot(x_initial, UHG_initial_flow, color='red', label='Initial UHG', ls = '--', linewidth='3', zorder=5, alpha=0.75)
    #ax1.fill_between(x,UHG_flow,facecolor='gray', alpha=0.25)    
    
    #ax1.minorticks_on()
    ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
    ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
    
    majorLocator = MultipleLocator(interval)
    ax1.xaxis.set_major_locator(majorLocator)
    
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Flow (cfs)')
    
    #Make tick labels smaller/rotate for long UHGs
    if num_ordinates >= 15:
        for label in ax1.xaxis.get_ticklabels():       
            label.set_fontsize(8)
            plt.xticks(rotation=90)
    if num_ordinates >= 24:
        for label in ax1.xaxis.get_ticklabels():       
            label.set_fontsize(6)
            plt.xticks(rotation=90)
            majorLocator = MultipleLocator(interval*2)
            ax1.xaxis.set_major_locator(majorLocator)
            
    #ax1.set_xlim([0,max_time+3])
    plt.ylim(ymin=0)
    plt.xlim(xmax=max(non_zero_cnt_init*interval_check,non_zero_cnt_calb*interval)) ## this attempts to avoid plotting all of the extra 0 ordinates on the tail
    
    #add plot legend with location and size
    ax1.legend(loc='upper right', prop={'size':10})
        
    plt.title(basin + ' UNIT-HG (Area = ' + str(int(float(area))) + '$mi^2$)' )
    
    output_folder = maindir + '\\Params_' + version_compare + '\\UHG_plot_compare\\'
    if os.path.exists(output_folder) == False:
        os.makedirs(output_folder)
    figname = maindir + '\\Params_' + version_compare + '\\UHG_plot_compare\\' + basin + '_UHG.png'
    plt.savefig(figname, dpi=100,bbox_inches='tight')
    
    plt.clf()    
    plt.close()
    #Turn interactive plot mode off (don't show figures)
    plt.ioff()    
    calib_csv.close()
    initial_csv.close()
print 'Script Completed'