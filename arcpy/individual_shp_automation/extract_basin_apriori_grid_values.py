# ---------------------------------------------------------------------------
# extract_basin_apriori_grid_values.py
# Created on: 2014-07-22 09:01:13.00000 (generated by ArcGIS/ModelBuilder)
# Usage: extract basin apriori grid values for all basins in a input RFC 
# Created by: Ryan Spies (Cody Moser arcgis tool)
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy
import numpy
import csv
import os
import glob
arcpy.env.overwriteOutput = True
os.chdir("../..")
maindir = os.getcwd()

################### User Input #####################
RFC = 'MBRFC_FY2015'
basins_folder = maindir + '\\' + RFC + '\\Shapefiles\\calb_basins\\'

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
basins_overwrite = []#['FRNO3','GOSO3','HARO3','HCRO3','JASO3','LOPO3','MNRO3','SPRO3','TRBO3','VIDO3'] 

output_dir =  maindir + '\\' + RFC + '\\Apriori\\'  # this must contain a folder for each basin (eg. FONN7)
################# End User Input ######################
if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")
print 'Processing...'

# location of apriori grids (CONUS)
SACSMA_Grids_Folder = 'D:\\NWS\\GIS\\APriori\\SACSMA_grids\\ssurgo\\grid_WGS84'

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = "D:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output.gdb" # temporary file storage directory
#arcpy.env.parallelProcessingFactor = "50"
print 'ok so far...'

# find all basins in RFC or only run the specified basin list
basin_files = os.listdir(basins_folder) # list all basin shapefiles in the above specified directory
if len(basins_overwrite) != 0:
    basin_files = basins_overwrite # use the basins_overright variable to run only specified basins instead of all RFC basins
basins = []
check_dir = os.listdir(output_dir) # list all folders in output_dir
for each in basin_files:
    print each
    if each.split('.')[0] not in basins:
        basins.append(each.split('.')[0])
        if not os.path.exists(output_dir + os.sep + each.split('.')[0]):
            os.makedirs(output_dir + os.sep + each.split('.')[0])
            print 'Created dirctory for basin: ' + each

print 'Identified ' + str(len(basins)) + ' basins in ' + RFC + ' input directory...'        
basins = ['2804','2817','2818','2828','2870','2850','2851']
# loop through basins
for basin in basins:
    ## Script arguments
    Basin_Boundary = basins_folder + '\\' + basin + '.shp'

    # list all SACSMA SSURGO grids (directories containing data only) #ignore extra files in directory
    all_ssurgo = [ name for name in os.listdir(SACSMA_Grids_Folder) if os.path.isdir(os.path.join(SACSMA_Grids_Folder, name)) ]    
    all_ssurgo.remove('info') # remove info directory from list of variables 
    for variable in all_ssurgo:
        print basin + ' --> ' + variable
        Out_text = output_dir + '\\' + basin + '\\' + basin + '_' + variable + '.txt' 

        ## Local variables:
        RASTER = SACSMA_Grids_Folder + '\\' + variable
        #Basin_Raster = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\' + variable
        #Basin_Points = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\' + variable + '_points'
        Basin_Raster = 'C:\\NWS\\python\\temp_output\\' + basin
        Basin_Points = 'C:\\NWS\\python\\temp_output\\' + basin + '_points'

        ## Process: Extract by Mask
        print 'Extracting by mask...'
        arcpy.gp.ExtractByMask_sa(RASTER, Basin_Boundary, Basin_Raster)

        ## Process: Raster to Point
        print 'Raster to point...'
        arcpy.RasterToPoint_conversion(Basin_Raster, Basin_Points, "VALUE")
        #
        ## Process: Export Feature Attribute to ASCII
        print 'Export attributes to text...'
        arcpy.ExportXYv_stats(Basin_Points + '.shp', "GRID_CODE", "COMMA", Out_text, "ADD_FIELD_NAMES")

print 'Completed grid extraction!'

print 'Merging all basin apriori data into single csv file...'
for Basin in basins:
    print Basin
    folderPath = maindir + '\\' + RFC + '\\APriori\\'+ Basin + '\\'
    apriori_file = open(folderPath + Basin + '_apriori_parameters.csv', 'w')
    apriori_file.write('Parameter,' + 'Mean,' + 'Max,' + 'Min,' + '\n')
    
    #SAC-SMA SECTION--------------------------------------------------------------
    #loop through SACSMA files in folderPath
    for filename in glob.glob(os.path.join(folderPath, "*.txt")):
        #print filename
    
        #Define output file name
        name = str(os.path.basename(filename)[:])
        name = name.replace('.txt', '')
        #print name
    
        txt_file = open(filename, 'r')
    
        #csv_file = open(r'P:\\NWS\\GIS\\NERFC\\APriori\\temp.csv', 'w')
        csv_file = open(folderPath + 'temp.csv', 'w')
    
        #csv_file.write('BASIN, MEAN, MIN, MAX,' + '\n')
        
        grid = []
        
        for line in txt_file:
            #print line
            csv_file.write(line)
    
        csv_file.close()
        txt_file.close()
    
        csv_file = open(folderPath + 'temp.csv')
        
        data_file = csv.reader(csv_file, delimiter = ',')
        data_file.next()
    
        grid = []
        
        for row in data_file:
            grid_code = float(row[2])
            grid.append(grid_code)
    
        maximum = numpy.max(grid)
        minimum = numpy.min(grid)
        mean = numpy.mean(grid)
    
        #print 'grid is', grid
        #print 'max is', maximum
        #print 'min is', minimum
        #print 'mean is', mean
    
        apriori_file.write(name + ',' + str(mean) + ',' + str(maximum) + ',' + str(minimum) + ',' + '\n')
    
    apriori_file.close()
    
    csv_file.close()
    os.remove(folderPath + 'temp.csv')
    
    print 'A priori parameters in', apriori_file

print 'Script Completed'
