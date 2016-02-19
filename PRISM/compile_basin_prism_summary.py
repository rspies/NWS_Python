#compile_basin_prism_summary.py
#Cody Moser/Ryan Spies
#cody.moser@amec.com
#AMEC
#Description: compiles basin prism data
#from .xls files output from ArcGIS Model Builder

#Import script modules
import glob
import os
import csv
import xlrd

#USER INPUT SECTION------------------------------------------------------------------------------
#PRISM Variable (ppt, tmean, tmin, tmax)
prism_var = 'ppt'
#RFC
RFC = 'NWRFC'
#FOLDER PATH OF .xls DATA FILES
input_directory = r'P:\\NWS\\GIS\\NWRFC\\FY2015\\PRISM\\Model_Builder_Output\\ppt\\1981_2010\\'
#FOLDER PATH OF OUTPUT SUMMARY FILE - Must be different than input_directory
output_folderPath = r'P:\\NWS\\GIS\\NWRFC\\FY2015\\PRISM\\'
#END USER INPUT SECTION---------------------------------------------------------------------------

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
output_file = open(output_folderPath + RFC + '_1981_2010_' + prism_var + '_Summary.csv', 'w')

#PRECIPITATION merge data section
if prism_var == 'ppt':
    #Write the summary .csv file header row
    output_file.write('Basin,' + prism_var + ' (mm),' + prism_var + ' (in)' + '\n')
    
    #loop through PRISM .csv files in folderPath
    for filename in glob.glob(os.path.join(input_directory, "*.csv")):
        #Get filename
        name = str(os.path.basename(filename)[:])
        #Open basin .csv file
        basin_csv_file = open(filename, 'r')
        #Use csv.reader to specify delimiter
        data_file = csv.reader(basin_csv_file, delimiter = ',')
        #Skip the first row
        data_file.next()
        #Get PRISM value
        for row in data_file:
            value_mm = float(row[2])
        value_in = value_mm * 0.0393701
        #Write PRISM value to summary .csv file
        output_file.write(name + ',' + str(value_mm) + ',' + str(value_in) + '\n')
        #Close the basin .csv file
        basin_csv_file.close()

#TEMPERATURE merge data section 
else:
    #Write the summary .csv file header row
    output_file.write('Basin,' + prism_var + ' (C),' + prism_var + ' (F)' + '\n')
    
    #loop through PRISM .csv files in folderPath
    for filename in glob.glob(os.path.join(input_directory, "*.csv")):
        #Get filename
        name = str(os.path.basename(filename)[:])
        #Open basin .csv file
        basin_csv_file = open(filename, 'r')
        #Use csv.reader to specify delimiter
        data_file = csv.reader(basin_csv_file, delimiter = ',')
        #Skip the first row
        data_file.next()
        #Get PRISM value
        for row in data_file:
            value_C = float(row[2])
        value_F = value_C * 1.8 + 32
        #Write PRISM value to summary .csv file
        output_file.write(name + ',' + str(value_C) + ',' + str(value_F) + '\n')
        #Close the basin .csv file
        basin_csv_file.close()    

#Close the summary PRISM file
output_file.close()

print 'prism Summary File is', output_file
print 'Script Complete'