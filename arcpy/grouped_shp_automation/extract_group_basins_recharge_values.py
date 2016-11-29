# ---------------------------------------------------------------------------
# extract_group_basins_recharge_values.py
# Modified on: 2015-10-13 (originally generated by ArcGIS/ModelBuilder)
# Description: extract recharge data from raster using basin shapefiles as mask
# and output a csv file for each basin
# UPDATED (10/14/2015): use a search cursor loop on a shapefile containing multiple basins
# Created and Modified by Ryan Spies (rspies@lynkertech.com)
# ---------------------------------------------------------------------------
print 'Importing modules...'
# Import modules
import arcpy
import os
import csv
import winsound
os.chdir("../..")
maindir = os.getcwd()

################### User Input ###########################################################
RFC = 'NCRFC_FY2016'
fx_group = 'REDMIS' # leave blank if not processing by fx group
variable = 'recharge' # choices: 'recharge' or 'trans'
#in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_from' + RFC[:5] + '\\calb_basins\\calb_basins_DES.shp'
in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_fromNCRFC\\calb_basins\\' + 'calb_basins_REDMIS_join.shp'
find_ch5id = 'CH5_ID' # attribute table header for basin id -> must exist!!!
#find_name = 'NAME' # optional: attribute table header for more basin info

# if you only want to run specific basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
#basins_overwrite = ['KISF1','FTWF1','HSPF1','WORF1','OLNF1','FWHF1','VRNF1','MNIG1','TREF1','LK2F1','KSEF1','LK1F1','PLMF1','ESLS1','OLVG1'] 

if fx_group != '':
    output_dir = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\GW_' + variable + '\\' + fx_group +os.sep
else:
    output_dir = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\GW_' + variable + '\\'

################# End User Input ##########################################################

if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")

# Process: output csv file
print 'Creating '+ RFC + '_recharge.csv file...'
recharge_csv = open(output_dir + RFC + '_' + variable + '_' + str(in_shp.split('\\')[-1])[:-4] + '.csv', 'ab')
csvFile = csv.writer(recharge_csv) #output csv

# location of Recharge/Transmisivity Raster
if variable == 'recharge':
    Recharge_Dataset = 'D:\\GIS Library\\rech48grd\\rech48grd'
    csvFile.writerow(['Basin','Mean Annual Recharge (mm)', 'Mean Annual Recharge (in)'])
if variable == 'trans':
    Recharge_Dataset = 'D:\\GIS Library\\USGS_karst\\TransmissivityMap_data_USGS\\transidw'
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

# use search cursor to loop through individual basins in shapefile
basins = arcpy.SearchCursor(in_shp)
fields = arcpy.ListFields(in_shp, "", "String")

#Process: Define Projection
sr = arcpy.SpatialReference(4269) # define projection of basin shp -> 4269 = GCS_North_American_1983
check_project = in_shp[:-4] + '.prj'
if not os.path.exists(check_project):
    print 'Defining Projection...'
    arcpy.DefineProjection_management(in_shp, sr)

all_data = {}
# loop through basins
with arcpy.da.SearchCursor(in_shp, ("SHAPE@",find_ch5id)) as cursor: # search cursor gets "A geometry object for the feature" and the "NAME" attribute for each basin
    for index, row in enumerate(cursor): 
        Basin_Boundary = row[0] # basin geometry
        ch5id = row[1] # basin = find_ch5id
        print 'Processing basin: ' + str(ch5id)
        print 'ch5id = ' + row[1]
        #print 'name = ' + row[2]
        #if ch5id in basins_overwrite:

        ## Local variables:
        Basin_Raster = 'C:\\NWS\\python\\temp_output\\' + ch5id
    
        ## Process: Extract by Mask
        print 'Extracting by mask...'
        arcpy.gp.ExtractByMask_sa(Recharge_Dataset, Basin_Boundary, Basin_Raster)
    
        ## Process: Calculate mean of raster
        print 'Raster to point...'
        result = arcpy.GetRasterProperties_management(Basin_Raster, "MEAN")
        print result
        all_data[ch5id]=str(result)
        if variable == 'recharge':
            csvFile.writerow([ch5id,all_data[ch5id],float(all_data[ch5id])/25.4])
        if variable == 'trans':
            csvFile.writerow([ch5id,all_data[ch5id]])

recharge_csv.close()

print 'Completed grid extraction!'
winsound.Beep(800,1000) # beep to indicate script is complete 