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

os.chdir("..")
maindir = os.getcwd() + os.sep + 'Extract_Hydro_Params'
version_compare = 'draft_calb' # 'draft_calb' or 'final_calb' will be used to compare results to the pre_calb
################################# User Input #########################################
RFC = 'NERFC_FY2016'
calib_csv = open(maindir +os.sep + RFC[:5] + os.sep + RFC + '\\Params_' + version_compare + '\\_' + RFC +'_SNOW17_ADC_' + version_compare + '_slim.csv','r')
initial_csv_file = maindir +os.sep + RFC[:5] + os.sep + RFC + '\\Params_pre_calb\\_' + RFC +'_SNOW17_ADC_pre_calb_slim.csv'
######################################################################################
basins = []
SWE = []
for each in calib_csv:
    sep = each.split(',')
    if sep[0] != 'BASIN':
        find = str(sep[0])
        if find != 'BASIN' and find != '':
            basins.append(find)
    else:
        for value in sep:
            if value != 'BASIN'and value != '\n':
                SWE.append(float(value))
calib_csv.close()

for basin in basins:
    calib_csv = open(maindir +os.sep + RFC[:5] + os.sep + RFC + '\\Params_' + version_compare + '\\_' + RFC +'_SNOW17_ADC_' + version_compare + '_slim.csv','r')
    initial_csv = open(initial_csv_file,'r')    
    print 'Plotting: ' + basin + '...'
    SCA_calb = []
    SCA_initial = []
    
    for each in calib_csv:
        sep = each.split(',')
        if sep[0] != 'BASIN':
            find = str(sep[0])
        else:
            find = 'header'
        if find == basin:
            count = 0
            for value in sep:
                if count > 0 and value != '\n':
                    SCA_calb.append(value)
                if count == 1:
                    area = float(value)
                count += 1
    for each in initial_csv:
        sep = each.split(',')
        if sep[0] != 'BASIN':
            find = str(sep[0])
        else:
            find = 'header'
        if find == basin:
            count = 0
            for value in sep:
                if count > 0 and value != '\n':
                    SCA_initial.append(value) 
                count += 1
                

    fig, ax1 = plt.subplots()
    #Plot the data
    ax1.plot(SCA_calb, SWE, color='green', label='Calibrated', linewidth='3', zorder=5)
    ax1.plot(SCA_initial, SWE, color='red', label='Initial', ls = '--', linewidth='3', zorder=5, alpha=0.75)
    #ax1.fill_between(x,UHG_flow,facecolor='gray', alpha=0.25)    
    
    #ax1.minorticks_on()
    ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
    ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
    
    majorLocator = MultipleLocator(0.1)
    ax1.xaxis.set_major_locator(majorLocator)
    
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    
    ax1.set_xlabel('Areal Extent of Snow Cover (decimal)')
    ax1.set_ylabel('WE/A(i)')
    
    #Make tick labels smaller/rotate for long UHGs
#    if num_ordinates >= 15:
#        for label in ax1.xaxis.get_ticklabels():       
#            label.set_fontsize(8)
#            plt.xticks(rotation=90)
#    if num_ordinates >= 24:
#        for label in ax1.xaxis.get_ticklabels():       
#            label.set_fontsize(6)
#            plt.xticks(rotation=90)
#            majorLocator = MultipleLocator(interval*2)
#            ax1.xaxis.set_major_locator(majorLocator)
            
    #ax1.set_xlim([0,max_time+3])
    plt.ylim(ymin=0)
    
    #add plot legend with location and size
    ax1.legend(loc='upper left', prop={'size':10})
        
    plt.title(basin + ' ADC Comparison - ' + basin )
        
    figname = maindir +os.sep + RFC[:5] + os.sep + RFC + '\\Params_' + version_compare + '\\ADC_plot_compare\\' + basin + '_ADC.png'
        
    plt.savefig(figname, dpi=100,bbox_inches='tight')
    
    plt.clf()    
    plt.close()
    #Turn interactive plot mode off (don't show figures)
    plt.ioff()    
    calib_csv.close()
    initial_csv.close()
print 'Script Completed'