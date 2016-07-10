# ---------------------------------------------------------------------------
# Created by: Ryan Spies (rspies@lynkertech.com)
# Date: 6/9/2015
# extract_basin_gSSURGO_data.py
# Description: extract gSSURGO gridded soil data using basin shapefiles and write
# a land cover count summary to csv file
# NOTE: only runs one SSURGO raster (usually 1 file for each state) -> requires
# multiple runs for basins in more than one state
#
# Steps to set up run:
# 1. Make sure the MapunitRaster_XX_10m raster has not been joined yet (Errors with field names?)
# 2. Open ArcMap and import the “muaggatt” table from the gssurgo .gdb directory
# 3. Right click on the table -> export -> save to SSURGO\XX\soils\mukey_join.dbf
# 4. Run script
# --------------------------------------------------------------------------
import os
os.chdir("../../../..")
maindir = os.getcwd()

################### User Input #####################
###################################################
RFC = 'MBRFC_FY2015'
state = 'WY'
basins_folder = maindir + '\\NWS\\GIS\\' + RFC + '\\Shapefiles\\from_RFC\\bighorn_basins\\'

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [] or basins_overwrite = ['COCF1'])
basins_overwrite = []#
ignore_basins = ['TBRM8','LOMM8','LTRM8','CYNM8','MRIM8','2802','ACMM8','BHLM8','DBMM8',]

# location of the state raster SSURGO data
State_gSSURGO_Raster = maindir + 'GIS Library\\SSURGO\\' + state.upper() + '\\soils\\gssurgo_g_' + state.lower() + '.gdb\\MapunitRaster_' + state.upper() + '_10m'
join_table = maindir + 'GIS Library\\SSURGO\\' + state.upper() + '\\soils\\mukey_join.dbf'
#State_soil_table = r'Q:\GISLibrary\SSURGO\TN\soils\gssurgo_g_tn.gdb\muaggatt'

# Output directory for the basin .csv summary files
output_dir = maindir + '\\NWS\\GIS\\' + RFC + '\\SSURGO\\data_files\\'  # this must contain a folder for each basin (eg. FONN7)
######################################################
################# End User Input ######################

# Import arcpy module
import arcpy
from arcpy import env
import csv
arcpy.env.overwriteOutput = True

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Set Geoprocessing environments
#arcpy.env.outputCoordinateSystem = "PROJCS['USA_Contiguous_Albers_Equal_Area_Conic_USGS_version',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]"
#arcpy.env.parallelProcessingFactor = "50%"
print 'ok so far...'

#################################################################################
# find all basins in RFC or only run the specified basin list
basin_files = os.listdir(basins_folder) # list all basin shapefiles in the above specified directory
if len(basins_overwrite) != 0:
    basin_files = basins_overwrite      # use the basins_overright variable to run only specified basins instead of all RFC basins
basins = []
check_dir = os.listdir(output_dir)      # list all folders in output_dir
for each in basin_files:
    if each.split('.')[0] not in basins and each.split('.')[0] not in ignore_basins:
        if len(each) < 13:
            basins.append(each.split('.')[0])
        else:
            print 'Ignoring: ' + each + ' - name too long'

print 'Identified ' + str(len(basins)) + ' basins in ' + RFC + ' input directory...'

# loop through basins
for basin in basins:
    ## Script arguments
    Basin_Boundary_shp_File = basins_folder + '\\' + basin + '.shp'
    print basin 
    
    ## Local variables:
    Basin_gSSURGO_Raster = 'C:\\NWS\\python\\temp_output\\x' + basin + '_soil' #put an x in front of raster name (some basins start with number)
    Model_Output_gdb = 'C:\\NWS\\python\\temp_output\\'
    
    # Process: Extract by Mask
    print 'Extracting raster with basin polygon...'
    #arcpy.gp.ExtractByMask_sa(State_gSSURGO_Raster, Basin_Boundary_shp_File, Basin_gSSURGO_Raster)
    arcpy.Clip_management(State_gSSURGO_Raster, "#", Basin_gSSURGO_Raster, Basin_Boundary_shp_File, "0", "ClippingGeometry")    

    # Build Basin Raster attribute table
    print 'Building basin raster attribute table...'
    arcpy.BuildRasterAttributeTable_management(Basin_gSSURGO_Raster)
    
    # Process: Join Field
    print 'Joining "MUKEY" and "hydgrpdcd" fields...'
    arcpy.JoinField_management(Basin_gSSURGO_Raster, "MUKEY", join_table, "mukey", "hydgrpdcd")    

    # Process: Table to Table
    print 'Converting to .dbf table...'
    # Process: Table to Table
    arcpy.TableToTable_conversion(Basin_gSSURGO_Raster, Model_Output_gdb, "out_table.dbf", "", "VALUE \"VALUE\" false true true 0 Long 0 0 ,First,#,,VALUE,-1,-1,,Value,-1,-1;COUNT \"COUNT\" false true true 0 Long 0 0 ,First,#,,COUNT,-1,-1,,Count,-1,-1;MUKEY \"MUKEY\" true true false 30 Text 0 0 ,First,#,,MUKEY,-1,-1;hydgrpdcd \"Hydrologic Group - Dominant Conditions\" true true false 254 Text 0 0 ,First,#,,hydgrpdcd,-1,-1", "")
  
    # Process: output csv file
    print 'Creating '+ basin + '_gSSURGO.csv file...'
    rows = arcpy.SearchCursor(Model_Output_gdb + '\\out_table.dbf')
    ssurgo_csv = open(output_dir + basin + '_gSSURGO.csv', 'wb')
    csvFile = csv.writer(ssurgo_csv) #output csv
    fieldnames = [f.name for f in arcpy.ListFields(Model_Output_gdb+ '\\out_table.dbf')]

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
    ssurgo_csv.close()
   
print 'Script completed!!'
