#_create_QIN_timeseries.py
#Cody Moser
#Modified by Ryan Spies (rspies@lynkertech.com)
# Description: creates a QIN time series in .csv format for import into CHPS
# capable of using 2 files from the USGS:
# 1. historical (before Oct 1, 2007) file in .rdb format
# 2. recent (after Oct 1, 2007) file in .txt format
### data retrieval info: http://waterdata.usgs.gov/nwis/?IV_data_availability

#import script modules
import os
import csv
os.chdir("../..")
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
RFC = 'MBRFC_FY2015'
rawdatapath = maindir + '\\Calibration_NWS\\' + RFC + '\\DataToLynker_fy15\\qin\\recent\\'
outputpath = maindir + '\\Calibration_NWS\\' + RFC + '\\DataToLynker_fy15\\qin\\CHPS_import_csv\\'
####################################################################
#END USER INPUT SECTION
####################################################################

Basins = []
for each in os.listdir(rawdatapath):
    if each.split('.')[0] not in Basins:
        Basins.append(each.split('.')[0])
print Basins

for Basin in Basins:
    print 'Processing: ' + Basin
    historical_csv_file = outputpath + Basin + '_historical_csv.csv'
    recent_csv_file = outputpath + Basin + '_recent_csv.csv'
    
    QIN_file = outputpath + Basin + '_QIN.csv'
    QIN_file_write = open(QIN_file, 'w')
    QIN_file_write.write('Location Names,' + Basin + '\n')
    QIN_file_write.write('Location Ids,' + Basin + '\n')
    QIN_file_write.write('Time,' + 'QIN [cfs]' + '\n')
    
    if Basin + '.rdb' in os.listdir(rawdatapath):
        historical_rdb_file_read = open(rawdatapath + Basin + '.rdb', 'r')
        historical_csv_file_write = open(historical_csv_file, 'w')
        for line in historical_rdb_file_read:
            if line[0] != '#':                      #ignore header lines
                if 'DT' in line or 'ST' in line:    #find data lines with mention of time zone
                    line = line
                    line = line.replace('\t', ',')
                    historical_csv_file_write.write(line)
        
        historical_rdb_file_read.close()
        historical_csv_file_write.close()
    else:
        print Basin + ': _.rdb file missing...'
    
    if Basin + '.txt' in os.listdir(rawdatapath):
        recent_txt_file_read = open(rawdatapath + Basin + '.txt', 'r')
        recent_csv_file_write = open(recent_csv_file, 'w')
        for line in recent_txt_file_read:
            if line[0] != '#':                      #ignore header lines
                if 'DT' in line or 'ST' in line:    #find data lines with mention of time zone
                    line = line
                    line = line.replace('\t', ',')
                    line = line.replace('-', '')
                    line = line.replace(' ', '')
                    line = line.replace(':', '')            
                    recent_csv_file_write.write(line)
        
        recent_txt_file_read.close()
        recent_csv_file_write.close()
    else:
        print Basin + ': _recent.txt file missing...'
    
    if Basin + '_historical_csv.csv' in os.listdir(outputpath):
        print 'Processing ' + Basin + '_historical_csv.csv...'
        historical_csv_file_read = open(historical_csv_file, 'r')
        
        data_file = csv.reader(historical_csv_file_read, delimiter = ',')    
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
        
        historical_csv_file_read.close()
        os.remove(outputpath + Basin + '_historical_csv.csv')
    
    if Basin + '_recent_csv.csv' in os.listdir(outputpath):
        print 'Processing ' + Basin + '_recent_csv.csv...'
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
            if flow == 'Ice' or flow == 'Ssn' or flow == 'Eqp':
                QIN_file_write.write(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + ',' + '-999.0' + '\n')
            else:
                QIN_file_write.write(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + ',' + str(float(flow)) + '\n')

        
        recent_csv_file_read.close()
        os.remove(outputpath + Basin + '_recent_csv.csv')
    
    QIN_file_write.close()


print 'Script Complete'
