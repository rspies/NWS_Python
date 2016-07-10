# ---------------------------------------------------------------------------
# extract_basin_prism_values.py
# Created on: 2014-07-22 18:30:25.00000 (generated by ArcGIS/ModelBuilder)
# Description: extract prism data from raster using basin shapefiles as mask
# and output a csv file for each basin
# UPDATED (8/4/2014): calculate basin mean temperature or precipitation
# Created by Ryan Spies (ryan.spies@amec.com)
# ---------------------------------------------------------------------------
# Import modules
import arcpy
import os
import csv
arcpy.env.overwriteOutput = True
os.chdir("../..")
maindir = os.getcwd()

################### User Input #####################
RFC = 'MBRFC_FY2015'
variable = 'ppt' # use temperature: 'tmean' or precipitation: 'ppt'
basins_folder = maindir + '\\' + RFC + '\\Shapefiles\\calb_basins\\'

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
basins_overwrite = ['DTTM8'] 

output_dir = maindir + '\\' + RFC + '\\PRISM\\Model_Builder_Output_' + variable +'_month\\'  # this must contain a folder for each basin (eg. FONN7)
################# End User Input ######################
if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")
months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Set Geoprocessing environments
#arcpy.env.scratchWorkspace = "P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output.gdb" # temporary file storage directory
#arcpy.env.parallelProcessingFactor = "50"
print 'ok so far...'

#################################################################################
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
        #if not os.path.exists(output_dir + os.sep + each.split('.')[0]):
        #    os.makedirs(output_dir + os.sep + each.split('.')[0])

print 'Identified ' + str(len(basins)) + ' basins in ' + RFC + ' input directory...'        

for month in months:
    # location of PRISM Raster (CONUS)
    PRISM_Dataset = 'D:\\GIS Library\\PRISM\\1981_2010\\' + variable + '\\4km\\PRISM_'+variable+'_30yr_normal_4kmM2_' +months[month]+ '_asc.asc'

    # loop through basins
    for basin in basins:
        ## Script arguments
        Basin_Boundary = basins_folder + '\\' + basin + '.shp'

        print basin 
        #Out_text = output_dir + basin + '_prism' + '.csv' 

        ## Local variables:
        #Basin_Raster = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\' + basin
        #Basin_Points = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\' + basin + '_points'
        #Stats_Table = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\prism_stats.dbf'
        Basin_Raster = 'C:\\NWS\\python\\temp_output\\' + basin
        Basin_Points = 'C:\\NWS\\python\\temp_output\\' + basin + '_points'
        Stats_Table = 'C:\\NWS\\python\\temp_output\\prism_stats.dbf'

        ## Process: Extract by Mask
        print 'Extracting by mask...'
        arcpy.gp.ExtractByMask_sa(PRISM_Dataset, Basin_Boundary, Basin_Raster)

        ## Process: Raster to Point
        print 'Raster to point...'
        arcpy.RasterToPoint_conversion(Basin_Raster, Basin_Points, "VALUE")
        print 'Completed raster to point'
        
        # Process: Summary Statistics
        print 'Calculating Summary statistics...'
        arcpy.Statistics_analysis(Basin_Points + '.shp', Stats_Table, "GRID_CODE MEAN", "")
        
        # Process: output csv file
        print 'Creating '+ basin + '_prism.csv file...'
        rows = arcpy.SearchCursor(Stats_Table)
        prism_csv = open(output_dir + basin + '_prism_' +month + '.csv', 'wb')
        csvFile = csv.writer(prism_csv) #output csv
        fieldnames = [f.name for f in arcpy.ListFields(Stats_Table)]

        allRows = []
        for row in rows:
            rowlist = []
            for field in fieldnames:
                rowlist.append(row.getValue(field))
            allRows.append(rowlist)

        csvFile.writerow(fieldnames)
        for row in allRows:
            csvFile.writerow(row)
        row = None
        rows = None
        prism_csv.close()
    
print 'Completed grid extraction!'
