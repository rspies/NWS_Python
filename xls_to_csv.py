# xls_to_csv.py
# 7/29/2014
# Ryan Spies (ryan.spies@amec.com)
# Description: converts all .xls and .xlsx files in the current directory to
# .csv files
# Warning: script does not explicitly account for excel date format
# refer to python module xlrd to handle excel dates in python

import xlrd
import csv
import os

path = os.getcwd()
xls_files = os.listdir(path)
xls_files = ['BOOT1_DailyResData.xlsx']
for each in xls_files:
    if each[-4:] == '.xls' or each[-4:] == 'xlsx':
        print each
        wb = xlrd.open_workbook(path + '\\' + each)
        sh = wb.sheet_by_name('Sheet1')
        your_csv_file = open(path + '\\' + each[:5] + '.csv', 'wb')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
        
        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        
        your_csv_file.close()
print 'Completed!!'