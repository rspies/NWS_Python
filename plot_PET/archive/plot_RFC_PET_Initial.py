#plot_ts_hydrographs.py
#python script to loop time series files in a folder and plot hydrographs
#Author: Cody Moser, PhD
#cody.lee.moser@noaa.gov
#NOAA/NWS/MARFC

print "Start Script"

import os
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
maindir = os.getcwd()

rfc = 'NERFC'
csv_read_NWS = open(maindir + os.sep + 'NERFC_Plot_PET_Initial_NWS.csv', 'r')
csv_read_FAO = open(maindir + os.sep + 'NERFC_Plot_PET_Initial_FAOPM.csv', 'r')
csv_read_apri = open(maindir + os.sep + 'NERFC_Plot_PET_apriori_ETD.csv', 'r')

data_NWS = pd.read_csv(csv_read_NWS, delimiter=',', skip_footer=0, header=0)
data_FAO = pd.read_csv(csv_read_FAO, delimiter=',', skip_footer=0, header=0)
data_apri = pd.read_csv(csv_read_apri, delimiter=',', skip_footer=0, header=0)

all_basins = list(data_NWS.columns.values)
x = range(1,13,1) # month range
count = 1
plot_num = 1
fig = plt.figure(figsize=(7,6))          
fig.suptitle('Initial Mid-month ET-Demand Comparison'+' (Units = mm/day)',y=1.02,fontsize=17)

for basin in all_basins:
    if basin != 'month' and basin != 'Month':
        y1 = list(data_NWS[basin])[:12]
        y2 = list(data_FAO[basin])[:12]
        y3 = list(data_apri[basin])[:12]
        
        ax1 = plt.subplot(2,2,plot_num)
        ax1.plot(x,y1, color='black', markersize=4, linestyle='-', linewidth=1, zorder=5, label = rfc + ' Initial')
        ax1.plot(x,y2, color='red', markersize=4, linestyle='-', linewidth=1, zorder=5, label = 'FAO-PM')
        ax1.plot(x,y3, color='green', markersize=4, linestyle='-', linewidth=1, zorder=5, label = 'Apriori ETD')
        
        ax1.minorticks_on()
        ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3, alpha=0.5)
        ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3, alpha=0.5)
        #ax1.set_xlabel('Month', fontsize='4')
        #ax1.set_ylabel('PET [mm/day]', fontsize='8')
        #labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        #t = range(1,14,1)
        plt.xticks(x, labels, fontsize=9)
        ax1.tick_params(labelsize=9)
        ax1.set_xlim([1,12])
        ax1.set_ylim([0,6])
        #ax1.legend(loc='upper left', prop={'size':4})
        ax1.xaxis.set_minor_locator(AutoMinorLocator(1))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(1))
        #ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
        plt.ioff()
        plt.title(basin, fontsize='14')
        count +=2; plot_num += 1
        
#### add a single legend outside the subplots
ax1.legend(loc="center",shadow=True,fontsize=15,bbox_to_anchor=(-0.1, 1.38))

print 'Saving figure...'
csv_read_NWS.close(); csv_read_FAO.close()
figname = maindir + os.sep + rfc + '_PET_inital_analysis.png'
            
#plt.savefig(figname, bbox_inches='tight', dpi=300)
plt.tight_layout()
subplots_adjust(left=None, bottom=None, right=None, top=0.9, wspace=0.25, hspace=0.8) #adjust white space 
plt.savefig(figname, bbox_inches='tight', dpi=350)
plt.close()
plt.show()

print "End Script"

