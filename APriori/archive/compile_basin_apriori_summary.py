#compile_basin_apriori_summary.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: compiles basin apriori data
#from .txt files output from ArcGIS Model Builder

#import script modules
import glob
import os
import numpy
import csv
os.chdir("../..")
maindir = os.getcwd()

#USER INPUT SECTION----------------------------------------------------------------
#RFC
RFC = 'MBRFC_FY2015'
#FOLDER PATH OF A PRIORI .txt DATA FILES
input_directory = maindir + '\\GIS\\' + RFC + '\\Apriori\\Model_Builder_Output\\'
#FOLDER PATH OF OUTPUT SUMMARY FILE - Must be different than input_directory
output_folderPath = maindir + '\\GIS\\' + RFC + '\\Apriori\\'
#END USER INPUT SECTION------------------------------------------------------------

print 'Script is Running...'

summary_file = open(output_folderPath + RFC + '_APriori_Summary.csv', 'w')
summary_file.write('Parameter,' + 'Mean,' + 'Max,' + 'Min,' + '\n')

#loop through .txt files in input_directory
for filename in glob.glob(os.path.join(input_directory, "*.txt")):
    print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('.txt', '')
    #print name

    #set input_file as basin .txt file
    input_file = open(filename, 'r')

    #use csv.reader to open basin .txt file
    data_file = csv.reader(input_file, delimiter = ',')
    data_file.next()
    
    grid = []
    
    for row in data_file:
        grid_code = float(row[2])
        grid.append(grid_code)

    maximum = numpy.max(grid)
    minimum = numpy.min(grid)
    mean = numpy.mean(grid)

    summary_file.write(name + ',' + str(mean) + ',' + str(maximum) + ',' + str(minimum) + ',' + '\n')
    
    input_file.close()
summary_file.close()

print 'Script Complete'
print 'A priori parameters in', summary_file