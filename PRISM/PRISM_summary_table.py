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
import xlrd # python module for exel file handling
import csv
os.chdir("../..")
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC Region
RFC = 'NWRFC_FY2017'
fx_group = '' # leave blank if not processing by fx group
variables = ['tmean','ppt'] # use temperature: 'tmean' or precipitation: 'ppt'
resolution = '800m' # choices: '800m' or '4km' -> PRISM resolution
climo_period = '1981_2010'
####################################################################
#END USER INPUT SECTION
####################################################################

for variable in variables:
    print variable
    #FOLDER PATH OF NLCD .xls DATA FILES
    if fx_group != '':
        xls_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\PRISM\\' + climo_period + '_climo_' + variable + '_' + resolution + '\\' + fx_group + '\\'
    else:
        xls_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\PRISM\\' + climo_period + '_climo_' + variable + '_' + resolution + '\\'
    #FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
    output_folderPath = maindir + '\\GIS\\'+ RFC[:5] + os.sep + RFC + '\\PRISM\\'
    
    print 'Script is Running...'
    #Define output file name
    if fx_group != '':
        out_file = open(output_folderPath + RFC[:5] + '_' +  RFC[-6:] + '_' + fx_group +  '_PRISM_Summary_' + climo_period + '_' + variable + '_' + resolution + '.csv', 'w')
    else:
        out_file = open(output_folderPath + RFC + '_PRISM_Summary_' + climo_period + '_' + variable + '_' + resolution + '.csv', 'w')
    
    basins=[]
    files = os.listdir(xls_folderPath)
    #loop through NLCD .xls files in folderPath
    if variable == 'ppt':
        out_file.write('Basin,' + 'PRISM Mean Annual Precip (in),' + '\n')
        for filename in files:
            #print filename[-3:]
            basin = (filename.split('_'))[0]
            if filename[-3:] == 'xls':
                print basin
                workbook = xlrd.open_workbook(xls_folderPath+filename)
                worksheet = workbook.sheet_by_name(basin + '_prism')
                cell_value = worksheet.cell_value(1, 2)
                precip_in = float(cell_value)/25.4 # convert mm to in
                out_file.write(basin + ',' + str("%.2f" % precip_in) + '\n')
            if filename[-3:] == 'csv':
                print basin
                basin_file = open(xls_folderPath + filename, 'rb')
                csv_read = csv.reader(basin_file)
                row_num = 0
                for row in csv_read:
                    if row_num == 1:
                        precip_in = float(row[2]) / 25.4    # convert mm to in
                        if RFC[:5] == 'APRFC':
                            precip_in = precip_in / 100 # AK PRISM units mm * 100
                        out_file.write(basin + ',' + str("%.2f" % precip_in) + '\n')
                    row_num += 1
    if variable == 'tmean':
        out_file.write('Basin,' + 'PRISM Mean Annual Temp (C),' + '\n')
        for filename in files:
            #print filename[-3:]
            basin = (filename.split('_'))[0]
            if filename[-3:] == 'xls':
                print basin
                workbook = xlrd.open_workbook(xls_folderPath+filename)
                worksheet = workbook.sheet_by_name(basin + '_prism')
                cell_value = worksheet.cell_value(1, 2)
                temp_c = float(cell_value)
                out_file.write(basin + ',' + str("%.2f" % temp_c) + '\n')
            if filename[-3:] == 'csv':
                print basin
                basin_file = open(xls_folderPath + filename, 'rb')
                csv_read = csv.reader(basin_file)
                row_num = 0
                for row in csv_read:
                    if row_num == 1:
                        temp_c = float(row[2]) 
                        if RFC[:5] == 'APRFC':
                            temp_c = temp_c / 100 # AK PRISM units C * 100
                        out_file.write(basin + ',' + str("%.2f" % temp_c) + '\n')
                    row_num += 1
        
    print 'Finished!'
out_file.close()
