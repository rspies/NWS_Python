# Created on September 19, 2014
# @author: rspies
# Python 2.7
# This script uses an .mxd and predefine layer files to export a png map
# image for each SAC-SMA parameter
# There must be an existing exported layer file for each param (proper label and symbology)

# Tip: the basin shapefile with the parameter values in the attribute table works best
# when the shapefile is an exported file (not a joined .shp file)

import arcpy
import os

########################### USER INPUT ################################
rfc = 'SERFC'
param_version = 'calb' # choices: 'sa' or 'calb;
out_dir = 'P:\\NWS\\GIS\\' + rfc + '\\map_output\\SAC_params_' + param_version
input_mxd = 'P:\\NWS\\GIS\\' + rfc + '\\SERFC_sac_params_' + param_version + '.mxd'
######################### END USER INPUT ##############################

avail_layers = os.listdir('P:\\NWS\\GIS\\' + rfc +'\\layer_files\\')
all_layers = []
for each in avail_layers:
    all_layers.append(each[9:-4])
variables = list(set(all_layers))
#variables = ['REXP'] # use this to run specific parameters
for variable in variables:
    print variable
    print 'Creating map jpeg...'
    mxd = arcpy.mapping.MapDocument(input_mxd)

    df_main = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
    #df_inset = arcpy.mapping.ListDataFrames(mxd, "Inset_Map")[0]

    if param_version == 'calb':
        updateLayer1 = arcpy.mapping.ListLayers(mxd, "all_basins_calb", df_main)[0]   # parameter shapefile
    if param_version == 'sa':
        updateLayer1 = arcpy.mapping.ListLayers(mxd, "all_basins_sa", df_main)[0]   # parameter shapefile
    #updateLayer2 = arcpy.mapping.ListLayers(mxd, "all_basins", df_main)[0]          
    #updateLayer3 = arcpy.mapping.ListLayers(mxd, "LMRFC_SERFC_all_inset", df_inset)[0]
    #updateLayer4 = arcpy.mapping.ListLayers(mxd, "LMRFC_all_calib_join_inset", df_inset)[0]

    sourceLayer1 = arcpy.mapping.Layer('P:\\NWS\\GIS\\' + rfc + '\\layer_files\\' + rfc + '_sa_' + variable + '.lyr')
    #sourceLayer2 = arcpy.mapping.Layer('P:\\NWS\\GIS\\' + rfc + '\\layer_files\\SERFC_calib_' + variable + '.lyr')

    #if updateLayer1.supports("LABELCLASSES"):
    lyr = updateLayer1
    for lblClass in lyr.labelClasses:
        if lblClass.showClassLabels:
            print "    Class Name:  " + lblClass.className
            #print "    Expression:  " + lblClass.expression
            print "    SQL Query:   " + lblClass.SQLQuery
            var_label = '[' + variable + ']'
            if variable[:2] == 'ET':
                var_label = '[' + variable[-3:] + '_ET' + ']' #layers use ET_XXX but table header is XXX_ET
            lblClass.expression =  var_label
            print "    Expression:  " + lblClass.expression
            lyr.showLabels = True
            arcpy.RefreshActiveView()
    
    arcpy.mapping.UpdateLayer(df_main, updateLayer1, sourceLayer1, True)
    #arcpy.ApplySymbologyFromLayer_management(updateLayer1, sourceLayer1)
    #arcpy.mapping.UpdateLayer(df_main, updateLayer2, sourceLayer2, False)
    #arcpy.mapping.UpdateLayer(df_inset, updateLayer3, sourceLayer1, False)
    #arcpy.mapping.UpdateLayer(df_inset, updateLayer4, sourceLayer2, False)

    arcpy.mapping.ExportToPNG(mxd, out_dir + '\\' + variable + '_' + param_version + '.png', resolution=150)
    del mxd, sourceLayer1

print 'Completed!'
print 'Check figures to ensure no basins are left white... if so rerun a couple individual parameters (seems to fix issue sometimes)'
