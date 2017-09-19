#Created on 5/23/2017
#@author: rspies
# Python 2.7
# This script converts individual QME datacard files to a single/merged csv file that can be imported for dss build

import os
import datetime
from dateutil import parser

os.chdir("../..") # change dir to \\AMEC\\NWS
maindir = os.getcwd()

############ User input ################
RFC = 'NCRFC_FY2017'
fx_group = '' # set to '' if not used
data_format = 'nhds' # choices: 'usgs' or 'chps' or 'nhds'
dss_csv = 'on'          # options: 'on' or 'off' # create csv for dss import

usgs_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data\\daily_discharge' # directory with USGS QME data
chps_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\QME\\QME_CHPS_export\\' # CHPS csv output files
nhds_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\QME\\' # NHDS data download (cardfiles)
new_file = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\datacards\\QME\\' # output summary tab delimited file location
########################################

if fx_group != '':
    nhds_files = nhds_files + os.sep + fx_group + os.sep + 'QME_Lynker_download' 
    dss_path = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_dss\\'  + fx_group
else: 
    nhds_files = nhds_files + os.sep + 'QME_Lynker_download' 
    dss_path = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_dss'

basins_list = []; count = 0

if data_format == 'usgs':
    QMEs = [f for f in os.listdir(usgs_files) if os.path.isfile(os.path.join(usgs_files, f))]
if data_format == 'chps':
    QMEs = [f for f in os.listdir(chps_files) if os.path.isfile(os.path.join(chps_files, f))]
if data_format == 'nhds':
    QMEs = [f for f in os.listdir(nhds_files) if os.path.isfile(os.path.join(nhds_files, f))]
dss_dic = {}
    
for QME in QMEs:
    print 'Reading data for: ' + QME
    count += 1
    if data_format == 'usgs': 
        csv_read = open(usgs_files + '\\' + QME, 'r')
        discharge = []; date = []
        ### read card file formatted .txt files lists
        line_count = 0
        for line in csv_read:
            if line_count >= 9: # ignore header lines
                sep = line.split()
                ### parse date columns
                month = str(sep[1])[:-2]
                year = str(sep[1])[-2:]
                if int(year) <= 17:
                    year = int(year) + 2000 # assume years <= 14 are in the 2000s
                else:
                    year = int(year) + 1900
                day = str(sep[2])
                full_date = datetime.datetime(year,int(month),int(day))
                date.append(full_date)
                if line_count == 12:
                    site_num = sep[0]
                discharge=sep[-1] # asssuming a single column datacard
                if dss_csv == 'on':
                    if str(full_date) not in dss_dic:
                        dss_dic[str(full_date)] = {}
                    if float(discharge) >= 0.0:
                        dss_dic[str(full_date)][QME]=str(float(discharge))
            line_count += 1
        csv_read.close()
    if data_format == 'chps': 
        csv_read = open(chps_files + '\\' + QME, 'r')
        discharge = []; date = []
        ### read card file formatted .txt files lists
        line_count = 0
        for line in csv_read:
            if line_count >= 2: # ignore header lines
                sep = line.split(',')
                full_date = parser.parse(sep[0])
                date.append(full_date.date())
                discharge=sep[-1] # asssuming a single column datacard
                if dss_csv == 'on':
                    if str(full_date) not in dss_dic:
                        dss_dic[str(full_date)] = {}
                    if float(discharge) >= 0.0:
                        dss_dic[str(full_date)][QME]=str(float(discharge))
            line_count += 1
        csv_read.close()
    if data_format == 'nhds': 
        csv_read = open(nhds_files + '\\' + QME, 'r')
        discharge = []; date = []
        ### read card file formatted .txt files lists
        line_count = 0
        for line in csv_read:
            if line_count >= 9: # ignore header lines
                sep = line.split()
                if len(sep) > 0: # ignore blank lines
                    if len(sep) < 4 and len(sep[-1]) < 10: # some QME files (from RFC) may not have gage/basin id as 1st index
                        sep.insert(0,'0000')
                    ### parse date columns
                    month = str(sep[1])[:-2]
                    year = str(sep[1])[-2:]
                    if int(year) <= 17:
                        year = int(year) + 2000 # assume years <= 17 are in the 2000s
                    else:
                        year = int(year) + 1900
                    day = str(sep[2])
                    if len(sep[-1]) > 10: # check for large streamflow values that get combined with day column
                        day = str(sep[2])[:-10]
                    full_date = datetime.datetime(year,int(month),int(day))
                    date.append(full_date)
                    if line_count == 12:
                        site_num = sep[0]
                    discharge=sep[-1] # asssuming a single column datacard
                    if dss_csv == 'on':
                        if str(full_date) not in dss_dic:
                            dss_dic[str(full_date)] = {}
                        if float(discharge) >= 0.0:
                            dss_dic[str(full_date)][QME]=str(float(discharge))
            line_count += 1
        csv_read.close()

if dss_csv == 'on':
    print 'Writing to combined dss csv...'
    combine_csv = open(dss_path + os.sep + 'QME_daily' + '_merged_for_dss.csv','w')
    combine_csv.write('Date,')
    for Basin in QMEs:
        if Basin != QMEs[-1]:
            combine_csv.write(Basin.split('_')[0] + ',')
        else:
            combine_csv.write(Basin.split('_')[0] + '\n')
    for datestep in sorted(dss_dic):
        combine_csv.write(str(datestep) + ',')
        for Basin in QMEs:
            if Basin in dss_dic[datestep]:
                combine_csv.write(dss_dic[datestep][Basin])
            else:
                combine_csv.write('')
            if Basin != QMEs[-1]:
                combine_csv.write(',')
            else:
                combine_csv.write('\n')
    combine_csv.close()   
print 'Completed!!'