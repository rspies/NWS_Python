# ---------------------------------------------------------------------------
# extract_basin_prism_values.py
# Created on: 2014-07-22 18:30:25.00000 (generated by ArcGIS/ModelBuilder)
# Description: extract prism data from raster using basin shapefiles as mask
# and output a csv file for each basin
# UPDATED (8/4/2014): calculate basin mean temperature or precipitation
# Created and Modified by Ryan Spies (ryan.spies@amec.com)
# ---------------------------------------------------------------------------
print 'Importing modules...'
# Import modules
import arcpy
import os
import csv
os.chdir("../..")
maindir = os.getcwd()

################### User Input ###########################################################
RFC = 'MBRFC_FY2015'
variable = 'recharge' # choices: 'recharge' or 'trans'
basins_folder = maindir + '\\' + RFC + '\\Shapefiles\\calb_basins\\'

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
basins_overwrite = [] 

output_dir = maindir + '\\' + RFC + '\\GW_' + variable + '\\'  # this must contain a folder for each basin (eg. FONN7)
################# End User Input ##########################################################

if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")

# Process: output csv file
print 'Creating '+ RFC + '_recharge.csv file...'
recharge_csv = open(output_dir + RFC + '_' + variable + '.csv', 'ab')
csvFile = csv.writer(recharge_csv) #output csv

# location of PRISM Raster (CONUS)
if variable == 'recharge':
    Recharge_Dataset = 'D:\\GIS Library\\rech48grd\\rech48grd'
    csvFile.writerow(['Basin','Mean Annual Recharge (mm)', 'Mean Annual Recharge (in)'])
if variable == 'trans':
    Recharge_Dataset = maindir + '\\SERFC\\TransmissivityMap_data_USGS\\transidw'
    csvFile.writerow(['Basin','log base 10 ft2 per day'])
print Recharge_Dataset

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True

# Set Geoprocessing environments
#arcpy.env.scratchWorkspace = "P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output.gdb" # temporary file storage directory
#arcpy.env.parallelProcessingFactor = "50"
print 'ok so far...'

#################################################################################
# find all basins in RFC or only run the specified basin list
# find all basins in RFC task or only run the specified basin overwrite list
basin_files = os.listdir(basins_folder) # list all basin shapefiles in the above specified directory
if len(basins_overwrite) != 0:
    basin_files = basins_overwrite      # use the basins_overright variable to run only specified basins instead of all RFC basins
basins = []
check_dir = os.listdir(output_dir)      # list all folders in output_dir
for each in basin_files:
    if each.split('.')[0] not in basins:
        basins.append(each.split('.')[0])
print basins

print 'Identified ' + str(len(basins)) + ' basins in ' + RFC + ' input directory...'        
all_data = {}
# loop through basins
for basin in basins:
    ## Script arguments
    Basin_Boundary = basins_folder + '\\' + basin + '.shp'
    # location of PRISM Raster (CONUS)
    #Recharge_Dataset = 'Q:\\GISLibrary\\rech48grd\\rech48grd'

    print basin 
    #Out_text = output_dir + basin + '_prism' + '.csv' 

    ## Local variables:
    Basin_Raster = 'C:\\NWS\\python\\temp_output\\' + basin

    ## Process: Extract by Mask
    print 'Extracting by mask...'
    arcpy.gp.ExtractByMask_sa(Recharge_Dataset, Basin_Boundary, Basin_Raster)

    ## Process: Calculate mean of raster
    print 'Raster to point...'
    result = arcpy.GetRasterProperties_management(Basin_Raster, "MEAN")
    print result
    all_data[basin]=str(result)
    if variable == 'recharge':
        csvFile.writerow([basin,all_data[basin],float(all_data[basin])/25.4])
    if variable == 'trans':
        csvFile.writerow([basin,all_data[basin]])

# Process: output csv file
#print 'Creating '+ basin + '_recharge.csv file...'
#recharge_csv = open(output_dir + RFC + '_recharge' + '.csv', 'wb')
#csvFile = csv.writer(recharge_csv) #output csv
#csvFile.writerow(['Basin','Mean Annual Recharge (mm)', 'Mean Annual Recharge (in)'])
#for each in all_data:
#    csvFile.writerow([each,all_data[each],all_data[each]/25.4])
recharge_csv.close()

print 'Completed grid extraction!'
