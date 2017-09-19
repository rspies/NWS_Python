# USGS_format_txt_to_csv.py
# Created by: Ryan Spies (rspies@lynkertech.com)
# Description: creates a QIN/STG time series in .csv format for import into CHPS
# capable of using the NWIS download files from the USGS -> 
### data retrieval info: http://waterdata.usgs.gov/nwis/?IV_data_availability
### USGS parameter codes: http://nwis.waterdata.usgs.gov/usa/nwis/pmcodes

#import script modules
import os
os.chdir("../..")  # change dir to NWS data folder
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
RFC = 'NCRFC_FY2017'
fx_group = '' # set to '' if not used
variable = 'STG'
timestep = 'inst'       # options: 'daily' or 'inst' # daily or instantaneous (hourly/sub-hourly)
dss_csv = 'on'          # options: 'on' or 'off' # create csv for dss import

if fx_group != '':
    usgs_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\' + variable + '\\'+fx_group + os.sep + 'usgs_' + timestep + os.sep
    outputpath = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\' + variable + '\\'+fx_group + os.sep + 'csv_' + timestep + os.sep
    dss_path = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_dss\\'  + fx_group
else:
    usgs_files = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\' + variable + os.sep + 'usgs_' + timestep + os.sep
    outputpath = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_csv\\' + variable + os.sep + 'csv_' + timestep + os.sep
    dss_path = maindir + '\\Calibration_NWS\\' + RFC[:5] + os.sep + RFC + '\\data_dss'
####################################################################
#END USER INPUT SECTION
####################################################################
unit_label = {'STG':'STG [ft]','QIN':'QIN [cfs]'}
var_code = {'STG':'00065','QIN':'00060'}

Basins = []
for each in os.listdir(usgs_files):
    if each.replace('_' + variable + '_' + timestep + '.txt','') not in Basins:
        Basins.append(each.replace('_' + variable + '_' + timestep + '.txt',''))
print Basins
dss_dic = {}

for Basin in Basins:
    print 'Processing: ' + Basin
    usgstxt = usgs_files + Basin + '_' + variable + '_' + timestep + '.txt'
    
    CSV_file = outputpath + Basin.upper() + '_' + variable + '_' + timestep + '.csv'
    CSV_file_write = open(CSV_file, 'w')
    CSV_file_write.write('Location Names,' + Basin.upper() + '\n')
    CSV_file_write.write('Location Ids,' + Basin.upper() + '\n')
    CSV_file_write.write('Time,' + unit_label[variable] + '\n')
        
    if Basin + '_' + variable + '_' + timestep + '.txt' in os.listdir(usgs_files):
        print 'Processing ' + Basin + '...'
        usgstxt_read = open(usgstxt, 'r')
        
        for line in usgstxt_read:
            if '<!DOCTYPE html>' in line:           # some downloaded files only contain html from nonexistant gage site -> ignore file
                print '!!! Bad data file -> ignoring ' + Basin + '_' + variable + '_' + timestep + '.txt'
                CSV_file_write.close()
                os.remove(CSV_file)
                break
            if line[0] != '#':                      # ignore header lines
                if 'agency_cd' in line:             # find the column with flow data (not the same column for all locations)
                    row = line.split('\t')
                    
                    if any('_' + var_code[variable] in j for j in row) == True: # check that flow/stg data is in file (usgs code for streamflow: 00060; stage: 00065)
                        for i, s in enumerate(row):
                            if '_' + var_code[variable] in s and 'cd' not in s: # 'cd' variable is the data quality marker column
                                flow_index = i
                    else:
                        print '!!! Can not find data column id (' + variable + ' - ' + var_code[variable] + ')...'
                        CSV_file_write.close()
                        os.remove(CSV_file)
                        break # break file loop if flow data not available
                            
                if line[:4] == 'USGS':    #find data lines with mention of USGS to note data row
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
                    #CSV_file_write.write(str(date) + '00' + ',' + flow + '\n')
                    if timestep == 'inst':
                        inst_date = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
                        if flow == 'Ice' or flow == 'Ssn' or flow == 'Eqp' or flow == '' or flow == 'Rat':
                            CSV_file_write.write(inst_date + ',' + '-999.0' + '\n')
                        else:
                            CSV_file_write.write(inst_date + ',' + str(float(flow)) + '\n')  
                            if dss_csv == 'on':
                                if inst_date not in dss_dic:
                                    dss_dic[inst_date] = {}
                                dss_dic[inst_date][Basin]=str(float(flow))
                    if timestep == 'daily':
                        inst_date = year + '-' + month + '-' + day
                        if flow == 'Ice' or flow == 'Ssn' or flow == 'Eqp' or flow == '' or flow == 'Rat':
                            CSV_file_write.write(inst_date + ',' + '-999.0' + '\n')
                        else:
                            CSV_file_write.write(inst_date + ',' + str(float(flow)) + '\n')    
                            if dss_csv == 'on':
                                if inst_date not in dss_dic:
                                    dss_dic[inst_date] = {}
                                dss_dic[inst_date][Basin]=str(float(flow))

        usgstxt_read.close()
    else:
        print Basin + ':' + variable + '_' + timestep + '.txt file missing...'
    CSV_file_write.close()

if dss_csv == 'on':
    print 'Writing to combined dss csv...'
    combine_csv = open(dss_path + os.sep + variable + '_' + timestep + '_merged_for_dss.csv','w')
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
