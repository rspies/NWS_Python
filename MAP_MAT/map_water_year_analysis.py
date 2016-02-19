# Ryan Spies
# 7/30/2014
# Python 2.6.5
# This script converts injests tab delimited text files from the map_mat_format_conversion.py output
# groups 6-hr MAP data into water year accumulations

#!!!!!!!!!!! Units left in inches and degrees F !!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!! Data must be 6 hour time steps !!!!!!!!!!!!!!!!!!!!!!

import os
import numpy as np
from dateutil import parser
path = os.getcwd()
os.chdir("../..")
maindir = os.getcwd()

######################## User Input Section ############################
rfc = 'LMRFC_FY2016'
# give directory of original RFC MAP/MAT files in single column .txt file format
map_dir = maindir + '\\Calibration_NWS\\' + rfc[:5] + os.sep + rfc + '\\datacards\\MAP\\MAP_single_column\\'
# give directory of output water year analysis csv files
out_dir = maindir + '\\Calibration_NWS\\' + rfc[:5] + os.sep + rfc + '\\datacards\\MAP\\MAP_water_year\\'
###################### End User Input ##################################

rfc_files = os.listdir(map_dir)
rfc_basins = []
for name in rfc_files:
    if name.endswith('.txt'): # only use text files in diretory
        rfc_basins.append(name)

for files in rfc_files:
    # locate only .mat and .map files
    if files[-9:-4] == 'MAP06' or files[-7:-4] == 'MAP':
        basin = files.split('_')[0]
        basin_title = str.upper(basin)
        print basin_title 
        #if basin_title == 'NOTG1':
        file1 = map_dir + '\\' + files
        fw = open(out_dir + '\\' + basin_title + '_WY_' + 'MAP.csv','w')
        fw.write('Water Year' + ',' + 'Accumulated MAP' + ',' + '# of 6hr values\n')        
        wy_data= {}
        fg = open(file1,'r')
        for each in fg:
            spl = each.split('\t')
            date = parser.parse(spl[0])
            prec = float(spl[1])
            if date.month >= 10: # all data starting on Oct 1 counts towards the next years WY total
                if int(date.year)+1 in wy_data:
                    wy_data[date.year+1].append(prec)
                else:
                    wy_data[date.year+1] = [prec]
            else:
                if int(date.year) in wy_data:
                    wy_data[date.year].append(prec)
                else:
                    wy_data[date.year] = [prec]   
        fg.close()
        for each_wy in wy_data:
            wy_map = np.sum(wy_data[each_wy])
            num_values = len(wy_data[each_wy])
            fw.write(str(each_wy) + ',' + str(wy_map) +',' + str(num_values) + '\n')
        fw.close()
print 'Finito!!!'
