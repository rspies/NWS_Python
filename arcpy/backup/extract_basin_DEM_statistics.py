# ---------------------------------------------------------------------------
# extract_basin_DEM_statistics.py
# Created on: 2014-07-22 18:31:56.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: extract_basin_DEM_statistics <Basin> 
# Description: 
# Created by Ryan Spies
# ---------------------------------------------------------------------------
################### User Input #####################

RFC = 'SERFC'
basins_folder = r'P:\NWS\GIS\SERFC\calib_basins'
dem_file = r'Q:\GISLibrary\NHDPlus\v1\SE\NHDPlus03V01_02_Elev_Unit_c\Elev_Unit_c\elev_cm'
output_dir = 'P:\\NWS\GIS\\' + RFC + '\\Elevation_Slope\\Stats_Out\\'

# mannually enter basins to analyze -> otherwise leave blank and script will
# analyze all basins in the basins_folder specified above
basins = ['COCF1'] 

################# End User Input ######################

# Import arcpy module
import arcpy
import os
import csv
arcpy.env.overwriteOutput = True

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Local variables (temporary files):
Basin_DEM = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\basin_DEM'
Slope_Raster = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\basin_slope'
Slope_Points = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\slope_points'
Slope_Stats__dbf = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\slope_stats.dbf'
Elevation_Points = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\elevation_pts'
Elevation_Stats__dbf = 'P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output\\elevation_stats'

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = "P:\\NWS\\GIS\\Models\\10_0_tools\\Model_Output.gdb" # temporary file storage directory
arcpy.env.parallelProcessingFactor = "50"
print 'ok so far...'

# find all basins in RFC
basin_files = os.listdir(basins_folder) # list all basin shapefiles in the above specified directory
if len(basins) == 0:
    for each in basin_files:
        if each[:5] not in basins:
            basins.append(each[:5])
    
#basins = ['CHEN7']        
for basin in basins:    
    print basin
    Basin_Boundary = basins_folder + '\\' + basin + '.shp'
    
    # Process: Extract by Mask
    print 'Extract by mask...'
    arcpy.gp.ExtractByMask_sa(dem_file, Basin_Boundary, Basin_DEM)
    
    # Process: Slope
    print 'Calculating basin slope raster...'
    arcpy.gp.Slope_sa(Basin_DEM, Slope_Raster, "PERCENT_RISE", "0.01")
    
    # Process: Raster to Point (2)
    print 'Coverting raster to point...'
    arcpy.RasterToPoint_conversion(Slope_Raster, Slope_Points, "Value")
    
    # Process: Summary Statistics (2)
    print 'Calculating mean slope...'
    arcpy.Statistics_analysis(Slope_Points + '.shp', Slope_Stats__dbf, "grid_code MEAN", "")

    # Process: output csv file
    print 'Creating '+ basin + '_mean_slope_percent.csv file...'
    rows = arcpy.SearchCursor(Slope_Stats__dbf)
    slope_csv = open(output_dir + basin + '_mean_slope_percent.csv', 'wb')
    csvFile = csv.writer(slope_csv) #output csv
    fieldnames = [f.name for f in arcpy.ListFields(Slope_Stats__dbf)]

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
    slope_csv.close()
        
    # Process: Raster to Point
    print 'Converting elevation raster to point...'
    arcpy.RasterToPoint_conversion(Basin_DEM, Elevation_Points, "VALUE")
    
    # Process: Summary Statistics
    print 'Calculating elevation statistics...'
    arcpy.Statistics_analysis(Elevation_Points + '.shp', Elevation_Stats__dbf, "grid_code MIN;grid_code MEAN;grid_code MAX", "")
    
    # Process: output csv file
    print 'Creating '+ basin + '_elevation_stats_cm.csv file...'
    rows = arcpy.SearchCursor(Elevation_Stats__dbf)
    elevation_csv = open(output_dir + basin + '_elevation_stats_cm.csv', 'wb')
    csvFile = csv.writer(elevation_csv) #output csv
    fieldnames = [f.name for f in arcpy.ListFields(Elevation_Stats__dbf)]

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
    elevation_csv.close()
    
print 'Completed!!' 
