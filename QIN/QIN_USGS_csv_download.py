# Created on October 6, 2015
# rspies (rspies@lynkertech.com)
# Python 2.7
# Loop through basin summary csv files and download USGS QIN data files from 
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
RFC = 'LMRFC_FY2017'
fx_group = ''                   # set to '' if not used
basin_col = 'CH5_ID'            # 'BASIN' # list column to pull the basin id from the summary csv
date_end = '2016-09-30'         # YYYY-MM-DD  # end date for NWIS data search
summary_output = 'yes'          # options: 'yes' or 'no' choice to create a text file with a summary of the data download
workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep

if fx_group != '':              # define directory locations if using fxgroup to break up download
    task_csv = RFC[:5] + '_fy17_task_summary_' + fx_group + '.csv'
    out_dir = workingdir + 'data_csv' + os.sep + 'QIN' + os.sep + fx_group + os.sep
    summary_file = workingdir + 'data_csv' + os.sep + 'QIN' + os.sep + fx_group + '_QIN_data_download_summary.csv'
else:
    task_csv = RFC[:5] + '_fy17_task_summary.csv'
    out_dir = workingdir + 'data_csv' + os.sep + 'QIN' + os.sep 
    summary_file = workingdir + 'data_csv' + os.sep + 'QIN' + os.sep + 'QIN_data_download_summary.csv'
############ End User Input ##############

if summary_output == 'yes':
    summary = open(summary_file,'w') # create a summary output file
    summary.write('Basin,Gage ID,Historic Start,Historic End,Historic Data Website,Recent Data Avail,Recent Data Website\n')
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
    print 'Warning!! Duplicate gage ids should only be used for one basin'
    raw_input("Press Enter to continue...")

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
        
        if basin_id + '_historical.txt' in os.listdir(out_dir + 'pre_2007'): ## check if basin data has already been downloaded
            print 'Historic data file already exists (overwriting) -> ' + basin_id 
            #count += 1
            #continue
        ################################# historical data retrieval #######################################
        try:
            hist_summary = urllib2.urlopen('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print 'Trying gage site search again...'
            hist_summary = urllib2.urlopen('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
        hist_page = hist_summary.read()
        
        if '<tr><td align="center">' in hist_page: # checks if site has historic data (prior to 2007)
            print 'Processing historical data from USGS server...'
            br = mechanize.Browser()
            try:
                response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print 'Trying gage site search again...'
                response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
            br.select_form('CFForm_1')
            min_date = br.form.find_control("mindatetime").value[:10]
            max_date = br.form.find_control("maxdatetime").value[:10]
            print min_date + ' -> ' + max_date
            #min_date = '2000-10-01'
            #max_date = '2000-10-01'
            if int(max_date[:4])-int(min_date[:4]) >8: # break up download requests if more than 8 years to prevent server timeout
                interval = int((int(max_date[:4])-int(min_date[:4]))/4)
                mid_date1 = str(int(min_date[:4])+interval) + '-09-30'
                mid_date2 = str(int(mid_date1[:4])) + '-10-01'
                mid_date3 = str(int(mid_date1[:4])+interval) + '-09-30'
                mid_date4 = str(int(mid_date3[:4])) + '-10-01'
                mid_date5 = str(int(mid_date3[:4])+interval) + '-09-30'
                mid_date6 = str(int(mid_date5[:4])) + '-10-01'
                print 'File split1: ' + min_date + ' -> ' + mid_date1
            else:
                mid_date1 = max_date
            br['fromdate'] = str(min_date)
            br['todate'] = str(mid_date1)
            br['rtype'] = ['1'] # download to file (1), display in browser (3)
            try:
                submit_form = br.submit() # submit webpage request
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print 'Trying gage site search again...'
                response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                br.select_form('CFForm_1')
                br['fromdate'] = str(min_date)
                br['todate'] = str(mid_date1)
                br['rtype'] = ['1'] # download to file (1), display in browser (3)
                submit_form = br.submit() # submit webpage request
            result = submit_form.read().replace('\r','')
            file_save = open(out_dir + 'pre_2007' + os.sep + basin_id + '_historical.txt','w')
            file_save.write(result)
            br.close()
            
            if int(max_date[:4])-int(min_date[:4]) >8: # download remaining chunks of data if it was divided (more than 8 years)
                time.sleep(5) # delays for 5 seconds
                print 'File split2: ' + mid_date2 + ' -> ' + mid_date3
                br = mechanize.Browser()
                try:
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Trying gage site search again...'
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                br.select_form('CFForm_1')
                br['fromdate'] = str(mid_date2)
                br['todate'] = str(mid_date3)
                br['rtype'] = ['1'] # download to file (1), display in browser (3)
                try:
                    submit_form = br.submit() # submit webpage request
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Trying gage site search again...'
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                    br.select_form('CFForm_1')
                    br['fromdate'] = str(mid_date2)
                    br['todate'] = str(mid_date3)
                    br['rtype'] = ['1'] # download to file (1), display in browser (3)
                    submit_form = br.submit() # submit webpage request
                result = submit_form.read()#.replace('\r','')
                sep = result.split('\n')[67:] # skip file header
                for each in sep:
                    file_save.write(str(each))
                br.close()
                time.sleep(5) # delays for 5 seconds
                
                print 'File split3: ' + mid_date4 + ' -> ' + mid_date5
                br = mechanize.Browser()
                try:
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Trying gage site search again...'
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                br.select_form('CFForm_1')
                br['fromdate'] = str(mid_date4)
                br['todate'] = str(mid_date5)
                br['rtype'] = ['1'] # download to file (1), display in browser (3)
                try:
                    submit_form = br.submit() # submit webpage request
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Trying gage site search again...'
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                    br.select_form('CFForm_1')
                    br['fromdate'] = str(mid_date4)
                    br['todate'] = str(mid_date5)
                    br['rtype'] = ['1'] # download to file (1), display in browser (3)
                    submit_form = br.submit() # submit webpage request
                result = submit_form.read()#.replace('\r','')
                sep = result.split('\n')[67:] # skip file header
                for each in sep:
                    file_save.write(str(each))
                br.close()
                time.sleep(5) # delays for 5 seconds
                
                print 'File split4: ' + mid_date6 + ' -> ' + max_date
                br = mechanize.Browser()
                try:
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Trying gage site search again...'
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                br.select_form('CFForm_1')
                br['fromdate'] = str(mid_date6)
                br['todate'] = str(max_date)
                br['rtype'] = ['1'] # download to file (1), display in browser (3)
                try:
                    submit_form = br.submit() # submit webpage request
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Trying gage site search again...'
                    response = br.open('http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id)
                    br.select_form('CFForm_1')
                    br['fromdate'] = str(mid_date6)
                    br['todate'] = str(max_date)
                    br['rtype'] = ['1'] # download to file (1), display in browser (3)
                    submit_form = br.submit() # submit webpage request
                result = submit_form.read()#.replace('\r','')
                sep = result.split('\n')[67:] # skip file header
                for each in sep:
                    file_save.write(str(each))
                br.close()
            file_save.close()
            if summary_output == 'yes':
                summary.write(basin_id+','+gage_id+',')
                summary.write(min_date+','+max_date+',http://ida.water.usgs.gov/ida/available_records.cfm?sn=' + gage_id + ',')
        else:
            print 'NO HISTORIC DATA AVAILABLE FOR SITE -> ' + gage_id
            if summary_output == 'yes':
                summary.write(basin_id+','+gage_id+',')
                summary.write('na,na,na,')
        
        ################################# recent data retrieval #######################################
        print 'Checking for recent data...'
        date_start = '2007-09-30' # YYYY-MM-DD
        #date_end = '2015-09-30' # YYYY-MM-DD
                            
        recent_url = urllib2.urlopen('http://waterdata.usgs.gov/nwis/uv?cb_00060=on&cb_00065=on&format=rdb&site_no=' + gage_id + '&period=&begin_date=' + date_start +'&end_date='+date_end)
        br = mechanize.Browser()
        res = br.open('http://waterdata.usgs.gov/nwis/uv?cb_00060=on&cb_00065=on&format=rdb&site_no=' + gage_id + '&period=&begin_date=' + date_start +'&end_date='+date_end)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)               
        recent_page = res.read()
        if len(recent_page) < 1200:
            print 'NO RECENT DATA AVAILABLE FOR SITE -> ' + gage_id
            if summary_output == 'yes':
                summary.write('na,http://waterdata.usgs.gov/nwis/inventory/?site_no='+gage_id+'&agency_cd=USGS\n')
        else:
            print 'Processing recent data from USGS server...'
            file_save = open(out_dir + 'post_2007' + os.sep + basin_id + '_recent.txt','w')
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
