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
RFC = 'NCRFC_FY2016' 
variable = 'ppt' # use temperature: 'tmean' or precipitation: 'ppt'

#FOLDER PATH OF NLCD .xls DATA FILES
xls_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\PRISM\\1981_2010_climo_' + variable + '\\' 
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = maindir + '\\GIS\\'+ RFC[:5] + os.sep + RFC + '\\PRISM\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'
#Define output file name
out_file = open(output_folderPath + RFC + '_PRISM_Summary_1981_2010_' + variable + '.csv', 'w')
out_file.write('Basin,' + 'PRISM Annual Precip (in),' + '\n')

basins=[]
files = os.listdir(xls_folderPath)
#loop through NLCD .xls files in folderPath
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
                out_file.write(basin + ',' + str("%.2f" % precip_in) + '\n')
            row_num += 1
    
print 'Finished!'
out_file.close()
