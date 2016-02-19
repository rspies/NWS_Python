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
csv_folderPath = r'P:\\NWS\\GIS\\MBRFC\\Elevation_Slope\\Model_Builder_Output\\'
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = r'P:\\NWS\\GIS\\MBRFC\\Elevation_Slope\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'

prism_file = open(output_folderPath + '_' + RFC + '_Elevation_Summary.csv', 'w')
prism_file.write('Basin,' + 'Minimum (ft),' + 'Mean (ft),' + 'Maximum (ft),' + '\n')

#loop through gSSURGO .xls files in folderPath
for filename in glob.glob(os.path.join(csv_folderPath, "*.csv")):
    #print filename

    #Define output file name
    name_full = str(os.path.basename(filename)[:])
    name_basin = name_full.replace('_elevation_stats_cm.csv', '')
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

    if "cm" in name_full:
        for row in data_file:
            minimum_cm = float(row[2])
            mean_cm = float(row[3])
            maximum_cm = float(row[4])

            minimum_ft = minimum_cm*0.0328084
            mean_ft = mean_cm*0.0328084
            maximum_ft = maximum_cm*0.0328084
    
    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
            prism_file.write(name_basin + ',' + str(minimum_ft) + ',' + str(mean_ft) + ',' + str(maximum_ft) + '\n')

    csv_file.close()  
prism_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
print 'prism Summary File is', prism_file
raw_input('Press Enter to continue...')
