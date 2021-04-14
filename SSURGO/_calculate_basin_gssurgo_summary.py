#_calculate_basin_ssurgo_summary.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: calculates basin % soil class from .txt files output from ArcGIS gridded SSURGO data

#import script modules
import glob
import os
import numpy
import csv
os.chdir("../..")
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC
RFC = 'WGRFC_2021'
fx_group = '' # set to blank '' if not using fx_groups
#FOLDER PATH OF gSSURGO .xls DATA FILES
if fx_group != '':
    csv_folderPath = maindir + '\\GIS\\'+RFC[:5] + os.sep + RFC+'\\SSURGO\\data_files\\' + fx_group + '\\'
else:
    csv_folderPath = 'E:\\TWDB_WGRFC\\gSSURGO\\data_files\\'
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath ='E:\\TWDB_WGRFC\\gSSURGO\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'
if fx_group == '':
    gssurgo_file = open(output_folderPath + RFC + '_SSURGO_Summary.csv', 'w')
else:
    gssurgo_file = open(output_folderPath + RFC[:5] + '_' + fx_group + '_' + RFC[-6:] + '_SSURGO_Summary.csv', 'w')
gssurgo_file.write('Basin,' + 'A,' + 'B,' + 'C,' + 'D,' + 'A/D,' + 'B/D,' + 'C/D,' + '\n')

#loop through gSSURGO .xls files in folderPath
for filename in glob.glob(os.path.join(csv_folderPath, "*.csv")):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    ch5id = name.split('_')[0]
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
    #data_file.next()

    A = []
    B = []
    C = []
    D = []
    AD = []
    BD = []
    CD = []

    Count = []

    #GET THE RASTER GRID COUNT OF EACH SOIL TYPE
    for row in data_file:
        if 'OID' in row:
            hydgrp = row.index('HYDGRPDCD')
            cntcol = row.index('COUNT')
        else:
            soil = str(row[hydgrp])
            count = float(row[cntcol])
            if soil == 'A':
                A.append(count)
                Count.append(count)
            if soil == 'B':
                B.append(count)
                Count.append(count)
            if soil == 'C':
                C.append(count)
                Count.append(count)
            if soil == 'D':
                D.append(count)
                Count.append(count)
            if soil == 'A/D':
                AD.append(count)
                Count.append(count)
            if soil == 'B/D':
                BD.append(count)
                Count.append(count)
            if soil == 'C/D':
                CD.append(count)
                Count.append(count)

    #SUM THE SOIL TYPE GRID COUNTS
    A_sum = numpy.sum(A)
    B_sum = numpy.sum(B)
    C_sum = numpy.sum(C)
    D_sum = numpy.sum(D)
    AD_sum = numpy.sum(AD)
    BD_sum = numpy.sum(BD)
    CD_sum = numpy.sum(CD)
    
    Count_sum = numpy.sum(Count)
    
    #CALCULATE PERCENT OF EACH SOIL TYPE
    A_percent = float(A_sum/Count_sum*100)
    B_percent = float(B_sum/Count_sum*100)
    C_percent = float(C_sum/Count_sum*100)
    D_percent = float(D_sum/Count_sum*100)
    AD_percent = float(AD_sum/Count_sum*100)
    BD_percent = float(BD_sum/Count_sum*100)
    CD_percent = float(CD_sum/Count_sum*100)
    
    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
    gssurgo_file.write(ch5id + ',' + str(A_percent) + ',' + str(B_percent) + ',' + str(C_percent) + ',' + str(D_percent) + ',' + str(AD_percent) + ',' + str(BD_percent) + ',' + str(CD_percent) + '\n')

    csv_file.close()  
gssurgo_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
