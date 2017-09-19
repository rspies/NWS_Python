# Created on 8/15/2016
# @author: rspies
# Python 2.7
# This script plots a comparison of the calibrated vs uncalibrated TATUM Coefficients and layer thresholds
# Tatum layer data obtained from the extracted CSV files
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm 

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

os.chdir("../..")

################################# User Input #########################################
RFC = 'MBRFC_FY2017'
fx_group = '' # set to blank '' if not using fx_groups
version_compare1 = 'final_calb' # 'draft_calb' or 'final_calb' will be used to compare results to the pre_calb
version_compare2 = 'pre_calb' # compare results to the pre_calb

if fx_group == '':
    maindir = os.getcwd() + os.sep + 'Extract_Hydro_Params' + os.sep + RFC[:5] + os.sep + RFC
else:
    maindir = os.getcwd() + os.sep + 'Extract_Hydro_Params' + os.sep + RFC[:5] + os.sep + RFC + os.sep + fx_group

interval = 6 # 6hour values
######################################################################################
csv1 = open(maindir  + '\\Params_' + version_compare1 + '\\_' + RFC +'_TATUM_Params_' + version_compare1 + '_slim.csv','r')
### output 
output_folder = maindir + '\\Params_' + version_compare1 + '\\TATUM_plot_compare\\'
if os.path.exists(output_folder) == False:
    os.makedirs(output_folder)
layer_sum_check = open(output_folder + 'layer_coeff_check.txt','w')
layer_sum_check.write('Checking all flow layers add to 1.00 -> list below layers != 1.00\n')
        
basins = []
tat_time = []
data_dict1 = {}; thresh_dict1 = {}
for each in csv1:
    layer_dict = {}; thresh_layer = {}
    sep = each.split(',')
    if sep[0] != 'BASIN':
        basin = sep[0]
        if basin not in basins:
            basins.append(basin)
        layer_dict[sep[3]]=sep[5:-1] # create layer dict with coefficient values
        thresh_layer[sep[3]]=sep[4] # add thresh value to dict
        if basin not in data_dict1:
            data_dict1[basin]=layer_dict
            thresh_dict1[basin]=thresh_layer
        else:
            data_dict1[basin][sep[3]]=sep[5:-1]
            thresh_dict1[basin][sep[3]]=sep[4] # add thresh value to dict
    else:
        tat_time=sep[5:]
csv1.close()

if version_compare2 != '':
    csv2 = open(maindir  + '\\Params_' + version_compare2 + '\\_' + RFC +'_TATUM_Params_' + version_compare2 + '_slim.csv','r')
    data_dict2 = {}; thresh_dict2 = {}; thresh_layer2 = {}
    for each in csv2:
        layer_dict2 = {}; thresh_layer2={}
        sep = each.split(',')
        thresh_layer2[sep[3]]=sep[4] # add thresh value to dict
        if sep[0] != 'BASIN':
            basin = sep[0]
            layer_dict2[sep[3]]=sep[5:-1]
            if basin not in data_dict2:
                data_dict2[basin]=layer_dict2
                thresh_dict2[basin]=thresh_layer2
            else:
                data_dict2[basin][sep[3]]=sep[5:-1]
                thresh_dict2[basin][sep[3]]=sep[4] # add thresh value to dict
    csv2.close()

for basin in basins:
    print 'Plotting ' + basin
    fig, ax1 = plt.subplots()
    colors=iter(cm.winter(np.linspace(0,1,len(data_dict1[basin])+1)))
    #Plot the data
    num_ords = []
    for layer in sorted(data_dict1[basin]):
        ax1.plot(tat_time[:len(data_dict1[basin][layer])], data_dict1[basin][layer], color=next(colors), label=version_compare1+' ' + layer + ': ' +thresh_dict1[basin][layer], linewidth='5', zorder=5)
        num_ords.append(len(data_dict1[basin][layer]))
        #ax1.plot(x_initial, UHG_initial_flow, color='red', label='Initial UHG', ls = '--', linewidth='3', zorder=5, alpha=0.75)
        #ax1.fill_between(x,UHG_flow,facecolor='gray', alpha=0.25)
        sum_coef = round(sum(map(float,data_dict1[basin][layer])),2) # convert list strings to float, sum, and round to 2 decimals
        if sum_coef != 1.00:
            print 'WARNING!! -> ' + basin + ' ' + layer + ' sum = ' + str(sum_coef)
            layer_sum_check.write(version_compare1 + ' ' + basin + ' ' + layer + ' sum = ' + str(sum_coef) + '\n')
    if version_compare2 != '':
        if basin in data_dict2:
            colors=iter(cm.autumn(np.linspace(0,1,len(data_dict2[basin])+1)))
            for layer in sorted(data_dict2[basin]):
                ax1.plot(tat_time[:len(data_dict2[basin][layer])], data_dict2[basin][layer], '--', dashes=(5,2), color=next(colors), label=version_compare2+' ' + layer + ': ' +thresh_dict2[basin][layer], linewidth='3', zorder=5)
                num_ords.append(len(data_dict2[basin][layer]))
                sum_coef = round(sum(map(float,data_dict2[basin][layer])),2) # convert list strings to float, sum, and round to 2 decimals
                if sum_coef != 1.00:
                    layer_sum_check.write(version_compare2 + ' ' + basin + ' ' + layer + ' sum = ' + str(sum_coef) + '\n')
                    #print 'WARNING!! -> ' + version_compare2 + ' ' + basin + ' ' + layer + ' sum = ' + str(sum_coef)
    
    #ax1.minorticks_on()
    ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
    ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
    
    majorLocator = MultipleLocator(interval)
    ax1.xaxis.set_major_locator(majorLocator)
    
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    
    ax1.set_xlabel('Time (hrs)')
    ax1.set_ylabel('Flow Coefficient')
    
    #Make tick labels smaller/rotate for long UHGs
    num_ordinates = max(num_ords)
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
    plt.ylim(ymax=1)
    
    #add plot legend with location and size
    ax1.legend(bbox_to_anchor=(1.6, 1.05), prop={'size':10})
        
    plt.title(basin + ' TATUM Coefficients')
    
    figname = maindir + '\\Params_' + version_compare1 + '\\TATUM_plot_compare\\' + basin + '_TATUM.png'
    plt.savefig(figname, dpi=100,bbox_inches='tight')
    
    plt.clf()    
    plt.close()
    #Turn interactive plot mode off (don't show figures)
    plt.ioff()  
layer_sum_check.close()
print 'Script Completed'
