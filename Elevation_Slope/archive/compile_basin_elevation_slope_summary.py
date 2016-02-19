#compile_basin_elevation_slope_summary.py
#Cody Moser/Ryan Spies
#cody.moser@amec.com
#AMEC
#Description: compiles basin elevation and slope data
#from .xls files output from ArcGIS Model Builder

#import script modules
import glob
import os
import csv
import xlrd

#USER INPUT SECTION----------------------------------------------------------------
#RFC
RFC = 'APRFC'
#FOLDER PATH OF ELEVATION/SLOPE .xls DATA FILES
input_directory = 'P:\\NWS\\GIS\\'+RFC+'\\Elevation_Slope\\Stats_out\\'
#FOLDER PATH OF OUTPUT SUMMARY FILE - Must be different than input_directory
output_folderPath = 'P:\\NWS\\GIS\\'+RFC+'\\Elevation_Slope\\'
#END USER INPUT SECTION------------------------------------------------------------

print 'Script is Running...'

#convert .xls files to .csv files
files = os.listdir(input_directory)
for filename in files:
    if filename[-3:] == 'xls':
        print filename
        name = filename.replace('.xls', '') 
        
    workbook = xlrd.open_workbook(input_directory + filename)
    sheet = workbook.sheet_by_name(name)
    output_csv_file = open(input_directory + name + '.csv', 'wb')
    wr = csv.writer(output_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sheet.nrows):
        wr.writerow(sheet.row_values(rownum))

    output_csv_file.close()

#create summary output file that data will be written to
summary_file = open(output_folderPath + RFC + '_Elevation_Slope_Summary.csv', 'wb')
csvfile = csv.writer(summary_file)
csvfile.writerow( ('Basin','Min Elev (ft)','Max Elev (ft)','Mean Elev (ft)','Mean Slope (%)') )

# creat a list of all the basins in the directory
basin_files = os.listdir(input_directory)
basins = []
for each in basin_files:
    if each[:5] not in basins:
        if each[:4] != 'info': # ignore the info directory
            basins.append(each[:5])

for basin in basins:
    print basin
    elev_file = open(input_directory + basin + '_elevation_stats_cm.csv', 'rb')
    slope_file = open(input_directory + basin + '_mean_slope_percent.csv', 'rb')
    elev_read = csv.reader(elev_file)
    slope_read = csv.reader(slope_file)
    row_num = 0
    for row in elev_read:
        if row_num == 1:
            min_elev = float(row[2]) / 30.48    # convert cm to ft
            mean_elev = float(row[3]) / 30.48   # convert cm to ft
            max_elev = float(row[4]) / 30.48    # convert cm to ft
        row_num += 1
    row_num = 0
    for row in slope_read:
        if row_num == 1:
            mean_slope = float(row[2].rstrip())
        row_num += 1
            
    csvfile.writerow((basin,min_elev,max_elev,mean_elev,mean_slope))
    
    elev_file.close(); slope_file.close()
summary_file.close()

print 'Script Complete'
