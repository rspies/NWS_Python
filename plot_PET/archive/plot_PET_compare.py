# Created on 12/15/2014
# @author: rspies
# This script plots a comparison of several ET-demand mid-month values at each basin
# Each time series source is located in an individual .csv file
import os
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

################################# User Input #########################################
maindir = os.getcwd()
RFC = 'SERFC'
# define the location of the PE .csv files
mape_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_monthly_climo.csv','r')
calb_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_final_calb.csv','r')
pen_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_fao_penman_calc.csv','r')
ohd_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_OHD_grid_climo.csv','r')
sa_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_SA_orig_pe.csv','r')
######################################################################################
basins = []

for each in mape_csv:
    sep = each.split(',')
    find = str(sep[0])
    if find != 'BASIN' and find != 'Basin' and len(find) < 7:
        basins.append(find)
mape_csv.close()
    
for basin in basins:
    print 'Plotting: ' + basin + '...'
    # redefine open file locations for each loop iteration
    mape_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_monthly_climo.csv','r')
    calb_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_final_calb.csv','r')
    pen_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_fao_penman_calc.csv','r')
    ohd_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_OHD_grid_climo.csv','r')
    sa_csv = open(os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\' + RFC + '_SA_orig_pe.csv','r')
    months = [1,2,3,4,5,6,7,8,9,10,11,12]    
    month_names = ['J','F','M','A','M','J','J','A','S','O','N','D']
    fig, ax1 = plt.subplots()
    mape = []; calb = []; pen = []; ohd = []; sa = []
    
    for each in mape_csv:
        sep = each.split(',')
        find = str(sep[0])
        if find == basin:
            for value in sep:
                if value != '\n' and value != basin:
                    mape.append(float(value))
    mape_csv.close()
    for each in calb_csv:
        sep = each.split(',')
        find = str(sep[0])
        if find == basin:
            for value in sep:
                if value != '\n' and value != basin:
                    calb.append(float(value))
    calb_csv.close()
    for each in pen_csv:
        sep = each.split(',')
        find = str(sep[0])
        if find == basin:
            for value in sep:
                if value != '\n' and value != basin:
                    pen.append(float(value))
    pen_csv.close()
    for each in ohd_csv:
        sep = each.split(',')
        find = str(sep[0])
        if find == basin:
            for value in sep:
                if value != '\n' and value != basin:
                    ohd.append(float(value))
    ohd_csv.close()
    for each in sa_csv:
        sep = each.split(',')
        find = str(sep[0])
        if find == basin:
            for value in sep:
                if value != '\n' and value != basin:
                    sa.append(float(value))
    sa_csv.close()

    #Plot the data
    ax1.plot(months, pen, label='FAO Penman', linewidth='2', zorder=5, linestyle='-',  color = 'green')
    ax1.plot(months, ohd, label='OHD Climo', linewidth='2', zorder=5, linestyle='-',  color = 'orange')
    ax1.plot(months, sa, label='Original SA', linewidth='2', zorder=5, linestyle='-',  color = 'magenta')
    ax1.plot(months, mape, label='Operational MAPE', linewidth='2', zorder=5, dashes=(5,4),linestyle='-', color = 'red')    
    ax1.plot(months, calb, label='Calb ET-Demand', linewidth='2', zorder=5, dashes=(5,4), linestyle='-', color = 'blue')
    
    ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
    ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
    
    majorLocator = MultipleLocator(1)
    ax1.xaxis.set_major_locator(majorLocator)
    
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.set_xlim(1)
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Mid-month ET Demand (mm/day)')
    plt.xticks(months, month_names)
    
    plt.ylim(ymin=0)
    
    #add plot legend with location and size
    ax1.legend(loc='lower center', prop={'size':9}, numpoints = 2)
    plt.title(basin.upper() + ' ET Demand Comparison' )
    
    # save fig
    figname = os.getcwd()[:-7] + '\\' + RFC +'\\Calibration_TimeSeries\\mape_test\\figures\\' + basin + '_PE_compare' +'.png'  
    plt.savefig(figname, dpi=175,bbox_inches='tight')

plt.clf()    
plt.close()
#Turn interactive plot mode off (don't show figures)
#plt.ioff()    
print 'Complete!'
print 'Script Completed'
