# ---------------------------------------------------------------------------
# extract_group_basins_AEC_histogram.py
# Created and Modified by Ryan Spies (rspies@lynkertech.com)
# Date: 6/16/2015
# Description: clip DEM raster to basin/elev zone and convert attribute table
# to a .xls output for area elevation curve calculations

# UPDATED (10/14/2015): use a search cursor loop on a shapefile containing multiple basins
# ---------------------------------------------------------------------------
print 'Importing modules...'
# Import arcpy module
import arcpy
import xlrd
import numpy as np
import os
import csv
arcpy.env.overwriteOutput = True
os.chdir("../../../GIS/")
maindir = os.getcwd()

################### User Input #####################
RFC = 'MBRFC_FY2016'
in_shp = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Shapefiles_fromMBRFC\\calb_basins\\Bighorn_Yellowstone_calb_basins.shp'
find_ch5id = 'CH5_ID_RFQ' # attribute table header for basin id
find_name = 'NAME' # attribute table header for basin id
dem_file = maindir + '\\GTOPO_1K_Hydro\\na_dem_null' # 1km resolution

#name_id_file = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\AEC\\basin_name_id.txt'
medium_summary = open(maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\AEC\\median_elev_summary.csv','a')
output_dir = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\AEC\\raster_tables\\'
output_hist = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\AEC\\histograms\\'
output_chps = maindir + '\\' + RFC[:5] + os.sep + RFC + '\\Elevation_Slope\\AEC\\chps_input\\'
split_file = "D://Projects//NWS//Calibration_NWS//" + RFC[:5] + os.sep + RFC + os.sep + 'MBRFC_fy16_basin_splits.csv'
sr = arcpy.SpatialReference(4269) # define projection of basin shp -> 4269 = GCS_North_American_1983

# manually enter basins to analyze (example: basins = ['MFDN3'])
# otherwise leave blank and script will
# analyze all basins in the basins_folder specified above
basins_overwrite = []; elev_splits = {}
## basin splits manually defined - by RFC (feet)
#elev_splits = {'CLEM':[0,6500],'2870':[0,6000],'ADDM':[0,6000],'AGSM':[0,6500],'BTCM':[0,6000],'BULW':[0,7500,9500],'DBRM':[0,5000]
#    ,'DCKW':[0,7500,9500],'DINW':[7500,9500],'DTTM':[0,6000],'DUBW':[0,7500,9500],'EDNM':[0,5500],'HLTM':[0,6000],'LPPM':[0,6000]
#    ,'NFSM':[0,6500],'NFSW':[0,7500,9500],'SMHM':[0,6500],'SSNM':[0,6500],'TSFM':[0,6000],'ULLM':[0,5500],'VLYW':[0,7500,9500]
#    ,'WLLM':[0,6000],'WRCW':[0,7500,9500]}
################# End User Input ######################

# read csv file with elev split info
reader = csv.reader(open(split_file))
next(reader) # skip header line
for row in reader:
    if len(row[9]) > 0:
        elev_splits[row[0]]=[int(row[9])]
    if len(row[10]) > 0:
        elev_splits[row[0]].append(int(row[10]))
    if len(row[11]) > 0:
        elev_splits[row[0]].append(int(row[11]))
print elev_splits

medium_summary.write('Basin,Medium Elev (m),# of DEM cells,# of skipped cells\n')

if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Local variables (temporary files):
Basin_DEM = 'C:\\NWS\\python\\temp_output\\'

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = "C:\\NWS\\python\\Model_Output.gdb" # temporary file storage directory
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
with arcpy.da.SearchCursor(in_shp, ("SHAPE@",find_ch5id,find_name)) as cursor: # search cursor gets "A geometry object for the feature" and the "NAME" attribute for each basin
    for index, row in enumerate(cursor): 
        Basin_Boundary = row[0] # basin geometry
        if len(row[1]) > 4:
            ch5id = row[1] # basin = find_ch5id
        elif len(row[2]) > 4:
            ch5id = row[2] # basin = find_name
        else:
            ch5id = row[1] # basin = find_ch5id
        print 'Processing basin: ' + str(ch5id)
        print 'ch5id = ' + row[1]
        print 'name = ' + row[2]
    
        # Process: Extract by Mask
        print 'Extract by mask...'
        arcpy.Clip_management(dem_file, "#", Basin_DEM+'x'+ch5id, Basin_Boundary, "0", "ClippingGeometry")
        #arcpy.gp.ExtractByMask_sa(dem_file, Basin_Boundary, Basin_DEM)
    
        # Process: Table to Table
        print 'Converting attribute table to text...'
        # Process: Table to Table
        arcpy.TableToTable_conversion(Basin_DEM+'x'+ch5id, output_dir, ch5id)
        basin_name = ch5id
        arcpy.TableToExcel_conversion(output_dir+ch5id+".dbf", output_hist+basin_name+".xls")
        proceed = 'yes'
    
#        else:
#            if ch5id in check_list:
#                basin_name = ch5id
#                if len(ch5id) <6:
#                    basin_name = ch5id + 'LOC'
#                arcpy.TableToExcel_conversion(output_dir+ch5id+".dbf", output_hist+basin_name+".xls")
#                proceed = 'yes'
        print basin_name
    
        # loop through and create data array for histogram/percentile calcs
        if proceed == 'yes':
            hist_array = []
            wb = xlrd.open_workbook(output_hist+basin_name+".xls")
            worksheet = wb.sheet_by_name(basin_name)
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1
            ##### define elevation zone ranges
            if basin_name[:5] in elev_splits: # search for 5 char basin id in split dictionary
                if basin_name[-1:] == 'U' or basin_name[-3:] == 'upr' or basin_name[-3:] == 'UPR':
                    min_elev = elev_splits[basin_name[:5]][-1]/3.28084
                    max_elev = 99999
                if basin_name[-2:] == 'MI' or basin_name[-3:] == 'mid' or basin_name[-3:] == 'MID':
                    min_elev = elev_splits[basin_name[:5]][-2]/3.28084
                    max_elev = elev_splits[basin_name[:5]][-1]/3.28084
                if basin_name[-1:] == 'L' or basin_name[-3:] == 'lwr' or basin_name[-3:] == 'LWR':
                    min_elev = elev_splits[basin_name[:5]][0]/3.28084
                    max_elev = elev_splits[basin_name[:5]][1]/3.28084
            elif basin_name in elev_splits: # search for full basin name (may be <> 5 characters)
                if basin_name[-1:] == 'U' or basin_name[-3:] == 'upr' or basin_name[-3:] == 'UPR':
                    min_elev = elev_splits[basin_name][-1]/3.28084
                    max_elev = 99999
                if basin_name[-2:] == 'MI' or basin_name[-3:] == 'mid' or basin_name[-3:] == 'MID':
                    min_elev = elev_splits[basin_name][-2]/3.28084
                    max_elev = elev_splits[basin_name][-1]/3.28084
                if basin_name[-1:] == 'L' or basin_name[-3:] == 'lwr' or basin_name[-3:] == 'LWR':
                    min_elev = elev_splits[basin_name][0]/3.28084
                    max_elev = elev_splits[basin_name][1]/3.28084
            else:
                max_elev = 99999; min_elev = 0
                print 'Splits not defined...'
            sum_skip = 0; total_cells = 0
            while curr_row < num_rows:
                curr_row += 1
                row = worksheet.row(curr_row)
                if curr_row >= 1: # ignore header
                    elev = int(worksheet.cell_value(curr_row,1))
                    count = int(worksheet.cell_value(curr_row,2))
                    if float(elev) >= min_elev and float(elev) <= max_elev:
                        hist_array.append([elev]*count)
                        total_cells += count
                    else:
                        sum_skip += count
            print 'Min elev: ' + str(min_elev) + ' <--> Max elev: ' + str(max_elev)
            print 'number of cells outside min/max range: ' + str(sum_skip)
            print 'cells within range: ' + str(total_cells) + '\n'
    
            hist_array = [item for sublist in hist_array for item in sublist] # flatten array
            out_chps = open(output_chps + basin_name + '.txt','w') # file to write chps ModuleParfile formatted data
            perc = 100.0
            chps_list = []; elev_list = []
            while perc >= 0:
                elev_perc = np.percentile(hist_array,perc)
                # check that the same elev level isn't already used as a percentile
                # check that percentile bounds are not duplicated for percents between 0-100
                if elev_perc not in elev_list and elev_perc != np.percentile(hist_array,0) and elev_perc != np.percentile(hist_array,100): 
                    chps_list.append('<row A="' + str("%.1f" % elev_perc) + '" B="'+str("%.2f" %(perc/100))+'"/>\n')
                    elev_list.append(elev_perc)
                # add 0% and 100% bounds
                if perc == 0 or perc == 100: 
                    chps_list.append('<row A="' + str("%.1f" % elev_perc) + '" B="'+str("%.2f" %(perc/100))+'"/>\n')
                    elev_list.append(elev_perc)
                if perc == 50.0:
                    medium_summary.write(basin_name.upper() + ',' + str("%.1f" % elev_perc) + ',' + str(total_cells) + ',' + str(sum_skip) + '\n')
                perc -= 10
    
            for each in chps_list[::-1]:
                out_chps.write(each)
            out_chps.close()
        
medium_summary.close()
print 'Completed!!' 
