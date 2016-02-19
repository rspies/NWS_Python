#plot_ts_hydrographs.py
#python script to loop time series files in a folder and plot hydrographs
#Author: Cody Moser, PhD
#cody.lee.moser@noaa.gov
#NOAA/NWS/MARFC

print "Start Script"

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pylab
from pylab import *
from matplotlib.ticker import AutoMinorLocator

csv_read = open(r'P:\NWS\Python\Plot_Runoff\SERFC\SERFC_Runoff.csv', 'r')

data = numpy.genfromtxt(csv_read, delimiter=',', skip_header=1, skip_footer=0,
                                names=['WY', 'COCF1', 'FGOG1', 'FLRV2', 'PLMF1', 'SRDV2', 'WORF1'])
x = data['WY']
COCF1 = data['COCF1']
FGOG1 = data['FGOG1']
FLRV2 = data['FLRV2']
PLMF1 = data['PLMF1']
SRDV2 = data['SRDV2']
WORF1 = data['WORF1']
          
#eq = r'$\mathdefault{N=0.8A^{0.3}}$'

fig = plt.figure()

ax1 = plt.subplot(111)

ax1.plot(x,COCF1, color='black', markersize=4, linestyle='-', linewidth=2, label='COCF1', zorder=5)
ax1.plot(x,FGOG1, color='red', markersize=4, linestyle='-', linewidth=2, label='FGOG1', zorder=5)
ax1.plot(x,FLRV2, color='blue', markersize=4, linestyle='-', linewidth=2, label='FLRV2', zorder=5)
ax1.plot(x,PLMF1, color='green', markersize=4, linestyle='-', linewidth=2, label='PLMF1', zorder=5)
ax1.plot(x,SRDV2, color='purple', markersize=4, linestyle='-', linewidth=2, label='SRDV2', zorder=5)
ax1.plot(x,WORF1, color='yellow', markersize=4, linestyle='-', linewidth=2, label='WORF1', zorder=5)

ax1.minorticks_on()
ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)

ax1.set_xlabel('Water Year', fontsize='8')
ax1.set_ylabel('Runoff (inches)', fontsize='8')

ax1.tick_params(labelsize=8)

ax1.set_xlim([1960,2015])
ax1.set_ylim([0,28])

ax1.legend(loc='upper right', prop={'size':8})

ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
plt.title('SERFC Water Year Runoff', fontsize='8')

plt.ioff()

figname = r'P:\\NWS\\Python\\Plot_Runoff\\SERFC\\SERFC_Runoff.png'
            
plt.savefig(figname, dpi=300)

#plt.show()

csv_read.close()

print "End Script"

raw_input("Press Enter to continue...")
