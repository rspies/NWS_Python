# ---------------------------------------------------------------------------
# Created by: Ryan Spies (rspies@lynkertech.com)
# Date: 6/9/2015
# UPDATED (10/14/2015): use a search cursor loop on a shapefile containing multiple basins
# extract_basin_gSSURGO_data.py
# Description: extract gSSURGO gridded soil data using basin shapefiles and write
# a land cover count summary to csv file
# NOTE: only runs one SSURGO raster (usually 1 file for each state) -> requires
# multiple runs for basins in more than one state
#
# Steps to set up run:
# 1. Make sure the MapunitRaster_XX_10m raster has not been joined yet (Errors with field names? & Error 000049 : Failed to build attribute table)
# 2. Open ArcMap and import the muaggatt table from the gssurgo .gdb directory
# 3. Right click on the table -> export (as dBASE Table)  -> save to SSURGO\XX\soils\mukey_join.dbf
# 4. Check that the mukey attribute is type long (not string), create new column if needed
# 5. Open windows command line and navigate to script (needs arcmap 10.6 -> python v2.7?)
# 5. Execute script
# --------------------------------------------------------------------------
# Import arcpy module
print 'Importing modules...'
import arcpy
import os
import os.path
import csv
import winsound
arcpy.env.overwriteOutput = True

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

os.chdir("../..")
maindir = os.getcwd()

os.chdir("../../..")
gisdir = os.getcwd()

################### User Input #####################
###################################################
RFC = 'WGRFC_2021'
fx_group = '' # leave blank if not processing by fx group
#in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_from' + RFC[:5] + '\\calb_basins\\calb_basins_DES.shp'
in_shp = "E:\\TWDB_WGRFC\\basins\\210318_Calb_Basins_Joined\\Calb_Basins.shp"
#maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_fromRFC\\calb_basins\\' + 'marfc_fy17_calb_basins.shp'
find_ch5id = 'Arc_Name_n' # attribute table header for basin id -> must exist!!!
#find_name = 'NAME' # optional: attribute table header for more basin info
state = 'TX'

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [] or basins_overwrite = ['COCF1'])
basins_overwrite = ['PPDT2']#
#ignore_basins = ['NWFM1','LOMM8','LTRM8','CYNM8','MRIM8','2802','ACMM8','BHLM8','DBMM8',]

# location of the state raster SSURGO data
State_gSSURGO_Raster = 'E:\\TWDB_WGRFC\\gSSURGO\\soils_GSSURGO_tx_3899944_01\\soils\\gssurgo_g_tx\\gSSURGO_TX.gdb\\MapunitRaster_10m'
join_table = 'E:\\TWDB_WGRFC\\gSSURGO\\soils_GSSURGO_tx_3899944_01\\soils\\gssurgo_g_tx' + '\\mukey_join.dbf'
#State_soil_table = r'Q:\GISLibrary\SSURGO\TN\soils\gssurgo_g_tn.gdb\muaggatt'

# Output directory for the basin .csv summary files
if fx_group != '':
    output_dir = 'E:\\TWDB_WGRFC\\gSSURGO\\data_files\\'
else:
    output_dir = 'E:\\TWDB_WGRFC\\gSSURGO\\data_files\\'
######################################################
################# End User Input ######################

print 'REMINDER: Check that mukey_join.dbf "mukey" field is type long!!!'
# original mukey column is "string" type and join will skip several instances
winsound.Beep(1000,700) # beep to indicate script is complete
#raw_input("Press enter to continue processing...")

#check that SSURGO file exits (may be named differently for older downloads)
if os.path.exists(os.path.dirname(State_gSSURGO_Raster)) == False:
    print 'Can not find SSURGO raster for ' + state
print 'State GSSURGO Raster location: ' + State_gSSURGO_Raster

if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")
print 'setup ok so far...'

ignore_basins = []
#################################################################################

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
            Basin_gSSURGO_Raster = 'C:\\NWS\\python\\temp_output\\x' + ch5id + 'go' #put an x in front of raster name (some basins start with number)
            Model_Output_gdb = 'C:\\NWS\\python\\temp_output\\'
            
            # Process: Extract by Mask
            print 'Extracting raster with basin polygon...'
            #arcpy.gp.ExtractByMask_sa(State_gSSURGO_Raster, Basin_Boundary, Basin_gSSURGO_Raster)
            try:
                arcpy.Clip_management(State_gSSURGO_Raster, "#", Basin_gSSURGO_Raster, Basin_Boundary, "0", "ClippingGeometry")
                print 'Clip successful...'
                gonogo = 'go'
            except Exception as e:
                if e.message[:12] == 'ERROR 001566':
                    print '!!!!! Basin appears to be outside ' + state + ' raster...skipping'
                    gonogo = 'no'
                else:
                    print e.message
                    gonogo = 'no'
        
            if gonogo == 'go':
                # Build Basin Raster attribute table
                print 'Building basin raster attribute table...'
                arcpy.BuildRasterAttributeTable_management(Basin_gSSURGO_Raster,"Overwrite")
                
                # Process: Join Field
                print 'Joining "VALUE" and "hydgrpdcd" fields...'
                try:
                    arcpy.JoinField_management(Basin_gSSURGO_Raster, "VALUE", join_table, "MUKEY", "hydgrpdcd")
                    print 'Join successful!'
                except Exception as x:
                    if 'ERROR 000728' in x.message:
                        print 'Could not find VALUE in join... trying "mukey"'
                        arcpy.JoinField_management(Basin_gSSURGO_Raster, "MUKEY", join_table, "MUKEY", "hydgrpdcd")
                        print 'Join successful!'
                    else:
                        print 'error = ' + x.message
            
                # Process: Table to Table
                print 'Converting to .dbf table...'
                # Process: Table to Table
                arcpy.TableToTable_conversion(Basin_gSSURGO_Raster, Model_Output_gdb, "out_table.dbf", "", "VALUE \"VALUE\" false true true 0 Long 0 0 ,First,#,,VALUE,-1,-1,,Value,-1,-1;COUNT \"COUNT\" false true true 0 Long 0 0 ,First,#,,COUNT,-1,-1,,Count,-1,-1;MUKEY \"MUKEY\" true true false 30 Text 0 0 ,First,#,,MUKEY,-1,-1;hydgrpdcd \"Hydrologic Group - Dominant Conditions\" true true false 254 Text 0 0 ,First,#,,hydgrpdcd,-1,-1", "")
              
                # Process: output csv file
                print 'Creating '+ ch5id + '_gSSURGO.csv file...'
                rows = arcpy.SearchCursor(Model_Output_gdb + '\\out_table.dbf')
                
                #check if output file already exits
                if os.path.isfile(output_dir + ch5id + '_gSSURGO.csv') == True:
                    print 'Appending data to existing basin csv file...'
                    header = True
                else:
                    header = False
                ssurgo_csv = open(output_dir + ch5id + '_gSSURGO.csv', 'ab')
                csvFile = csv.writer(ssurgo_csv) #output csv
                fieldnames = [f.name for f in arcpy.ListFields(Model_Output_gdb+ '\\out_table.dbf')]
            
                allRows = []
                for row in rows:
                    rowlist = []
                    for field in fieldnames:
                        rowlist.append(row.getValue(field))
                    allRows.append(rowlist)
                if header == False:
                    csvFile.writerow(fieldnames)
                for row in allRows:
                    csvFile.writerow(row)
                row = None
                rows = None
                ssurgo_csv.close()
            print '\n'
   
print 'Script completed!!'
winsound.Beep(800,1000) # beep to indicate script is complete
