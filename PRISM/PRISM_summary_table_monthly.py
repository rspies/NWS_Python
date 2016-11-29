#_calculate_basin_nlcd_summary.py
#Ryan Spies
#ryan.spies@amec.com
#AMEC
#Description: creates summary table of PRISM data (converts mm to in)
#from .xls files output from ArcGIS Model Builder 
#7/24/2014 -> modified to also run the script using .csv files (output from python arcpy tool)
#output single .csv

#import script modules
import os
#import xlrd # python module for exel file handling
import csv
import glob
os.chdir("../..")
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC Region
RFC = 'MARFC_FY2017'
fx_group = '' # leave blank if not processing by fx group
variables = ['ppt','tmean','tmax','tmin'] # use temperature: 'tmean','tmax','tmin' or precipitation: 'ppt'

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
basins_overwrite = []

####################################################################
#END USER INPUT SECTION
####################################################################
for variable in variables:
    print variable
    #FOLDER PATH OF PRISM .xls/.csv DATA FILES
    if fx_group != '':
        csv_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\PRISM\\Model_Builder_Output_' + variable + '_month\\' + fx_group + '\\'
    else:
        csv_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\PRISM\\Model_Builder_Output_' + variable + '_month\\'
    #FOLDER PATH OF BASIN SUMMARY PRISM .xls DATA FILES (!Must be different than csv_FolderPath!)
    output_folderPath = maindir + '\\GIS\\'+ RFC[:5] + os.sep + RFC + '\\PRISM\\'
    
    
    units = {'ppt':'inches','tmax':'degrees C','tmin':'degrees C','tmean':'degrees C'}
    
    basin_files = glob.glob(csv_folderPath+'/*.csv') # list all basin .csv files in the above specified directory
    if len(basins_overwrite) != 0:
        basin_files = basins_overwrite # use the basins_overright variable to run only specified basins instead of all RFC basins
    basins = []
    for each in basin_files:
        basename = os.path.basename(each)
        if (basename.split('_'))[0] not in basins:
            basins.append((basename.split('_'))[0].strip('\.'))
    
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    print 'Script is Running...'
    #Define output file name
    if fx_group != '':
        out_file = open(output_folderPath + RFC[:5] + '_' + fx_group + '_' + RFC[-6:] + '_Monthly_PRISM_' + variable + '_Summary.csv', 'w')
    else:
        out_file = open(output_folderPath + RFC + '_Monthly_PRISM_' + variable + '_Summary.csv', 'w')
    out_file.write('variable: ' + variable + ',' + 'units: ' + units[variable] + '\n')
    out_file.write('Basin,'+'Jan,'+'Feb,'+'Mar,'+'Apr,'+'May,'+'Jun,'+'Jul,'+'Aug,'+'Sep,'+'Oct,'+'Nov,'+'Dec,'+'\n')
    #loop through NLCD .xls files in folderPath
    for basin in basins:
        out_file.write(basin + ',')
        for month in months:
            print basin
            basin_file = open(csv_folderPath + basin + '_prism_' + month + '.csv', 'rb')
            csv_read = csv.reader(basin_file)
            row_num = 0
            if variable == 'ppt':
                for row in csv_read:
                    if row_num == 1:
                        precip_in = float(row[2]) / 25.4    # convert mm to in
                        if RFC[:5] == 'APRFC':
                            precip_in = precip_in / 100 # AK PRISM units mm * 100
                        out_file.write(str("%.2f" % precip_in) + ',')
                        print month + ' -> ' + str("%.2f" % precip_in)
                    row_num += 1
            else:
                for row in csv_read:
                    if row_num == 1:
                        temp_in = float(row[2]) # no temperature conversion
                        if RFC[:5] == 'APRFC':
                            temp_in = temp_in / 100 # AK PRISM units C * 100
                        out_file.write(str("%.2f" % temp_in) + ',')
                        print month + ' -> ' + str("%.2f" % temp_in)
                    row_num += 1
        out_file.write('\n')
        
print 'Finished!'
out_file.close()
