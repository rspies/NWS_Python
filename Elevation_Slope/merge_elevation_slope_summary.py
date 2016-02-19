# merge_elevation_slope_summary.py
# by Ryan Spies (7/22/2014)
# ryan.spies@amec.com
# AMEC
# Description: merges elevation and slope data from individual basin .csv files 
# output from ArcGIS Model Builder or automated python script: P:\NWS\GIS\Models\python\extract_basin_DEM_statistics.py

#import script modules
import os
import csv
os.chdir("../..")
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
# OPTIONAL -> run all basins within an RFC directory
RFC = 'NCRFC_FY2016'
#FOLDER PATH OF ELEVATION AND SLOPE .CSV FILES FROM MODEL BUILDER OR PYTHON SCRIPT
file_dir = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\Stats_Out\\'
summary_csv = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\'
non_hydro1k_tasks = ['SERFC_FY14'] # identify tasks that DON'T use the hydro1k DEM (e.g. NHD plus 30m DEM)
####################################################################
#END USER INPUT SECTION
####################################################################

new_file = open(summary_csv + RFC + '_elev_slope_summary.csv', 'wb')
csvfile = csv.writer(new_file)
if RFC in non_hydro1k_tasks:
    new_file.write('Units converted from ?cm? to feet\n')
else:
    new_file.write('Units converted from meters to ft\n')
csvfile.writerow( ('Basin','Min Elev (ft)','Max Elev (ft)','Mean Elev (ft)','Mean Slope (%)') )

# creat a list of all the basins in the directory
basin_files = os.listdir(file_dir)
basins = []
for each in basin_files:
    if each.split('_')[0] not in basins:
        if each[:4] != 'info': # ignore the info directory
            basins.append(each.split('_')[0])

print 'Script is Running...'
for basin in basins:
    print basin
    elev_file = open(file_dir + basin + '_elevation_stats_cm.csv', 'rb')
    slope_file = open(file_dir + basin + '_mean_slope_percent.csv', 'rb')
    elev_read = csv.reader(elev_file)
    slope_read = csv.reader(slope_file)
    row_num = 0
    for row in elev_read:
        if RFC in non_hydro1k_tasks: # most RFC's using NHD Plus v. 1 (30m resolution with units in cm)
            if row_num == 1:
                min_elev = float(row[3]) / 30.48    # convert cm to ft (NHD Plus DEM)
                mean_elev = float(row[4]) / 30.48   # convert cm to ft (NHD Plus DEM)
                max_elev = float(row[5]) / 30.48    # convert cm to ft (NHD Plus DEM)
            row_num += 1
        else: # RFC using the HYDRO1K (1km resolution with units in meters)
            if row_num == 1:
                min_elev = float(row[3]) * 3.28084    # convert m to ft (HYDRO1K DEM)
                mean_elev = float(row[4]) * 3.28084   # convert m to ft (HYDRO1K DEM)
                max_elev = float(row[5]) * 3.28084    # convert m to ft (HYDRO1K DEM)
            row_num += 1
    row_num = 0
    for row in slope_read:
        if row_num == 1:
            if RFC in non_hydro1k_tasks:
                mean_slope = float(row[2].rstrip())
            else: # RFC uses the HYDRO1K (1km resolution with units in meters)
                mean_slope = float(row[2].rstrip()) * 100
        row_num += 1
            
    csvfile.writerow((basin,min_elev,max_elev,mean_elev,mean_slope))
    
    elev_file.close(); slope_file.close()
new_file.close()
print 'Script Complete'
