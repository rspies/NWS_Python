#_calculate_basin_ssurgo_summary.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: calculates basin % soil class from .txt files output from ArcGIS gridded SSURGO data

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
RFC = 'WGRFC'
#FOLDER PATH OF gSSURGO .xls DATA FILES
csv_folderPath = r'P:\\NWS\\GIS\\WGRFC\\SSURGO\\data_files\\'
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = r'P:\\NWS\\GIS\\WGRFC\\SSURGO\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'

gssurgo_file = open(output_folderPath + '_' + RFC + '_SSURGO_Summary.csv', 'w')
gssurgo_file.write('Basin,' + '%A,' + '%B,' + '%C,' + '%D,' + '\n')

#loop through gSSURGO .xls files in folderPath
for filename in glob.glob(os.path.join(csv_folderPath, "*.csv")):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('_ssurgo.csv', '')
    #print name

    txt_file = open(filename, 'r')

    #csv_file = open(r'P:\\NWS\\GIS\\NERFC\\APriori\\temp.csv', 'w')
    csv_file = open(output_folderPath + 'temp.csv', 'w')
    
    grid = []
    
    for line in txt_file:
        #print line
        csv_file.write(line)

    csv_file.close()
    txt_file.close()

    csv_file = open(output_folderPath + 'temp.csv')
    
    data_file = csv.reader(csv_file, delimiter = ',')
    data_file.next()

    A = []
    B = []
    C = []
    D = []

    Count = []

    #GET THE RASTER GRID COUNT OF EACH SOIL TYPE
    for row in data_file:
        soil = str(row[4])
        count = float(row[2])
        if soil == 'A' or soil == 'A/D':
            A.append(count)
            Count.append(count)
        if soil == 'B' or soil == 'B/D':
            B.append(count)
            Count.append(count)
        if soil == 'C' or soil == 'C/D':
            C.append(count)
            Count.append(count)
        if soil == 'D' or soil == 'D/D':
            D.append(count)
            Count.append(count)

    #SUM THE SOIL TYPE GRID COUNTS
    A_sum = numpy.sum(A)
    B_sum = numpy.sum(B)
    C_sum = numpy.sum(C)
    D_sum = numpy.sum(D)
    
    Count_sum = numpy.sum(Count)
    
    #CALCULATE PERCENT OF EACH SOIL TYPE
    A_percent = float(A_sum/Count_sum*100)
    B_percent = float(B_sum/Count_sum*100)
    C_percent = float(C_sum/Count_sum*100)
    D_percent = float(D_sum/Count_sum*100)
    
    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
    gssurgo_file.write(name + ',' + str(A_percent) + ',' + str(B_percent) + ',' + str(C_percent) + ',' + str(D_percent) + '\n')

    csv_file.close()  
gssurgo_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
print 'gssurgo Summary File is', gssurgo_file
raw_input('Press Enter to continue...')
