# merge_USGS_QIN_timeseries.py
# Created by: Ryan Spies (rspies@lynkertech.com)
# Description: creates a QIN time series in .csv format for import into CHPS
# capable of using the 2 files from the USGS -> downloaded with QIN_USGS_csv_download.py:
# 1. historical (before Oct 1, 2007) txt file 
# 2. recent (after Oct 1, 2007) txt file
### data retrieval info: http://waterdata.usgs.gov/nwis/?IV_data_availability
### USGS parameter codes: http://nwis.waterdata.usgs.gov/usa/nwis/pmcodes

#import script modules
import os
os.chdir("../..")  # change dir to NWS data folder
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
RFC = 'SERFC_FY2017'
fx_group = '' # set to '' if not used
dss_csv = 'off'          # options: 'on' or 'off' # create csv for dss import

if fx_group != '':
    histdata = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\QIN\\'+fx_group+'\\pre_2007\\'
    recentdata = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\QIN\\'+fx_group+'\\post_2007\\'
    outputpath = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\QIN\\'+fx_group+'\\merged_csv\\'
    dss_path = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_dss\\'  + fx_group
else:
    histdata = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\QIN\\pre_2007\\'
    recentdata = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\QIN\\post_2007\\'
    outputpath = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\QIN\\merged_csv\\'
    dss_path = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_dss'
####################################################################
#END USER INPUT SECTION
####################################################################

Basins = []
for each in os.listdir(histdata):
    if each.replace('_historical.txt','') not in Basins:
        Basins.append(each.replace('_historical.txt',''))
for each in os.listdir(recentdata):
    if each.replace('_recent.txt','') not in Basins:
        Basins.append(each.replace('_recent.txt',''))
print Basins
dss_dic = {} # dictionary for storing all locations/dates

for Basin in Basins:
    print 'Processing: ' + Basin
    historical_csv_file = histdata + Basin + '_historical.txt'
    recent_csv_file = recentdata + Basin + '_recent.txt'
    
    QIN_file = outputpath + Basin.upper() + '_QIN.csv'
    QIN_file_write = open(QIN_file, 'w')
    QIN_file_write.write('Location Names,' + Basin.upper() + '\n')
    QIN_file_write.write('Location Ids,' + Basin.upper() + '\n')
    QIN_file_write.write('Time,' + 'QIN [cfs]' + '\n')
    
    if Basin + '_historical.txt' in os.listdir(histdata):
        print 'Processing ' + Basin + '_historical.txt...'
        historic_file_read = open(historical_csv_file, 'rU')
 
        for row in historic_file_read:
            if row[0] != '#':                      #ignore header lines
                if 'site_no' in row:             # find the column with flow data (not the same column for all locations)
                    sep = row.split('\t')
                    flow_ind = sep.index('value')
                if 'DT' in row or 'ST' in row:    #find data lines with mention of time zone
                    sep = row.split('\t')
                    date = str(sep[1])
                    year = date[0:4]
                    month = date[4:6]
                    day = date[6:8]
                    hour = date[8:10]
                    minute = date[10:12]
                    second = date[12:14]
                    flow = str(sep[flow_ind])
                    inst_date = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
                    if flow == 'Ice':
                        QIN_file_write.write(inst_date + ',' + '-999.0' + '\n')
                    else:
                        QIN_file_write.write(inst_date + ',' + flow + '\n')
                        if dss_csv == 'on':
                            if inst_date not in dss_dic:
                                dss_dic[inst_date] = {}
                            dss_dic[inst_date][Basin]=str(float(flow))
        historic_file_read.close()
    else:
        print Basin + ': historical data file not found...'
    
    if Basin + '_recent.txt' in os.listdir(recentdata):
        print 'Processing ' + Basin + '_recent.txt...'
        recent_csv_file_read = open(recent_csv_file, 'r')
        
        for line in recent_csv_file_read:
            if '<!DOCTYPE html>' in line:           # some downloaded files only contain html from nonexistant gage site -> ignore file
                print '!!! Bad data file -> ignoring ' + Basin + '_recent.txt'
                if Basin + '_historical.txt' not in os.listdir(histdata):
                    print 'DELETING output merge file...'
                    QIN_file_write.close()
                    os.remove(QIN_file)
                break
            if line[0] != '#':                      # ignore header lines
                if 'agency_cd' in line:             # find the column with flow data (not the same column for all locations)
                    row = line.split('\t')
                    
                    if any('_00060' in j for j in row) == True: # check that flow data is in file (usgs code for streamflow: 00060)
                        for i, s in enumerate(row):
                            if '_00060' in s and '_00060_' not in s:
                                flow_index = i
                    elif any('_00065' in j for j in row) == True:
                        print '!!! Stage data only in post_2007 file??...'
                        if Basin + '_historical.txt' not in os.listdir(histdata):
                            print 'DELETING output merge file...'
                            QIN_file_write.close()
                            os.remove(QIN_file)
                        break # break file loop if flow data not available
                    else:
                        print '!!! Can not find flow data column id (00060 - discharge)...'
                        if Basin + '_historical.txt' not in os.listdir(histdata):
                            print 'DELETING output file...'
                            QIN_file_write.close()
                            os.remove(QIN_file)
                        break # break file loop if flow data not available
                            
                if 'DT' in line or 'ST' in line:    #find data lines with mention of time zone
                    line = line
                    line = line.replace('\t', ',')
                    line = line.replace('-', '')
                    line = line.replace(' ', '')
                    line = line.replace(':', '')
                    row = line.split(',')
                    date = str(row[2])
                    year = date[0:4]
                    month = date[4:6]
                    day = date[6:8]
                    hour = date[8:10]
                    minute = date[10:12]
                    second = '00'
                    flow = str(row[flow_index])
                    #QIN_file_write.write(str(date) + '00' + ',' + flow + '\n')
                    inst_date = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
                    if flow == 'Ice' or flow == 'Ssn' or flow == 'Eqp' or flow == '' or flow == 'Rat':
                        QIN_file_write.write(inst_date + ',' + '-999.0' + '\n')
                    else:
                        QIN_file_write.write(inst_date + ',' + str(float(flow)) + '\n')    
                        if dss_csv == 'on':
                            if inst_date not in dss_dic:
                                dss_dic[inst_date] = {}
                            dss_dic[inst_date][Basin]=str(float(flow))
        recent_csv_file_read.close()
    else:
        print Basin + ': _recent.txt file missing...'
    QIN_file_write.close()
###########################    
if dss_csv == 'on':
    print 'Writing to combined dss csv...'
    combine_csv = open(dss_path + os.sep + 'QIN_inst' + '_merged_for_dss.csv','w')
    combine_csv.write('Date,')
    for Basin in Basins:
        if Basin != Basins[-1]:
            combine_csv.write(Basin + ',')
        else:
            combine_csv.write(Basin + '\n')
    for datestep in sorted(dss_dic):
        combine_csv.write(datestep + ',')
        for Basin in Basins:
            if Basin in dss_dic[datestep]:
                combine_csv.write(dss_dic[datestep][Basin])
            else:
                combine_csv.write('')
            if Basin != Basins[-1]:
                combine_csv.write(',')
            else:
                combine_csv.write('\n')
    combine_csv.close()
print 'Script Complete'
