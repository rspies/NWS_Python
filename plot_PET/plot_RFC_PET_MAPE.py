#plot_ts_hydrographs.py
#python script to loop time series files in a folder and plot hydrographs
#Author: Cody Moser, PhD
#cody.lee.moser@noaa.gov
#NOAA/NWS/MARFC

print("Start Script")

import os
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
maindir = os.getcwd()

############################### User Input ####################################
maindir = os.path.abspath(r'D:\projects\2021_twdb_wgrfc_calb\processed_data\PET')
rfc = 'WGRFC'
version = 'initial' # choices: 'initial', 'draft', 'final'
#csv_read_NWS = open(maindir + os.sep + 'plot_input' + os.sep + rfc + '_Plot_PET_Initial_NWS_MAPEAdj.csv', 'r')
csv_read_FAO = open(maindir + os.sep + 'plot_input' + os.sep + rfc + '_Plot_PET_Initial_FAOPM.csv', 'r')
csv_read_apri = open(maindir + os.sep + 'plot_input' + os.sep + rfc + '_Plot_PET_apriori_ETD.csv', 'r')
csv_read_MAPE = open(maindir + os.sep + 'plot_input' + os.sep + rfc + '_Plot_PET_MAPE_ETD.csv', 'r')
csv_read_station = open(maindir + os.sep + 'plot_input' + os.sep + rfc + '_Plot_PET_station_climofill_ETD.csv', 'r')
csv_read_calb = maindir + os.sep + rfc + '_Plot_PET_'+ version + '_calb.csv'

############################ End User Input ###################################
print('Be sure to check all units!!!!!!!!!')
#data_NWS = pd.read_csv(csv_read_NWS, delimiter=',', skip_footer=0, header=0)
data_FAO = pd.read_csv(csv_read_FAO, delimiter=',', header=0)
data_apri = pd.read_csv(csv_read_apri, delimiter=',', header=0)
data_MAPE = pd.read_csv(csv_read_MAPE, delimiter=',', header=0)
data_station_fill = pd.read_csv(csv_read_station, delimiter=',', header=0)
if version == 'draft' or version == 'final':
    data_calb = pd.read_csv(open(csv_read_calb,'r'), delimiter=',', header=0)
    csv_read_calb.close()
# close files
#csv_read_NWS.close()
csv_read_FAO.close(); csv_read_MAPE.close()

all_basins = list(data_MAPE.columns.values)
x = range(1,13,1) # month range
count = 1
plot_num = 1
#fig = plt.figure(figsize=(6.0,7.5)) 
#all_basins = ['NGET2']

for basin in all_basins:
    if basin != 'month' and basin != 'Month':
        fig, ax1 = plt.subplots(figsize=(6.0,6.0))
        #fig = plt.figure(figsize=(6.0,8.5))          
        fig.suptitle(basin + ': Mid-month ET-Demand Comparison'+'\n(Units = mm/day)',fontsize=15)
        
        #y1 = list(data_NWS[basin])[:12]
        y2 = list(data_FAO[basin])[:12]
        y3 = list(data_apri[basin])[:12]
        y4 = list(data_MAPE[basin])[:12]
        y5 = list(data_station_fill[basin])[:12]
        
        #ax1 = plt.subplot(5,20,plot_num)
        #ax1.plot(x,y1, color='black', markersize=4, linestyle='-', linewidth=1, zorder=5, label = 'NWS initial (MAPE * PEadj)')
        ax1.plot(x,y2, color='orange', markersize=4, linestyle='-', linewidth=2.5, zorder=5, label = 'FAO-PM')
        ax1.plot(x,y3, color='purple', markersize=4, linestyle='-', linewidth=2.5, zorder=5, label = 'Apriori ETD')
        ax1.plot(x,y4, color='green', markersize=4, linestyle='-', linewidth=2.5, zorder=5, label = 'MAPE ETD')
        ax1.plot(x,y5, color='brown', markersize=4, linestyle='-', linewidth=2.5, zorder=5, label = 'Station Climo ETD')
        
        if version == 'draft' or version == 'final':
            y4 = list(data_calb[basin])[:12]
            ax1.plot(x,y4, color='aqua', markersize=4, linestyle='-', linewidth=2.5, zorder=5, label = rfc + ' Calb')
        
        ax1.minorticks_on()
        ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3, alpha=0.3)
        ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3, alpha=0.3)
        #ax1.set_xlabel('Month', fontsize='4')
        #ax1.set_ylabel('PET [mm/day]', fontsize='8')
        #labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        ax1.set_xlabel('Month')
        ax1.set_ylabel('PET mm/day')
        plt.xticks(x, labels, fontsize=12)
        ax1.tick_params(labelsize=12)
        ax1.set_xlim([1,12])
        ax1.set_ylim([0,8])
        #ax1.legend(loc='upper left', prop={'size':4})
        ax1.xaxis.set_minor_locator(AutoMinorLocator(1))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(1))
        #ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
        plt.ioff()
        #plt.title(basin, fontsize='13')
        count +=2; plot_num += 1
        
        #### add a single legend outside the subplots
        ax1.legend(loc="center left",fontsize=12,ncol=2,bbox_to_anchor=(0.1,-0.2))
        
        print(basin + ' saving figure...')
        figname = maindir + os.sep + 'plots' + os.sep + basin + '_PET_' + version + '_analysis_MAPE.png'
                    
        #plt.savefig(figname, bbox_inches='tight', dpi=300)
        plt.tight_layout()
        #subplots_adjust(left=None, bottom=None, right=None, top=0.9, wspace=0.25, hspace=0.5) #adjust white space (hspace is space on top of each subplot)
        plt.savefig(figname, bbox_inches='tight', dpi=350)
        plt.close()
        plt.show()

print("End Script")

