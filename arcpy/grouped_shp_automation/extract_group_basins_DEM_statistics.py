# ---------------------------------------------------------------------------
# extract_group_basins_DEM_statistics.py
# Created on: 2015-10-09 (originally generated by ArcGIS/ModelBuilder)
# Usage: extract_basin_DEM_statistics <Basin> 
# Description: extract elevation and slope characteristics for a basin shapefile

# UPDATED (10/14/2015): use a search cursor loop on a shapefile containing multiple basins
# Created and Modified by Ryan Spies (rspies@lynkertech.com)
# ---------------------------------------------------------------------------
print 'Importing modules...'
# Import arcpy module
import arcpy
import os
import csv
import winsound
arcpy.env.overwriteOutput = True
#os.chdir("../../../GIS/")
maindir = os.getcwd()

################### User Input #####################
RFC = 'WGRFC_2021'
fx_group = '' # leave blank if not processing by fx group
#in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_from' + RFC[:5] + '\\calb_basins\\calb_basins_DES.shp'
in_shp = r'F:\projects\2021_twdb_wgrfc_calb\gis\basin_shapefiles\210318_Calb_Basins_Joined\Calb_Basins.shp'
find_ch5id = 'Arc_Name_n' # attribute table header for basin id -> must exist!!!
#find_name = 'NAME' # optional: attribute table header for more basin info

#dem_file = maindir + '\\GTOPO_1K_Hydro\\na_dem_null' # 1km resolution
dem_file = r'F:\projects\2021_twdb_wgrfc_calb\data\DEM_nhdplus\NHDPlusTX\NHDPlus12\NEDSnapshot\elev_cm_merge.tif'
#dem_file = r'P:\NWS\GIS\APRFC\Processing\ASTER\kusk_mosiac.tif'
    
# Output directory for the basin .csv summary files
if fx_group != '':
    output_dir = "F:\\projects\\2021_twdb_wgrfc_calb\\data\DEM_nhdplus\\Elevation_Slope\\Stats_Out\\"
else:
    output_dir = "F:\\projects\\2021_twdb_wgrfc_calb\\data\DEM_nhdplus\\Elevation_Slope\\Stats_Out\\"

# manually enter basins to analyze (example: basins = ['MFDN3'])
# otherwise leave blank and script will
# analyze all basins in the basins_folder specified above
#basins_overwrite = [] 
################# End User Input ######################

if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Local variables (temporary files):
Basin_DEM = 'C:\\NWS\\python\\temp_output\\basin_DEM'
Slope_Raster = 'C:\\NWS\\python\\temp_output\\basin_slope'
Slope_Points = 'C:\\NWS\\python\\temp_output\\slope_points'
Slope_Stats__dbf = 'C:\\NWS\\python\\temp_output\\slope_stats.dbf'
Elevation_Points = 'C:\\NWS\\python\\temp_output\\elevation_pts'
Elevation_Stats__dbf = 'C:\\NWS\\python\\temp_output\\elevation_stats'

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = "C:\\NWS\\python\\Model_Output.gdb" # temporary file storage directory
#arcpy.env.parallelProcessingFactor = "50"
print 'ok so far...'

# use search cursor to loop through individual basins in shapefile
basins = arcpy.SearchCursor(in_shp)
fields = arcpy.ListFields(in_shp, "", "String")

#Process: Define Projection
check_project = in_shp[:-4] + '.prj'
if not os.path.exists(check_project):
    sr = arcpy.SpatialReference(4269) # define projection of basin shp -> 4269 = GCS_North_American_1983
    print 'Defining Projection...'
    arcpy.DefineProjection_management(in_shp, sr)
        
# Search cursor info: http://resources.arcgis.com/de/help/main/10.1/index.html#//018w00000011000000     
with arcpy.da.SearchCursor(in_shp, ("SHAPE@",find_ch5id)) as cursor: # search cursor gets "A geometry object for the feature" and the "NAME" attribute for each basin
    for index, row in enumerate(cursor): 
        Basin_Boundary = row[0] # basin geometry
        ch5id = row[1] # basin = find_ch5id
        print 'Processing basin: ' + str(ch5id)
        print 'ch5id = ' + row[1]
        
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
        print 'Creating '+ ch5id + '_mean_slope_percent.csv file...'
        rows = arcpy.SearchCursor(Slope_Stats__dbf)
        slope_csv = open(output_dir + ch5id + '_mean_slope_percent.csv', 'wb')
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
        print 'Creating '+ ch5id + '_elevation_stats_cm.csv file...'
        rows = arcpy.SearchCursor(Elevation_Stats__dbf)
        elevation_csv = open(output_dir + ch5id + '_elevation_stats_cm.csv', 'wb')
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
winsound.Beep(800,1000) # beep to indicate script is complete 
