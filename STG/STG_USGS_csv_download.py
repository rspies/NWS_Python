# Created on October 6, 2015
# rspies (rspies@lynkertech.com)
# Python 2.7
# Loop through basin summary csv files and download USGS STG data files from 
# historic data site (pre WY 2007) http://ida.water.usgs.gov/ida/ 
# and recent site (2007 WY+) http://waterdata.usgs.gov/nwis
### USGS automated retrievals info: http://help.waterdata.usgs.gov/faq/automated-retrievals 

import os
import sys
import urllib2
import mechanize
import time
import pandas as pd

os.chdir("../..") # change dir to NWS main folder
maindir = os.getcwd()

############ User input ################
RFC = 'SERFC_FY2017'
fx_group = ''                   # set to '' if not used
basin_col = 'CH5_ID'            # 'BASIN' # list column to pull the basin id from the summary csv
date_end = '2017-01-01'         # YYYY-MM-DD  # end date for NWIS data search
date_begin = '1998-10-01'       # yyyy-MM-DD # default minimum date not to exceed
timestep = 'inst'               # options: 'daily' or 'inst' # daily or instantaneous (hourly/sub-hourly)
summary_output = 'yes'          # options: 'yes' or 'no' choice to create a text file with a summary of the data download
workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep

if fx_group != '':              # define directory locations if using fxgroup to break up download
    task_csv = RFC[:5] + '_fy17_task_summary_' + fx_group + '.csv'
    out_dir = workingdir + 'data_csv' + os.sep + 'STG' + os.sep + fx_group + os.sep + 'usgs_' + timestep + os.sep
    summary_file = workingdir + 'data_csv' + os.sep + 'STG' + os.sep + fx_group + '_' + timestep + '_STG_data_download_summary.csv'
else:
    task_csv = RFC[:5] + '_fy17_task_summary.csv'
    out_dir = workingdir + 'data_csv' + os.sep + 'STG' + os.sep + 'usgs_' + timestep + os.sep
    summary_file = workingdir + 'data_csv' + os.sep + 'STG' + os.sep + timestep + '_STG_data_download_summary.csv'
############ End User Input ##############

if summary_output == 'yes':
    summary = open(summary_file,'w') # create a summary output file
    summary.write('Basin,Gage ID,Recent Data Avail,Recent Data Website\n')
read_csv = open(workingdir + task_csv,'r')
df = pd.read_csv(read_csv,sep=',',header=0,dtype=object)
read_csv.close()

if basin_col in df:
    ch5id = df[basin_col].tolist()
else:
    print '"' + basin_col + '" not in csv header...'
if 'USGS_GAGE' in df:
    usgs_gages = df['USGS_GAGE'].tolist()
elif 'GAGE_ID' in df:
    usgs_gages = df['GAGE_ID'].tolist()
else:
    print 'Can not find USGS gage column identifier ("usgs_id" or "GAGE_ID") in csv header...' 
    
basin_gage = dict(zip(usgs_gages, ch5id)) # dictionary with merged gage id and basin id
if len(usgs_gages)!=len(set(basin_gage)): # check for duplicate gage ids being used
    print 'Warning!! Duplicate gage ids found... check if this is needed'
    #raw_input("Press Enter to continue...")

#usgs_gages = ['2207220','2202040','2198000','2197500'] # use this list to only process specific gages
print usgs_gages
count = 0
for each in usgs_gages:
    if str(each) != 'nan' and str(each) != 'na' and str(each).isdigit() == True: # check that gage id is acceptable format
        gage_id = str(int(each))
        if len(gage_id) == 7:
            gage_id = '0' + gage_id
        basin_id = str(basin_gage[each]).replace(' ', '')
        print gage_id + ' -> ' + basin_id
        summary.write(basin_id+','+gage_id+',')     
                
        ################################# recent data retrieval #######################################
        print 'Checking for recent data...'
        date_start = date_begin # YYYY-MM-DD
        #date_end = '2015-09-30' # YYYY-MM-DD
        
        if timestep == 'inst':                    
            recent_url = urllib2.urlopen('http://waterdata.usgs.gov/nwis/uv?cb_00065=on&format=rdb&site_no=' + gage_id + '&period=&begin_date=' + date_start +'&end_date='+date_end)
            br = mechanize.Browser()
            res = br.open('http://waterdata.usgs.gov/nwis/uv?cb_00065=on&format=rdb&site_no=' + gage_id + '&period=&begin_date=' + date_start +'&end_date='+date_end)
        if timestep == 'daily':                    
            recent_url = urllib2.urlopen('http://waterdata.usgs.gov/nwis/dv?cb_00065=on&format=rdb&site_no=' + gage_id + '&period=&begin_date=' + date_start +'&end_date='+date_end)
            br = mechanize.Browser()
            res = br.open('http://waterdata.usgs.gov/nwis/dv?cb_00065=on&format=rdb&site_no=' + gage_id + '&period=&begin_date=' + date_start +'&end_date='+date_end)

        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)               
        recent_page = res.read()
        if len(recent_page) < 1300:
            print 'NO RECENT DATA AVAILABLE FOR SITE -> ' + gage_id
            if summary_output == 'yes':
                summary.write('na,http://waterdata.usgs.gov/nwis/inventory/?site_no='+gage_id+'&agency_cd=USGS\n')
        else:
            print 'Processing recent data from USGS server...'
            file_save = open(out_dir + basin_id + '_STG_' + timestep + '.txt','w')
            file_save.write(recent_page)
            file_save.close()
            if summary_output == 'yes':
                summary.write('YES,http://waterdata.usgs.gov/nwis/inventory/?site_no='+gage_id+'&agency_cd=USGS\n')
        br.close()
        print 'delaying to avoid detection...\n'
        time.sleep(10) # delays for 10 second
    count += 1
if summary_output == 'yes':
    summary.close()
print 'Script completed'
