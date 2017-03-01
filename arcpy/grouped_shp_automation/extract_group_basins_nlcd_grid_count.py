# ---------------------------------------------------------------------------
# extract_group_basins_nlcd_grid_count.py
# Modified on: 2015-10-13 (originally generated by ArcGIS/ModelBuilder)

# Created and Modified by Ryan Spies (rspies@lynkertech.com)
# Description: extract NLCD gridded data using basin shapefiles and write
# a land cover count summary to csv file
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
os.chdir("../../../GIS/")
maindir = os.getcwd()

################### User Input #####################
RFC = 'MARFC_FY2017'
fx_group = '' # leave blank if not processing by fx group
#in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_from' + RFC[:5] + '\\calb_basins\\calb_basins_DES.shp'
in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_fromRFC\\calb_basins\\' + 'marfc_fy17_calb_basins.shp'
find_ch5id = 'CH5_ID' # attribute table header for basin id -> must exist!!!
#find_name = 'NAME' # optional: attribute table header for more basin info

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
#basins_overwrite = [] 

if fx_group != '':
    output_dir = maindir + '\\'+ RFC[:5] + os.sep + RFC + '\\NLCD\\data_files\\' + fx_group + os.sep
else:
    output_dir = maindir + '\\'+ RFC[:5] + os.sep + RFC + '\\NLCD\\data_files\\'

# location of NLCD Raster (CONUS)
if RFC[:5] == 'APRFC': # different file for Alaska
    NLCD_Dataset = r'D:\\GIS Library\\NLCD\\AK_NLCD_2001\\ak_nlcd_2001_land_cover_3-13-08_se5.img'
    #NLCD_Dataset = r'Q:\\GISLibrary\\NLCD\\AK_NLCD_2001\\ak_nlcd_2001_land_cover_3-13-08_se5.img'
else:
    NLCD_Dataset = r'D:\\GIS Library\\NLCD\\nlcd_2011_landcover_2011_edition_2014_03_31.img'
################# End User Input ######################
if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")

ignore_basins = []
# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

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
        #print 'name = ' + row[2]
        if ch5id not in ignore_basins:
    
            ## Local variables:
            Basin_Raster = 'C:\\NWS\\python\\temp_output\\XX_' + ch5id
            Basin_Points = 'C:\\NWS\\python\\temp_output\\XX_' + ch5id + '_points'
            NLCD = 'C:\\NWS\\python\\temp_output\\' 
        
            # Process: Extract by Mask
            print 'Clipping raster with basin polygon...'
            #arcpy.gp.ExtractByMask_sa(NLCD_Dataset, Basin_Boundary, Basin_Raster)
            arcpy.Clip_management(NLCD_Dataset, "#", Basin_Raster, Basin_Boundary, "0", "ClippingGeometry")
            
            # Process: Build Raster Attribute Table
            print 'Building basin raster nlcd attribute table...'
            arcpy.BuildRasterAttributeTable_management(Basin_Raster, "Overwrite")
            arcpy.TableToTable_conversion(NLCD_Dataset, NLCD, 'nlcd_table.dbf')
        
            # Process: Join Field
            print 'Joining field with land cover name...'
            arcpy.JoinField_management(Basin_Raster, "Value", NLCD + 'nlcd_table.dbf', "VALUE", "Land_Cover")
            
            # Process: Table to Table
            print 'Converting to .dbf table...'
            arcpy.TableToTable_conversion(Basin_Raster, NLCD, ch5id + '_NLCD.dbf')#, "", "Value \"Value\" false false false 4 Long 0 0 ,First,#,P:\\NWS\\GIS\\Models\\Model_Output.gdb\\Extract_img1\\Band_1,Value,-1,-1;Count \"Count\" false false false 8 Double 0 0 ,First,#,P:\\NWS\\GIS\\Models\\Model_Output.gdb\\Extract_img1\\Band_1,Count,-1,-1;Land_Cover \"Land_Cover\" true false false 254 Text 0 0 ,First,#,P:\\NWS\\GIS\\Models\\Model_Output.gdb\\Extract_img1\\Band_1,Land_Cover,-1,-1", "")
            
            # Process: output csv file
            print 'Creating '+ ch5id.strip('XX_') + '_NLCD.csv file...'
            rows = arcpy.SearchCursor(NLCD + ch5id + '_NLCD.dbf')
            nlcd_csv = open(output_dir + ch5id.strip('XX_') + '_NLCD.csv', 'wb')
            csvFile = csv.writer(nlcd_csv) #output csv
            fieldnames = [f.name for f in arcpy.ListFields(NLCD + ch5id + '_NLCD.dbf')]
        
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
            nlcd_csv.close()
    
print 'Script completed!!'
winsound.Beep(800,1000) # beep to indicate script is complete
