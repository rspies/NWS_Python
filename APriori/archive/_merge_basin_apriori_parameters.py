#_merge_basin_apriori_parameters.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: merges SACSMA a priori parameters from .txt files output from ArcGIS Model Builder

#import script modules
import glob
import os
import re

import numpy
import csv

####################################################################
#USER INPUT SECTION
####################################################################
#BASIN NAME
Basin = 'CRKT1'
#FOLDER PATH OF APRIORI .TXT FILES FROM MODEL BUILDER
folderPath = r'P:\\NWS\\GIS\\LMRFC\\APriori\\'+ Basin + '\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'

apriori_file = open(folderPath + Basin + '_apriori_parameters.csv', 'w')
apriori_file.write('Parameter,' + 'Mean,' + 'Max,' + 'Min,' + '\n')

#SAC-SMA SECTION--------------------------------------------------------------
#loop through SACSMA files in folderPath
for filename in glob.glob(os.path.join(folderPath, "*.txt")):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('.txt', '')
    #print name

    txt_file = open(filename, 'r')

    #csv_file = open(r'P:\\NWS\\GIS\\NERFC\\APriori\\temp.csv', 'w')
    csv_file = open(folderPath + 'temp.csv', 'w')

    #csv_file.write('BASIN, MEAN, MIN, MAX,' + '\n')
    
    grid = []
    
    for line in txt_file:
        #print line
        csv_file.write(line)

    csv_file.close()
    txt_file.close()

    csv_file = open(folderPath + 'temp.csv')
    
    data_file = csv.reader(csv_file, delimiter = ',')
    data_file.next()

    grid = []
    
    for row in data_file:
        grid_code = float(row[2])
        grid.append(grid_code)

    maximum = numpy.max(grid)
    minimum = numpy.min(grid)
    mean = numpy.mean(grid)

    #print 'grid is', grid
    #print 'max is', maximum
    #print 'min is', minimum
    #print 'mean is', mean

    apriori_file.write(name + ',' + str(mean) + ',' + str(maximum) + ',' + str(minimum) + ',' + '\n')

apriori_file.close()

csv_file.close()
os.remove(folderPath + 'temp.csv')

print 'Script Complete'
print 'A priori parameters in', apriori_file
raw_input('Press Enter to continue...')
