# ---------------------------------------------------------------------------
# extract_basin_AEC_histogram.py
# Created and Modified by Ryan Spies (rspies@lynkertech.com)
# Date: 6/16/2015
# Description: clip DEM raster to basin/elev zone and convert attribute table
# to a .xls output for area elevation curve calculations
# ---------------------------------------------------------------------------
print 'Importing modules...'
# Import arcpy module
import arcpy
import xlrd
import numpy as np
import os
arcpy.env.overwriteOutput = True
os.chdir("../..")
maindir = os.getcwd()

################### User Input #####################
RFC = 'MBRFC_FY2015'
basins_folder = maindir + '\\' + RFC + '\\Shapefiles\\from_RFC\\missiouri_river_elev_zones\\' # missiouri_river, bighorn_elev_zones
dem_file = maindir + '\\GTOPO_1K_Hydro\\na_dem_null' # 1km resolution
#dem_file = r'Q:\GISLibrary\NHDPlus\v1\WG\NHDPlus12\Elev_Unit_d\elev_cm'
#dem_file = r'P:\NWS\GIS\APRFC\Processing\ASTER\kusk_mosiac.tif'
name_id_file = maindir + '\\' + RFC + '\\Elevation_Slope\\AEC\\basin_name_id.txt'
medium_summary = open(maindir + '\\' + RFC + '\\Elevation_Slope\\AEC\\median_elev_summary.csv','a')
output_dir = maindir + '\\' + RFC + '\\Elevation_Slope\\AEC\\raster_tables\\'
output_hist = maindir + '\\' + RFC + '\\Elevation_Slope\\AEC\\histograms\\'
output_chps = maindir + '\\' + RFC + '\\Elevation_Slope\\AEC\\chps_input\\'
sr = arcpy.SpatialReference(4269) # define projection of basin shp -> 4269 = GCS_North_American_1983

# manually enter basins to analyze (example: basins = ['MFDN3'])
# otherwise leave blank and script will
# analyze all basins in the basins_folder specified above
basins_overwrite = [] 
## basin splits defined by RFC (feet)
elev_splits = {'CLEM':[0,6500],'2870':[0,6000],'ADDM':[0,6000],'AGSM':[0,6500],'BTCM':[0,6000],'BULW':[0,7500,9500],'DBRM':[0,5000]
    ,'DCKW':[0,7500,9500],'DINW':[7500,9500],'DTTM':[0,6000],'DUBW':[0,7500,9500],'EDNM':[0,5500],'HLTM':[0,6000],'LPPM':[0,6000]
    ,'NFSM':[0,6500],'NFSW':[0,7500,9500],'SMHM':[0,6500],'SSNM':[0,6500],'TSFM':[0,6000],'ULLM':[0,5500],'VLYW':[0,7500,9500]
    ,'WLLM':[0,6000],'WRCW':[0,7500,9500]}
################# End User Input ######################
medium_summary.write('Basin,Medium Elev (m),# of DEM cells,# of skipped cells\n')

if not os.path.exists('C:\\NWS\\python\\temp_output\\'):
    print "Missing directory: 'C:\\NWS\\python\\temp_output\\' -> please create"
    raw_input("Press enter to continue processing...")
if not os.path.exists(output_dir):
    print "Missing directory: " + output_dir + " -> please create"
    raw_input("Press enter to continue processing...")

name_id = open(name_id_file,'r')
name_id_pair = {}; check_list = []
# Obtain basin name/id pairs for naming files
for line in name_id:
    each = line.split('\t')
    name_id_pair[each[1].rstrip()] = each[0].rstrip()
    check_list.append(each[0].rstrip())

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Local variables (temporary files):
Basin_DEM = 'C:\\NWS\\python\\temp_output\\'

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = "C:\\NWS\\python\\Model_Output.gdb" # temporary file storage directory
#arcpy.env.parallelProcessingFactor = "50"
print 'ok so far...'

# find all basins in RFC task or only run the specified basin overwrite list
basin_files = os.listdir(basins_folder) # list all basin shapefiles in the above specified directory
if len(basins_overwrite) != 0:
    basin_files = basins_overwrite      # use the basins_overright variable to run only specified basins instead of all RFC basins
basins = []
check_dir = os.listdir(output_dir)      # list all folders in output_dir
for each in basin_files:
    if each.split('.')[0] not in basins:
        if len(each.split('.')[0]) < 10:
            basins.append(each.split('.')[0])
            
for basin in basins:    
    print basin
    proceed = 'no'
    Basin_Boundary = basins_folder + '\\' + basin + '.shp'
    check_project = basins_folder + '\\' + basin + '.prj'

    # Process: Define Projection
    print 'Define Projection...'
    if not os.path.exists(check_project):
        arcpy.DefineProjection_management(Basin_Boundary, sr)
    
    # Process: Extract by Mask
    print 'Extract by mask...'
    arcpy.Clip_management(dem_file, "#", Basin_DEM+'x'+basin, Basin_Boundary, "0", "ClippingGeometry")
    #arcpy.gp.ExtractByMask_sa(dem_file, Basin_Boundary, Basin_DEM)

    # Process: Table to Table
    print 'Converting attribute table to text...'
    # Process: Table to Table
    arcpy.TableToTable_conversion(Basin_DEM+'x'+basin, output_dir, basin)
    if basin[:4] in name_id_pair:
        basin_name = name_id_pair[basin[:4]]+basin[4:]
        arcpy.TableToExcel_conversion(output_dir+basin+".dbf", output_hist+basin_name+".xls")
        proceed = 'yes'

    else:
        if basin in check_list:
            basin_name = basin
            if len(basin) <6:
                basin_name = basin + 'LOC'
            arcpy.TableToExcel_conversion(output_dir+basin+".dbf", output_hist+basin_name+".xls")
            proceed = 'yes'
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
        if basin_name[:4] in elev_splits:
            if basin_name[-1:] == 'U' or basin_name[-3:] == 'upr':
                min_elev = elev_splits[basin_name[:4]][-1]/3.28084
                max_elev = 99999
            if basin_name[-2:] == 'MI' or basin_name[-3:] == 'mid':
                min_elev = elev_splits[basin_name[:4]][-2]/3.28084
                max_elev = elev_splits[basin_name[:4]][-1]/3.28084
            if basin_name[-1:] == 'L' or basin_name[-3:] == 'lwr':
                min_elev = elev_splits[basin_name[:4]][0]/3.28084
                max_elev = elev_splits[basin_name[:4]][1]/3.28084
        else:
            max_elev = 99999; min_elev = 0
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
        print 'number of cells outside min/max range: ' + str(sum_skip)
        print 'cells within range: ' + str(total_cells) + '\n'

        hist_array = [item for sublist in hist_array for item in sublist] # flatten array
        out_chps = open(output_chps + basin_name + '.txt','w') # file to write chps ModuleParfile formatted data
        perc = 100.0
        chps_list = []; elev_list = []
        while perc >= 0:
            elev_perc = np.percentile(hist_array,perc)
            if elev_perc not in elev_list: # check that the same elev level isn't already used as a percentile
                chps_list.append('<row A="' + str("%.1f" % elev_perc) + '" B="'+str("%.2f" %(perc/100))+'"/>\n')
                elev_list.append(elev_perc)
            if perc == 50.0:
                medium_summary.write(basin_name.upper() + ',' + str("%.1f" % elev_perc) + ',' + str(total_cells) + ',' + str(sum_skip) + '\n')
            perc -= 10

        for each in chps_list[::-1]:
            out_chps.write(each)
        out_chps.close()
    
name_id.close()    
medium_summary.close()
print 'Completed!!' 
