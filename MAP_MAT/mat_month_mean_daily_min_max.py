# Ryan Spies
# 8/5/2014
# Python 2.6.5
# This script calculates a mean daily max and min temperature for each month

#!!!!!!!!!!! Units left in degrees F !!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!! Data must be 6 hour time steps !!!!!!!!!!!!!!!!!!!!!!

import os
import numpy as np
from dateutil import parser
from dateutil.relativedelta import relativedelta
import csv
path = os.getcwd()

######################## User Input Section ############################
rfc = 'NERFC'
# give directory of original RFC MAP/MAT files
map_dir = 'P:\\NWS\\Calibration_NWS\\NERFC\\fromNERFC\\MAT'
###################### End User Input ##################################

rfc_files = os.listdir(map_dir)
rfc_basins = []
for name in rfc_files:
    if name.endswith('.txt'): # only use text files in diretory
        rfc_basins.append(name)

for files in rfc_files:
    # locat only .mat and .map files
    if files[-9:-4] == 'MAT06' or files[-7:-4] == 'MAT':
        basin = files[:5]
        basin_title = str.upper(basin)
        print basin_title 

        # enter file locations for old and new files
        file1 = map_dir + '\\' + files
        csvfile = open('P:\\NWS\\Calibration_NWS\\NERFC\\fromNERFC\\MAT\\' + basin_title + '_monthly_tmin_tmax_.csv','w')
        writer = csv.writer(csvfile)
        writer.writerow(['Monthly mean daily max and min temperatures (F)'])
        writer.writerow(['Year', 'Variable', 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])              
        day_data= {}
        fg = open(file1,'r')
        # create a dictionary with 6hr data grouped into daily data
        print 'Creating dictionary with 6hr data grouped into daily data...'
        for each in fg:
            spl = each.split('\t')
            date = parser.parse(spl[0])
            all_day = date.replace(hour=12)
            temp = float(spl[1])
            if temp < -100 or temp > 120:
                print 'Warning... bad data: ' + str (date) 
                temp = 'na'
            if all_day in day_data:
                day_data[all_day].append(temp)
            else:
                day_data[all_day] = [temp]   
        fg.close()
        start = min(day_data).replace(month=1,day=1,hour=12)
        end = max(day_data).replace(month=12,day=1,hour=12)
        
        # create two dictionaries with tmin and tmax data for each day
        print 'Calculating Tmin and Tmax for each day...'
        mnday_min = {}; mnday_max = {}
        for day in day_data:
            tmin = min(day_data[day])
            tmax = max(day_data[day])
            day_mn = day.replace(day=1)
            if day_mn in mnday_min:
                mnday_min[day_mn].append(tmin)
            else:
                mnday_min[day_mn] = [tmin]
            if day_mn in mnday_max:
                mnday_max[day_mn].append(tmax)
            else:
                mnday_max[day_mn] = [tmax]
         
        # write to new csv file: the mean daily values for each month
        print 'writing data to csv file...'
        year_max = []; year_min = []
        while start <= end:
            ## tmax output
            if start in mnday_max:
                year_max.append(np.average(mnday_max[start]))
            else:
                year_max.append('na')
            if start.month == 12:
                csvfile.write(str(start.year) + ',' + 'Tmax' + ',')
                for each in year_max:
                    csvfile.write(str(each) + ',')
                csvfile.write('\n')
                year_max = []
            # tmin output 
            if start in mnday_min:
                year_min.append(np.average(mnday_min[start]))
            else:
                year_min.append('na')
            if start.month == 12:
                csvfile.write(str(start.year) + ',' + 'Tmin' + ',')
                for each in year_min:
                    csvfile.write(str(each) + ',')
                csvfile.write('\n')
                year_min = []
            #writer.writerow([start.year,'Tmax',np.average(mnday_max[start.replace(month=1)]),np.average(mnday_max[start.replace(month=2)]),np.average(mnday_max[start.replace(month=3)]),np.average(mnday_max[start.replace(month=4)]),np.average(mnday_max[start.replace(month=5)]),np.average(mnday_max[start.replace(month=6)]),np.average(mnday_max[start.replace(month=7)]),np.average(mnday_max[start.replace(month=8)]),np.average(mnday_max[start.replace(month=9)]),np.average(mnday_max[start.replace(month=10)]),np.average(mnday_max[start.replace(month=11)]),np.average(mnday_max[start.replace(month=12)])])
            start = start + relativedelta(months=1)
        csvfile.close()
print 'Finito!!!'
