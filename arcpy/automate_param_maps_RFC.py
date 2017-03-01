# Created on July, 23 2015
# @author: rspies
# Python 2.7
# This script uses an .mxd and predefine layer files to export a png map
# image for each SAC-SMA parameter
# There must be an existing exported layer file for each param (proper label and symbology)

# Tip: the basin shapefile with the parameter values in the attribute table works best
# when the shapefile is an exported file (not a joined .shp file)
print 'Importing modules...'
import arcpy
import os
os.chdir("../..")
maindir = os.getcwd()
########################### USER INPUT ################################
rfc = 'LMRFC_FY2017'
fx_group = ''
param_version = 'draft' # choices: 'sa' or 'calb' or 'final' or 'draft';
labels = 'on' # choices: 'on' or 'off'
model = 'SACSMA' # choices: 'SACSMA' or 'SNOW17'
#input_mxd = 'P:\\NWS\\GIS\\' + rfc + '\\' + rfc + '_sac_params_' + param_version + '.mxd'
input_mxd = maindir +'\\GIS\\' + rfc[:5] + os.sep + rfc + '\\' + rfc[:5].lower() + '_fy17_' + param_version + '_param_map' + '.mxd'
######################### END USER INPUT ##############################
### output location
if fx_group != '':
    out_dir = maindir +'\\GIS\\' + rfc[:5] + os.sep + rfc + '\\map_output\\' + model + '_params_' + param_version + '\\' + fx_group
else:
    out_dir = maindir +'\\GIS\\' + rfc[:5] + os.sep + rfc + '\\map_output\\' + model + '_params_' + param_version
###

if not os.path.exists(out_dir): 
    print 'creating output directory: ' + str(out_dir)
    os.makedirs(out_dir)

print 'Finding list of parameters...'
layers_dir = maindir +'\\GIS\\' + rfc[:5] + os.sep + rfc + '\\layer_files\\' +  model + '\\'
avail_layers = os.listdir(layers_dir)
all_layers = []
for each in avail_layers:
    all_layers.append(each[9:-4])
variables = list(set(all_layers))

#variables = ['UZTWM'] # use this to run specific parameters
for variable in variables:
    print variable
    print 'Populating mxd...'
    mxd = arcpy.mapping.MapDocument(input_mxd)

    df_main = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
    df_inset = arcpy.mapping.ListDataFrames(mxd, "Inset_Map")[0]

    if param_version == 'final' or param_version == 'draft':
        updateLayer1 = arcpy.mapping.ListLayers(mxd, rfc[:5].lower() + '_' + param_version + "_" + model + "_params", df_main)[0]   # parameter shapefile
    if param_version == 'sa':
        updateLayer1 = arcpy.mapping.ListLayers(mxd, rfc[:5].lower() + '_' + "initial_params_0727", df_main)[0]   # parameter shapefile
    if param_version == 'final'or param_version == 'draft':
        updateLayer2 = arcpy.mapping.ListLayers(mxd, rfc[:5].lower() + '_' + param_version + "_" + model + "_params", df_inset)[0]   # parameter shapefile
    if param_version == 'sa':
        updateLayer2 = arcpy.mapping.ListLayers(mxd, rfc[:5].lower() + '_' + "initial_params_0727", df_inset)[0]   # parameter shapefile          
    
    sourceLayer1 = arcpy.mapping.Layer(layers_dir + rfc[:5] + '_sa_' + variable + '.lyr')
    #sourceLayer2 = arcpy.mapping.Layer(maindir +'\\GIS\\' + rfc + '\\layer_files\\SERFC_calib_' + variable + '.lyr')

    #if updateLayer1.supports("LABELCLASSES"):
    print 'Updating parameter labels...'
    lyr = updateLayer1
    for lblClass in lyr.labelClasses:
        if lblClass.showClassLabels:
            print "    Class Name:  " + lblClass.className
            print "    Expression:  " + lblClass.expression
            print "    SQL Query:   " + lblClass.SQLQuery
            var_label = '[' + variable + ']'
            if variable[:2] == 'ET':
                var_label = '[' + variable[-3:] + '_ET' + ']' #layers use ET_XXX but table header is XXX_ET
            lblClass.expression =  var_label
            print "    Expression:  " + lblClass.expression
            if labels == 'on':
                lyr.showLabels = True
            else:
                lyr.showLabels = False
            arcpy.RefreshActiveView()
    updateLayer2.showLables = False # not labels in inset map
    
    arcpy.mapping.UpdateLayer(df_main, updateLayer1, sourceLayer1, True)
    arcpy.mapping.UpdateLayer(df_inset, updateLayer2, sourceLayer1, True)
    #arcpy.ApplySymbologyFromLayer_management(updateLayer1, sourceLayer1)
    #arcpy.mapping.UpdateLayer(df_main, updateLayer2, sourceLayer2, False)
    #arcpy.mapping.UpdateLayer(df_inset, updateLayer3, sourceLayer1, False)
    #arcpy.mapping.UpdateLayer(df_inset, updateLayer4, sourceLayer2, False)
    print 'Creating map png...'
    arcpy.mapping.ExportToPNG(mxd, out_dir + '\\' + variable + '_' + param_version + '.png', resolution=220)
    del mxd, sourceLayer1

print 'Completed!'
print 'Check figures to ensure no basins are left white... if so rerun a couple individual parameters (seems to fix issue sometimes)'
