#_merge_basin_prism_data.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: merges prism .csv data output from ArcGIS model builder

#import script modules
import glob
import os
import re

import numpy
import csv

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC
RFC = 'MBRFC'
#FOLDER PATH OF .csv DATA FILES
csv_folderPath = r'P:\\NWS\\GIS\\MBRFC\\PRISM\\Model_Builder_Output\\tmin\\'
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = r'P:\\NWS\\GIS\\MBRFC\\PRISM\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'

prism_file = open(output_folderPath + '_' + RFC + '_1981_2010_tmin_Summary.csv', 'w')
prism_file.write('Basin,' + 'tmin,' + '\n')

#loop through gSSURGO .xls files in folderPath
for filename in glob.glob(os.path.join(csv_folderPath, "*.csv")):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('_prism.csv', '')
    #print name

    txt_file = open(filename, 'r')

    #csv_file = open(r'P:\\NWS\\GIS\\NERFC\\APriori\\temp.csv', 'w')
    csv_file = open(output_folderPath + 'temp.csv', 'w')
    
    for line in txt_file:
        #print line
        csv_file.write(line)

    csv_file.close()
    txt_file.close()

    csv_file = open(output_folderPath + 'temp.csv')
    
    data_file = csv.reader(csv_file, delimiter = ',')
    data_file.next()

    for row in data_file:
        value = float(row[2])
    
    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
    prism_file.write(name + ',' + str(value) + '\n')

    csv_file.close()  
prism_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
print 'prism Summary File is', prism_file
raw_input('Press Enter to continue...')
