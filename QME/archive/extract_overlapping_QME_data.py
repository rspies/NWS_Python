# extract_overlapping_QME_data.py
# by Cody Moser (10/13/2014)
# cody.moser@amec.com
# AMEC
# Description: extracts overlapping QME (non-missing) data
#from two time series in a .csv file

#import script modules
import os
import csv

#USER INPUT SECTION
input_csv = r'P:\\NWS\\MBRFC\\QME\\MUSM8\\MUSM8_MSBM8_Monthly_QME.csv'
output_csv = r'P:\\NWS\\MBRFC\\QME\\MUSM8\\MUSM8_MSBM8_Monthly_QME_Overlap.csv'
#END USER INPUT SECTION

output_file = open(output_csv, 'w')
input_file = open(input_csv, 'r')

for line in input_file:
    #line.replace('/', '-')
    if "GMT" in line:
        output_file.write(line)
    if "QME" in line:
        output_file.write(line)
    if "-999" not in line:
        output_file.write(line)

input_file.close()
output_file.close()

print 'Script Complete'
