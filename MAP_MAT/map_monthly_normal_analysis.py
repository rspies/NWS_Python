# Ryan Spies
# 9/11/2014
# Python 2.6.5
# This script converts injests tab delimited text files from the map_mat_format_conversion.py output
# groups 6-hr MAP data into monthly accumulations to calculate the 30-year mean
# 1981-2010 (used to compare to PRISM monthly data)

#!!!!!!!!!!! Units left in inches and degrees F !!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!! Data must be 6 hour time steps !!!!!!!!!!!!!!!!!!!!!!

import os
import numpy as np
from dateutil import parser
path = os.getcwd()

######################## User Input Section ############################
rfc = 'SERFC'
# give directory of original RFC MAP/MAT files in single column .txt file format
map_dir = 'P:\NWS\Calibration_NWS\\' + rfc + '\\from' + rfc + '\\MAP\\single_column'
# give directory of output water year analysis csv files
out_dir = 'P:\\NWS\\Calibration_NWS\\' + rfc + '\\from' + rfc + '\\MAP\\normal_monthly'
###################### End User Input ##################################

rfc_files = os.listdir(map_dir)
rfc_basins = []
for name in rfc_files:
    if name.endswith('.txt'): # only use text files in diretory
        rfc_basins.append(name)
fw = open(out_dir + '\\' + rfc + '_Monthly_MAP_Summary_1981_2010' + '.csv','w')
fw.write('Basin,'+'Jan,'+'Feb,'+'Mar,'+'Apr,'+'May,'+'Jun,'+'Jul,'+'Aug,'+'Sep,'+'Oct,'+'Nov,'+'Dec,'+'\n')
for files in rfc_files:
    # locat only .mat and .map files
    if files[-9:-4] == 'MAP06' or files[-7:-4] == 'MAP':
        basin = files[:5]
        basin_title = str.upper(basin)
        print basin_title 
        fw.write(basin_title + ',')
        # enter file locations for old and new files
        file1 = map_dir + '\\' + basin + '_MAP06.txt'
        month_data= {'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[],'11':[],'12':[]}
        fg = open(file1,'r')
        for each in fg:
            spl = each.split('\t')
            date = parser.parse(spl[0])
            prec = float(spl[1])
            if date.year >= 1981 and date.year <= 2010:
                month_data[str(int(date.month))].append(prec) 
        fg.close()
        count = 1
        while count <= 12:
            for each_mn in month_data:
                if each_mn == str(count):
                    mn_map = np.sum(month_data[each_mn])/30 # 30-year data mean
                    fw.write(str("%.2f" % mn_map) + ',')
            count += 1
        fw.write('\n')
fw.close()
print 'Finito!!!'
