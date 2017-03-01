# QME_water_year_statistics.py
# 6/1/2015
# Ryan Spies (rspies@lynkertech.com)
# Description: calculates a WY summary of QME data from NWS datacard data
# and outputs a water year mean daily flow table

import os
import datetime
import csv
import numpy as np
os.chdir("../..")
maindir = os.getcwd()

###################### User Input ##########################################
############################################################################
path = os.getcwd()
rfc = 'APRFC_FY2017'
# directory with basin .xlsx files (daily data):
variable = 'QME' # QME or MAP
datacard_dir = maindir + '\\Calibration_NWS\\' + rfc[:5] + os.sep + rfc + '\\datacards\\QME\\QME_Lynker_download\\'
# output directory:
out_dir = maindir + '\\Calibration_NWS\\' + rfc[:5] + os.sep + rfc + '\\datacards\\WY_summary\\'
############################################################################
################### End User Input #########################################
summary_file = open(out_dir + os.sep + rfc + '_' + variable + '_summary.csv','w')
summary_file.write(',')
years = range(1948,2016)

## AF to cfs per day
#af_cfs = 43560.0/(24*60*60)
datacard_files = os.listdir(datacard_dir) 
summary_data = {}

for each in datacard_files:     
    wy_data= {}; start_row = 0
    location = (os.path.basename(each)).split('_')[0].split('.')[0]
    print 'Processing: ' + location + '...'
    
    open_file = open(datacard_dir + os.sep + each,'r')
    for line in open_file:
        if line[0] != '$':
            start_row += 1
            if start_row > 2: # skip two header lines (without '$')
                if len(line[:20].split()[-2]) > 1:
                    parse_month =int((line[:20].split()[-2])[:-2])
                    parse_year = int((line[:20].split()[-2])[-2:])
                else: # catch some datacard formats with space between mm yy starting in 2000
                    parse_month =int((line[:20].split()[-3]))
                    parse_year = int((line[:20].split()[-2]))
                if parse_year <= 16:
                    parse_year = parse_year + 2000
                else:
                    parse_year = parse_year + 1900
                parse_day = int((line[:20].split()[-1]))
                date = datetime.datetime(parse_year,parse_month,parse_day)
                
                ########### QME ############
                if variable == 'QME':
                    outflow = float(line.split()[3])
                    if start_row == 3: # 1st row of data should be the first line after header
                        start_date = date
                        gage = str(line.split()[0])
                        print 'Start date: ' + str(start_date)
                
                    # add data to the dictionary with the water year reference
                    if date.month >= 10 and outflow >= 0:
                        if int(date.year)+1 in wy_data:
                            wy_data[date.year+1].append(outflow)
                        else:
                            wy_data[date.year+1] = [outflow]
                    elif date.month < 10 and outflow >= 0:
                        if int(date.year) in wy_data:
                            wy_data[date.year].append(outflow)
                        else:
                            wy_data[date.year] = [outflow] 
                        
                ########### MAP ############
                if variable == 'MAP':
                    all_map = line[20:].split() # ususally the first column is blank for MAP (usgs gage)
                    
                    # add data to the dictionary with the water year reference
                    if date.month >= 10 and all_map >= 0:
                        if int(date.year)+1 in wy_data:
                            for each_map in all_map:
                                wy_data[date.year+1].append(float(each_map))
                        else:
                            for each_map in all_map:
                                wy_data[date.year+1] = [float(each_map)]
                    elif date.month < 10 and all_map >= 0:
                        if int(date.year) in wy_data:
                            for each_map in all_map:
                                wy_data[date.year].append(float(each_map))
                        else:
                            for each_map in all_map:
                                wy_data[date.year] = [float(each_map)]   
                        
    open_file.close()            
    csvfile = open(out_dir + '\\basin_data\\' + (os.path.basename(each)).split('_')[0].split('.')[0] + '_WY_' + variable +'_summary.csv','wb')
    writer = csv.writer(csvfile)
    if variable == 'QME':
        writer.writerow(['USGS gage id:',gage])
        writer.writerow(['WY', 'Mean Daily QME (cfs)', 'Mean Daily QME (cms)', 'daily count'])
    if variable == 'MAP':
        writer.writerow(['WY', 'MAP_inches', 'data count'])
        
    # write a summary of the data to a basin specific csv file
    for each_wy in wy_data:
        summary_year = {}
        wy_out = np.sum(wy_data[each_wy])
        num_values = len(wy_data[each_wy])
        wy_start = datetime.datetime(each_wy-1,10,1) # start date of WY 10/1
        wy_end = datetime.datetime(each_wy,9,30) # end date of WY 9/30
        
        if variable == 'QME':
            total_out_cfsd = (wy_out/num_values)
            total_out_cmsd = total_out_cfsd/35.3147
            if num_values >= 300: #only calculate WY values for years with more than 300 daily data points
                writer.writerow([each_wy,total_out_cfsd,total_out_cmsd,num_values])
                summary_year[each_wy]=[total_out_cmsd]
                if location in summary_data:
                    summary_data[location].update(summary_year)
                else:
                    summary_data[location] = summary_year
            else:
                writer.writerow([each_wy,"n/a","n/a",num_values])
            next_wy = int(each_wy)
            print next_wy
            while (next_wy+1) not in wy_data:
                if int(next_wy)+1 < 2016: # find missing WY's in data and output to csv 
                    writer.writerow([str(next_wy+1),'n/a','n/a','0'])
                    print 'no data for wy: ' + str(next_wy+1)
                else:
                    break
                next_wy += 1
                
        if variable == 'MAP':
            if num_values >= 1200: #only calculate WY values for years with more than 1200 6-hr data points
                writer.writerow([each_wy,wy_out,num_values])
                summary_year[each_wy]=[wy_out]
                if location in summary_data:
                    summary_data[location].update(summary_year)
                else:
                    summary_data[location] = summary_year
            else:
                writer.writerow([each_wy,"n/a",num_values])
            next_wy = int(each_wy)
            print next_wy
            while (next_wy+1) not in wy_data:
                if int(next_wy)+1 < 2016: # find missing WY's in data and output to csv 
                    writer.writerow([str(next_wy+1),'n/a','n/a','0'])
                    print 'no data for wy: ' + str(next_wy+1)
                else:
                    break
                next_wy += 1
            
    csvfile.close()

### write all data to summary file
if variable == 'QME':
    summary_file.write('Mean Daily QME (cms)\n,')
for loc in summary_data:
    summary_file.write(loc + ',')
summary_file.write('\n')
for year in years:
    summary_file.write(str(year) + ',')
    for loc in summary_data:
        if year in summary_data[loc]:
            summary_file.write(str("%.2f" % summary_data[loc][year][0]) + ',')
        else:
            summary_file.write(',')
    summary_file.write('\n')

summary_file.close()
print 'Completed!!'
