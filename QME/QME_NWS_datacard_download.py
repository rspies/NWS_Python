#Created on October 1, 2014
#@author: rspies
# Python 2.7
# loop through basin summary csv files and download USGS QME datacard files 
# from http://dipper.nws.noaa.gov/hdsb/data/archived/usgs.html. 
# Uses urllib2 module

import os
import sys
import urllib2
import time
import pandas as pd

os.chdir("../..") # change dir to \\AMEC\\NWS
maindir = os.getcwd()

############ User input ################
RFC = 'MBRFC_FY2016'
fx_group = 'BigYel_resup' # set to '' if not used
basin_col = 'CH5_ID' # 'BASIN' # list column to pull the basin id from the summary csv
workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep

if fx_group != '':
    task_csv = RFC[:5] + '_fy16_task_summary_' + fx_group + '.csv'
    out_dir = workingdir + 'datacards' + os.sep + 'QME' + os.sep + fx_group + os.sep + 'QME_Lynker_download' + os.sep
    summary_file = workingdir + 'datacards' + os.sep + 'QME' + os.sep + fx_group + os.sep + 'QME_datacard_download_summary_' + fx_group + '.csv'
else:
    task_csv = RFC[:5] + '_fy16_task_summary.csv' #_' + fx_group + '.csv'
    out_dir = workingdir + 'datacards' + os.sep + 'QME' + os.sep #+ fx_group + os.sep + 'QME_Lynker_download' + os.sep
    summary_file = workingdir + 'datacards' + os.sep + 'QME_datacard_download_summary.csv' #_' + fx_group + '.csv'

date_start = '1948-10-01' # YYYY-MM-DD -> start on 10/1 to prevent CHPS issues
date_end = '2014-09-30' # YYYY-MM-DD
########################################

summary = open(summary_file,'w')
summary.write('Basin,Gage ID,LAT,LON,Drainage Area(mi),Download Start,Download End,Valid Data,Missing Data,Gage Website\n')
read_csv = open(workingdir + task_csv,'r')
df = pd.read_csv(read_csv,sep=',',header=0)
read_csv.close()
ch5id =[]; usgs_gages=[]; latitude=[]; longitude=[]
if basin_col in df:
    ch5id = df[basin_col].tolist()
else:
    print '"' + basin_col + '" not in csv header...'
if 'usgs_id' in df:
    usgs_gages = df['usgs_id'].tolist()
else:
    print '"usgs_id" not in csv header...' 
    if 'GAGE_ID' in df:
        usgs_gages = df['GAGE_ID'].tolist()
    else:
        print '"GAGE_ID" not in csv header...' 
print ch5id
print usgs_gages
gage_basin = dict(zip(usgs_gages, ch5id))
#usgs_gages = ['6259000'] # run specific gages 
count = 0
for each in usgs_gages:
    if str(each) != 'nan' and str(each) != 'na' and str(each) != '' and str(each)[:1].isalpha() == False: # check for missing or non-usgs gage ids
        gage_id = str(int(str(each)[:8]))
        if len(gage_id) == 7:
            gage_id = '0' + gage_id
        basin_id = gage_basin[each].replace(' ', '').upper()
        #lat = str(latitude[count])
        #lon = str(longitude[count])
        print gage_id + ' -> ' + basin_id
        response = urllib2.urlopen('http://dipper.nws.noaa.gov/cgi-bin/hdsb/hdb/create_time_series.pl?source=usgs&id=' + gage_id + '&type=discharge&nozeros=nozeros&sdate=' + date_start +'&edate=' + date_end + '&output=browser&flags=none')
        the_page = response.read()
        summary.write(basin_id+','+gage_id+',')#+lat+','+lon+',')
        if len(the_page) < 100: # page returns no data info
            print 'QME data not found for site (site may or may not exist)...'
            #summary.write(',,na,na,na,na,na\n')
            ### look at USGS gage website for Lat/Lon info
            response = urllib2.urlopen('http://waterdata.usgs.gov/nwis/inventory/?site_no='+ gage_id +'&agency_cd=USGS')
            usgs_page = response.read()
            sep = usgs_page.split('\n')[-150:]
            lat='na';lon='na';area='na';link='na'
            for each in sep:
                if 'Latitude' in each:
                    line = each
                    line = line.replace('&#176','')
                    line = line.replace(';',',')
                    line = line.replace("\'",',')
                    line = line.replace('<dd>','')
                    line = line.replace('Latitude','')
                    line = line.replace('Longitude','')
                    line = line.replace('&nbsp','')
                    line = line.replace('"','')
                    nums = line.split(',')
                    sys.path.append(os.getcwd() + os.sep + 'python' + os.sep + 'modules')
                    import conversions
                    lat = conversions.dms_to_dd(float(nums[0]),float(nums[1]),float(nums[2]),'N')
                    lon = conversions.dms_to_dd(float(nums[4]),float(nums[5]),float(nums[6]),'W')
                    link = 'http://waterdata.usgs.gov/nwis/inventory/?site_no='+ gage_id +'&agency_cd=USGS'
                if 'Drainage area' in each:
                    line = each
                    line = line.replace('<dd>','')
                    line = line.replace('</dd>','\t')
                    line = line.replace(',','')
                    line = line.replace('Drainage area: ','')
                    line = line.replace(' square miles','')
                    area = line.split('\t')[0]
            summary.write(str(lat)+','+str(lon) + ',' + str(area) + ',na,na,na,na,' + link + '\n')
        else:
            final_page = the_page.replace(gage_id,basin_id,1)
            total_obs = final_page.count(gage_id)
            total_missing = (final_page.count('-999.00') + final_page.count('-998.00'))
            total_valid = total_obs - total_missing
            ### look at USGS gage website for Lat/Lon info
            response = urllib2.urlopen('http://waterdata.usgs.gov/nwis/inventory/?site_no='+ gage_id +'&agency_cd=USGS')
            usgs_page = response.read()
            sep = usgs_page.split('\n')[-150:]
            for each in sep:
                if 'Latitude' in each:
                    line = each
                    line = line.replace('&#176','')
                    line = line.replace(';',',')
                    line = line.replace("\'",',')
                    line = line.replace('<dd>','')
                    line = line.replace('Latitude','')
                    line = line.replace('Longitude','')
                    line = line.replace('&nbsp','')
                    line = line.replace('"','')
                    nums = line.split(',')
                if 'Drainage area' in each:
                    line = each
                    line = line.replace('<dd>','')
                    line = line.replace('</dd>','\t')
                    line = line.replace(',','')
                    line = line.replace('Drainage area: ','')
                    line = line.replace(' square miles','')
                    area = line.split('\t')[0]
            sys.path.append(os.getcwd() + os.sep + 'python' + os.sep + 'modules')
            import conversions
            lat = conversions.dms_to_dd(float(nums[0]),float(nums[1]),float(nums[2]),'N')
            lon = conversions.dms_to_dd(float(nums[4]),float(nums[5]),float(nums[6]),'W')
            summary.write(str(lat)+','+str(lon)+','+area+','+date_start+','+date_end+','+str(total_valid)+','+str(total_missing)+',')
            summary.write('http://waterdata.usgs.gov/nwis/inventory/?site_no='+ gage_id +'&agency_cd=USGS'+'\n')
            file_save = open(out_dir + basin_id + '_qme.txt','w')
            file_save.write(final_page)
            file_save.close()
        print 'delaying to avoid detection...'
        time.sleep(10) # delays for 10 second
    count += 1

summary.close()
print 'Completed!!'