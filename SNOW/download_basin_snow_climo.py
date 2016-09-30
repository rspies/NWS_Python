#Created on 2/14/2016
#@author: rspies (rspies@lynkertech.com)
# Python 2.7
# Description: Download NOHRSC SNODAS data for a list of basins and output to a csv
# Note: data download in year
### Example NOHRSC data: http://www.nohrsc.noaa.gov/interactive/html/graph.html?brfc=ncrfc&basin=scri4&w=600&h=400&o=a&uc=0&by=2002&bm=1&bd=1&bh=6&ey=2003&em=1&ed=7&eh=5&data=1&units=0

import os
import urllib2
import time
import pandas as pd

os.chdir("../..") # change dir to \\NWS
maindir = os.getcwd()

############ User input ################
RFC = 'NCRFC_FY2016'
fx_group = 'RED+'
yr_start = 2002; yr_end = 2015
workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep

if fx_group != '':
    task_csv = RFC[:5] + '_fy16_task_summary_' + fx_group + '.csv'
    basin_col = 'basin' # 'BASIN' # list column to pull the basin id for searching on the NOHRSC website
    out_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'download_data' + os.sep + fx_group + os.sep
    summary_file = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'NOHRSC_data_download_summary_' + fx_group + '.csv'
else:
    task_csv = RFC[:5] + '_fy16_task_summary.csv'
    basin_col = 'CH5_ID' # 'BASIN' # list column to pull the basin id for searching on the NOHRSC website
    out_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'download_data' + os.sep 
    summary_file = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'NOHRSC_data_download_summary.csv'

########################################
summary = open(summary_file,'w')
summary.write('Basin,SHEF_ID,SNODAS_area_sq_mi\n')
read_csv = open(workingdir + task_csv,'r')
df = pd.read_csv(read_csv,sep=',',header=0)
read_csv.close()

if basin_col in df:
    ch5id = df[basin_col].tolist()
else:
    print '"' + basin_col + '" not in csv header...'

######### create clean list of basins to search
ch5id_list =[] 
for basin in ch5id:
    if len(str(basin)) != 5:
        basin = str(basin).upper().rstrip('LOC')
        basin = str(basin).upper().rstrip('UPR')
        basin = str(basin).upper().rstrip('MID')
        basin = str(basin).upper().rstrip('LWR')
    if str(basin).upper() == 'NEW LOCATION' or str(basin) == 'nan' or str(basin) == 'N/A' or str(basin) == 'NEW ' or str(basin) == 'N\A' or str(basin) == 'NAN':
        basin = ''
        print 'New Location basin or NA (no id) -> ignored'
    elif len(str(basin)) != 5:
        print 'Warning - basin id is not 5 characters: ' + str(basin).upper()
    if str(basin).upper() not in ch5id_list and str(basin) != '': # check for duplicates and empty strings
        ch5id_list.append(str(basin).upper())
        
print ch5id_list
#ch5id_list = ['HVNM4'] # manually run basins with this list
count = 0
#### loop through basin list and query website for data
for basin_query in ch5id_list:
    print 'Processing: ' + basin_query
    if os.path.exists(out_dir + basin_query + '_snodas.csv') == False:
        file_save = open(out_dir + basin_query + '_snodas.csv','w')
        file_save.write('date,snow_cover_%,swe_min,swe_mean,swe_max,depth_min,depth_mean,depth_max\n') # write header at start of file
    else:
        file_save = open(out_dir + basin_query + '_snodas.csv','a')
    yr_int = yr_start
    if str(basin_query) != 'nan' and str(basin_query) != 'na': # check that basin id is acceptable format
        while yr_int <= yr_end:
            print 'Connecting to NOHRSC website for ' + basin_query + ' --> ' + str(yr_int) + '...'
            if yr_int == yr_start: # start 10/1/2002
                response = urllib2.urlopen('http://www.nohrsc.noaa.gov/interactive/html/graph.html?brfc='+RFC[:5].lower()+'&basin=' + basin_query + '&w=600&h=400&o=a&uc=0&by='+str(yr_int)+'&bm=10&bd=1&bh=0&ey='+str(yr_int)+'&em=12&ed=31&eh=23&data=1&units=0')
            else:
                response = urllib2.urlopen('http://www.nohrsc.noaa.gov/interactive/html/graph.html?brfc='+RFC[:5].lower()+'&basin=' + basin_query + '&w=600&h=400&o=a&uc=0&by='+str(yr_int)+'&bm=1&bd=1&bh=0&ey='+str(yr_int)+'&em=12&ed=31&eh=23&data=1&units=0')
            noh_page = response.read()
            seg = noh_page.replace('</td></tr>','\n') # use this to identify the end of line
            sep = seg.split('\n')
            
            for line in sep:
                # split variables with comma
                csv_line = line.replace('<tr><td>','')
                csv_line = csv_line.replace('</td><td>',',')
                csv_line = csv_line.replace('</td></tr>','')
                len_line = csv_line.split(',')
                if yr_int == yr_start and 'SHEF ID:' in csv_line and len(len_line) == 2:
                    print len_line
                    summary.write(basin_query+',')
                    summary.write(len_line[1]+',')
                if yr_int == yr_start and 'Basin Area:' in csv_line and len(len_line) == 2:
                    print len_line
                    summary.write(len_line[1].strip('sq. mi') + '\n')

                if len(len_line) == 8:
                    file_save.write(csv_line + '\n')

            print 'delaying to avoid detection...'
            time.sleep(5) # delays for 10 second
            yr_int += 1
    file_save.close()
    count += 1
summary.close()
print 'Script completed!!'
