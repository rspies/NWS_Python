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
folderPath = 'P:\\NWS\\QIN\\NERFC\\ANDM3\\'
Basin = 'ANDM3'
Basin_long = 'ANDM3MER'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'
#print folderPath

historical_rdb_file = folderPath + Basin + '_historical_rdb.rdb'
historical_csv_file = folderPath + Basin + '_historical_csv.csv'

recent_txt_file = folderPath + Basin + '_recent.txt'
recent_csv_file = folderPath + Basin + '_recent_csv.csv'

QIN_file = folderPath + Basin + '_QIN.csv'

historical_rdb_file_read = open(historical_rdb_file, 'r')
historical_csv_file_write = open(historical_csv_file, 'w')

recent_txt_file_read = open(recent_txt_file, 'r')
recent_csv_file_write = open(recent_csv_file, 'w')

QIN_file_write = open(QIN_file, 'w')

for line in historical_rdb_file_read:
    if 'EDT' in line or 'EST' in line:
        line = line
        line = line.replace('\t', ',')
        historical_csv_file_write.write(line)

historical_rdb_file_read.close()
historical_csv_file_write.close()

for line in recent_txt_file_read:
    if 'EDT' in line or 'EST' in line:
        line = line
        line = line.replace('\t', ',')
        line = line.replace('-', '')
        line = line.replace(' ', '')
        line = line.replace(':', '')
        
        recent_csv_file_write.write(line)

recent_txt_file_read.close()
recent_csv_file_write.close()

historical_csv_file = folderPath + Basin + '_historical_csv.csv'
historical_csv_file_read = open(historical_csv_file, 'r')

data_file = csv.reader(historical_csv_file_read, delimiter = ',')

QIN_file_write.write('Location Names,' + Basin + '\n')
QIN_file_write.write('Location Ids,' + Basin + '\n')
QIN_file_write.write('Time,' + 'QIN [cfs]' + '\n')

for row in data_file:
    date = str(row[1])
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    minute = date[10:12]
    second = date[12:14]
    flow = str(row[5])
    if flow == 'Ice':
        QIN_file_write.write(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + ',' + '-999.0' + '\n')
    else:
        QIN_file_write.write(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + ',' + flow + '\n')


print 'year is', year
print 'month is', month
print 'day is', day
print 'hour is', hour
print 'minute is', minute
print 'second is', second


historical_csv_file_read.close()

recent_csv_file = folderPath + Basin + '_recent_csv.csv'
recent_csv_file_read = open(recent_csv_file, 'r')

data_file = csv.reader(recent_csv_file_read, delimiter = ',')
data_file.next()

for row in data_file:
    date = str(row[2])
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    minute = date[10:12]
    second = '00'
    flow = str(row[4])
    #QIN_file_write.write(str(date) + '00' + ',' + flow + '\n')
    if flow == 'Ice':
        QIN_file_write.write(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + ',' + '-999.0' + '\n')
    else:
        QIN_file_write.write(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + ',' + flow + '\n')

print 'year is', year
print 'month is', month
print 'day is', day
print 'hour is', hour
print 'minute is', minute
print 'second is', second

recent_csv_file_read.close()

QIN_file_write.close()












os.remove(folderPath + Basin + '_historical_csv.csv')
os.remove(folderPath + Basin + '_recent_csv.csv')

print 'Script Complete'
print 'QIN File is', QIN_file
raw_input('Press Enter to continue...')
