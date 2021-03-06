# ---------------------------------------------------------------------------
# extract_basin_prism_values.py
# Created on: 2014-07-22 18:30:25.00000 (generated by ArcGIS/ModelBuilder)
# Description: extract prism data from raster using basin shapefiles as mask
# and output a csv file for each basin
# UPDATED (8/4/2014): calculate basin mean temperature or precipitation
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
variables = ['tmean','tmax','tmin','ppt'] # use temperature: 'tmean','tmax','tmin' or precipitation: 'ppt'
resolution = '4km' # choices: '800m' or '4km' -> PRISM resolution
#in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_from' + RFC[:5] + '\\calb_basins\\calb_basins_DES.shp'
in_shp = r'F:\projects\2021_twdb_wgrfc_calb\gis\basin_shapefiles\210318_Calb_Basins_Joined\Calb_Basins.shp'
find_ch5id = 'Arc_Name_n' # attribute table header for basin id -> must exist!!!
#find_name = 'NAME' # optional: attribute table header for more basin info

# if you only want to run specific basins or ignore basins -> list them below
# otherwise set it equal to empty list (basins_overwrite = [])
#basins_overwrite = ['DTTM8']
ignore_basins = []
################# End User Input ######################
if RFC[:5] == 'APRFC':
    resolution = '4km' # only 4km 1971-2000 data for Alaska

for variable in variables:
    if fx_group != '':
        output_dir = maindir + '\\'+ RFC[:5] + os.sep + RFC + '\\PRISM\\Model_Builder_Output_' + variable + '_' + resolution +'_month\\' + fx_group +os.sep
    else:
        output_dir =  'F:\\projects\\2021_twdb_wgrfc_calb\\data' + '\\PRISM\\Model_Builder_Output\\' + variable + '_' + resolution +'_month\\'

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

    #################################################################################


    for month in months:
        # location of PRISM Raster (CONUS)
        if RFC[:5] == 'APRFC':
            PRISM_Dataset = 'D:\\GIS Library\\PRISM\\Alaska\\AK_PRISM_' + variable + '\\' + variable + '\\' + variable + months[month]
        else:
            PRISM_Dataset = 'D:\\GIS Library\\PRISM\\1981_2010\\' + variable + '\\'+resolution+'\\PRISM_'+variable+'_30yr_normal_'+resolution+'M2_' +months[month]+ '_asc.asc'

        # Search cursor info: http://resources.arcgis.com/de/help/main/10.1/index.html#//018w00000011000000     
        with arcpy.da.SearchCursor(in_shp, ("SHAPE@",find_ch5id)) as cursor: # search cursor gets "A geometry object for the feature" and the "NAME" attribute for each basin
            for index, row in enumerate(cursor): 
                Basin_Boundary = row[0] # basin geometry
                ch5id = row[1] # basin = find_ch5id
                print 'Processing basin: ' + str(ch5id)
                print 'ch5id = ' + row[1]
                #print 'name = ' + row[2]
                
                if ch5id not in ignore_basins: #check for ignore basins
                    ## Local variables:
                    Basin_Raster = 'C:\\NWS\\python\\temp_output\\' + ch5id
                    Basin_Points = 'C:\\NWS\\python\\temp_output\\' + ch5id + '_points'
                    Stats_Table = 'C:\\NWS\\python\\temp_output\\prism_stats.dbf'
            
                    ## Process: Extract by Mask
                    print 'Extracting/Clipping by mask...'
                    #arcpy.gp.ExtractByMask_sa(PRISM_Dataset, Basin_Boundary, Basin_Raster) # fails for small basins
                    arcpy.Clip_management(PRISM_Dataset, "#", Basin_Raster, Basin_Boundary, "0", "ClippingGeometry","NO_MAINTAIN_EXTENT")
                    
            
                    ## Process: Raster to Point
                    print 'Raster to point...'
                    arcpy.RasterToPoint_conversion(Basin_Raster, Basin_Points, "VALUE")
                    print 'Completed raster to point'
                    
                    # Process: Summary Statistics
                    print 'Calculating Summary statistics...'
                    arcpy.Statistics_analysis(Basin_Points + '.shp', Stats_Table, "GRID_CODE MEAN", "")
                    
                    # Process: output csv file
                    print 'Creating '+ ch5id + '_prism.csv file...'
                    rows = arcpy.SearchCursor(Stats_Table)
                    prism_csv = open(output_dir + ch5id + '_prism_' +month + '.csv', 'wb')
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
winsound.Beep(800,1000) # beep to indicate script is complete
