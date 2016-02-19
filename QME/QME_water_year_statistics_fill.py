# QME_water_year_statistics_fill.py
# 7/13/2015
# Ryan Spies (rspies@lynkertech.com)
# Description: calculates a WY summary of QME data from NWS datacard data
# and outputs a water year mean daily flow table
# This version also fills missing winter data with a constant value (determined
# by visual analysis in CHPS) -> used in MBRFC-FY15

import glob
import os
import datetime
import csv
import numpy as np
os.chdir("../..")
maindir = os.getcwd()

###################### User Input ##########################################
############################################################################
path = os.getcwd()
rfc = 'MBRFC_FY2015'
# directory with basin .xlsx files (daily data):
qme_dir = maindir + '\\Calibration_NWS\\' + rfc + '\\DataToLynker_fy15\\qme\\calb_basins\\'
#xls_files = ['ezbt1-stg-q-2002-2012.xlsx']  # use this to run a specific file(s)
# output directory:
out_dir = maindir + '\\Calibration_NWS\\' + rfc + '\\DataToLynker_fy15\\qme\\WY_summaries_fill\\'
############################################################################
################### End User Input #########################################
basins_fill = {'TSFM8':53,'NFSM8':176,'SSNM8':92} # <-feet, meters: {'TSFM8':1.5,'NFSM8':5.0,'SSNM8':2.6}

## AF to cfs per day
#af_cfs = 43560.0/(24*60*60)
datacard_files = glob.glob(qme_dir+'*.txt') 

for each in datacard_files:     
    wy_data= {}; start_row = 0; wy_fill = {}
    if os.path.basename(each).split('_')[0] in basins_fill:
        print 'Processing: ' + (os.path.basename(each)).split('_')[0] + '...'
        open_file = open(each,'r')
        for line in open_file:
            if line[0] != '$':
                start_row += 1
                if start_row > 2: # skip two header lines (without '$')
                    parse_month =int((line[:20].split()[1])[:-2])
                    parse_year = int((line[:20].split()[1])[-2:])
                    if parse_year <= 15:
                        parse_year = parse_year + 2000
                    else:
                        parse_year = parse_year + 1900
                    parse_day = int((line[:20].split()[2]))
                    date = datetime.datetime(parse_year,parse_month,parse_day)
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
                    elif date.month >= 10 and outflow < 0: 
                        outflow = basins_fill[os.path.basename(each).split('_')[0]]
                        if int(date.year)+1 in wy_data:
                            wy_data[date.year+1].append(outflow)
                        else:
                            wy_data[date.year+1] = [outflow]
                        if int(date.year)+1 in wy_fill:
                            wy_fill[date.year+1].append(outflow)
                        else:
                            wy_fill[date.year+1] = [outflow]
                    elif date.month < 10 and outflow >= 0:
                        if int(date.year) in wy_data:
                            wy_data[date.year].append(outflow)
                        else:
                            wy_data[date.year] = [outflow]
                    elif date.month < 5 and outflow < 0:
                        outflow = basins_fill[os.path.basename(each).split('_')[0]]
                        if int(date.year) in wy_data:
                            wy_data[date.year].append(outflow)
                        else:
                            wy_data[date.year] = [outflow]
                        if int(date.year) in wy_fill:
                            wy_fill[date.year].append(outflow)
                        else:
                            wy_fill[date.year] = [outflow]
                            
        open_file.close()            
        csvfile = open(out_dir + '\\' + (os.path.basename(each)).split('_')[0] + '_WY_QME_summary_fill.csv','wb')
        writer = csv.writer(csvfile)
        writer.writerow(['USGS gage id:',gage])
        writer.writerow(['WY', 'Mean Daily QME (cfs)', 'Mean Daily QME (cms)', 'daily count','fill count'])
        # write a summary of the data to a basin specific csv file
        for each_wy in wy_data:
            wy_out = np.sum(wy_data[each_wy])
            num_values = len(wy_data[each_wy])
            if each_wy in wy_fill:
                num_fill = len(wy_fill[each_wy])
            else:
                num_fill = 0
            wy_start = datetime.datetime(each_wy-1,10,1) # start date of WY 10/1
            wy_end = datetime.datetime(each_wy,9,30) # end date of WY 9/30
            total_out_cfsd = (wy_out/num_values)
            total_out_cmsd = total_out_cfsd/35.3147
            if num_fill < num_values:
                writer.writerow([each_wy,total_out_cfsd,total_out_cmsd,num_values,num_fill])
            
        csvfile.close()
print 'Completed!!'
