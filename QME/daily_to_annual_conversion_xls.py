# daily_to_annual_resdata.py
# 8/11/2014
# Ryan Spies (ryan.spies@amec.com)
# Description: calculates a WY summary of QME data in an excel format with daily
# data -> outputs a water year mean daily flow table

import xlrd
import os
import datetime
import csv
import numpy as np

###################### User Input ##########################################
############################################################################
path = os.getcwd()
rfc = 'SERFC'
# directory with basin .xlsx files (daily data):
path_daily = 'P:\\NWS\\Calibration_NWS\\' + rfc + '\\data\\daily_discharge'
xls_files = os.listdir(path_daily) 
#xls_files = ['ezbt1-stg-q-2002-2012.xlsx']  # use this to run a specific file(s)
# output directory:
out_dir = 'P:\\NWS\\Calibration_NWS\\' + rfc + '\\data\\annual_discharge'
############################################################################
################### End User Input #########################################

print xls_files

## AF to cfs per day
af_cfs = 43560.0/(24*60*60)

for each in xls_files:
    if each[-4:] == '.xls' or each[-4:] == 'xlsx':
        print each
        wb = xlrd.open_workbook(path_daily + '\\' + each)
        worksheet = wb.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        curr_row = -1
        
        wy_data= {}       
        print 'Interating through the each row...'
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            if curr_row == 1: # 1st row of data should be the first line after header
                start = xlrd.xldate_as_tuple(worksheet.cell_value(curr_row, 0),0)
                start_date = datetime.datetime(start[0],start[1],start[2],start[3])
                print 'Start date: ' + str(start_date)
            if curr_row >= 1:  # 1st row of data should be the first line after header
                date_xls = xlrd.xldate_as_tuple(worksheet.cell_value(curr_row, 0),0)
                date = datetime.datetime(date_xls[0],date_xls[1],date_xls[2],date_xls[3])
                outflow = worksheet.cell_value(curr_row, 2)
                if outflow < 0:
                    print 'Warning... negative outflow' 
                    
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
                else:
                    print outflow
                    
        csvfile = open(out_dir + '\\' + each[:5] + '_WY_QME_summary.csv','wb')
        writer = csv.writer(csvfile)
        writer.writerow(['WY', 'Mean Daily QME (cfs)', 'daily count'])
        # write a summary of the data to a basin specific csv file
        for each_wy in wy_data:
            wy_out = np.sum(wy_data[each_wy])
            num_values = len(wy_data[each_wy])
            wy_start = datetime.datetime(each_wy-1,10,1) # start date of WY 10/1
            wy_end = datetime.datetime(each_wy,9,30) # end date of WY 9/30
            total_out_cfsd = (wy_out/num_values)
            writer.writerow([each_wy,total_out_cfsd,num_values])
            
        csvfile.close()
print 'Completed!!'
