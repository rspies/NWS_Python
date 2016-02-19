#_calculate_basin_nlcd_summary.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: calculates basin % land classification
#from .xls files output from ArcGIS Model Builder

#import script modules
import glob
import os
import re

import numpy
import csv

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC
RFC = 'WGRFC'
#FOLDER PATH OF NLCD .xls DATA FILES
csv_folderPath = r'P:\\NWS\\GIS\\WGRFC\\NLCD\\data_files\\'
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = r'P:\\NWS\\GIS\\WGRFC\\NLCD\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'

nlcd_file = open(output_folderPath + '_' + RFC + '_NLCD_Summary.csv', 'w')
nlcd_file.write('Basin,' + '%Open Water,' + '%Perennial Snow/Ice,' + \
                '%Developed Open Space,' + '%Developed Low Intensity,' + '%Developed Medium Intensity,' + '%Developed High Intensity,' + \
                '%Barren Land,' + '%Deciduous Forest,' + '%Evergeen Forest,' + '%Mixed Forest,' + '%Shrub/Scrub,' + '%Herbaceuous,' + \
                '%Hay/Pasture,' + '%Cultivated Crops,' + '%Woody Wetlands,' + '%Emergent Herbaceuous Wetlands,' + ',' + \
                '%Developed,' + '%Forest,' + '\n')

#loop through NLCD .xls files in folderPath
for filename in glob.glob(os.path.join(csv_folderPath, "*.csv")):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('_NLCD.csv', '')
    #print name

    txt_file = open(filename, 'r')

    #csv_file = open(r'P:\\NWS\\GIS\\NERFC\\APriori\\temp.csv', 'w')
    csv_file = open(output_folderPath + 'temp.csv', 'w')
    
    grid = []
    
    for line in txt_file:
        #print line
        csv_file.write(line)

    csv_file.close()
    txt_file.close()

    csv_file = open(output_folderPath + 'temp.csv')
    
    data_file = csv.reader(csv_file, delimiter = ',')
    data_file.next()

    Open_Water = []
    Perennial_SnowIce = []
    Developed_OpenSpace = []
    Developed_LowIntensity = []
    Developed_MediumIntensity = []
    Developed_HighIntensity = []
    Barren_Land = []
    Deciduous_Forest = []
    Evergreen_Forest = []
    Mixed_Forest = []
    Shrub_Scrub = []
    Herbaceuous = []
    Hay_Pasture = []
    Cultivated_Crops = []
    Woody_Wetlands = []
    Emergent_Herbaceuous_Wetlands = []

    Count = []

    #GET THE RASTER GRID COUNT OF EACH LAND CLASSIFICATION
    for row in data_file:
        LandCover = str(row[3])
        count = float(row[2])
        if LandCover == 'Open Water':
            Open_Water.append(count)
            Count.append(count)
        if LandCover == 'Perennial Snow/Ice':
            Perennial_SnowIce.append(count)
            Count.append(count)
        if LandCover == 'Developed, Open Space':
            Developed_OpenSpace.append(count)
            Count.append(count)
        if LandCover == 'Developed, Low Intensity':
            Developed_LowIntensity.append(count)
            Count.append(count)
        if LandCover == 'Developed, Medium Intensity':
            Developed_MediumIntensity.append(count)
            Count.append(count)
        if LandCover == 'Developed, High Intensity':
            Developed_HighIntensity.append(count)
            Count.append(count)
        if LandCover == 'Barren Land':
            Barren_Land.append(count)
            Count.append(count)
        if LandCover == 'Deciduous Forest':
            Deciduous_Forest.append(count)
            Count.append(count)
        if LandCover == 'Evergreen Forest':
            Evergreen_Forest.append(count)
            Count.append(count)
        if LandCover == 'Mixed Forest':
            Mixed_Forest.append(count)
            Count.append(count)
        if LandCover == 'Shrub/Scrub':
            Shrub_Scrub.append(count)
            Count.append(count)
        if LandCover == 'Herbaceuous':
            Herbaceuous.append(count)
            Count.append(count)
        if LandCover == 'Hay/Pasture':
            Hay_Pasture.append(count)
            Count.append(count)
        if LandCover == 'Cultivated Crops':
            Cultivated_Crops.append(count)
            Count.append(count)
        if LandCover == 'Woody Wetlands':
            Woody_Wetlands.append(count)
            Count.append(count)
        if LandCover == 'Emergent Herbaceuous Wetlands':
            Emergent_Herbaceuous_Wetlands.append(count)
            Count.append(count)

    #SUM THE NLCD GRID COUNTS
    OpenWater_sum = numpy.sum(Open_Water)
    Perennial_SnowIce_sum = numpy.sum(Perennial_SnowIce)
    Developed_OpenSpace_sum = numpy.sum(Developed_OpenSpace)
    Developed_LowIntensity_sum = numpy.sum(Developed_LowIntensity)
    Developed_MediumIntensity_sum = numpy.sum(Developed_MediumIntensity)
    Developed_HighIntensity_sum = numpy.sum(Developed_HighIntensity)
    Barren_Land_sum = numpy.sum(Barren_Land)
    Deciduous_Forest_sum = numpy.sum(Deciduous_Forest)
    Evergreen_Forest_sum = numpy.sum(Evergreen_Forest)
    Mixed_Forest_sum = numpy.sum(Mixed_Forest)
    Shrub_Scrub_sum = numpy.sum(Shrub_Scrub)
    Herbaceuous_sum = numpy.sum(Herbaceuous)
    Hay_Pasture_sum = numpy.sum(Hay_Pasture)
    Cultivated_Crops_sum = numpy.sum(Cultivated_Crops)
    Woody_Wetlands_sum = numpy.sum(Woody_Wetlands)
    Emergent_Herbaceuous_Wetlands_sum = numpy.sum(Emergent_Herbaceuous_Wetlands)

    Developed_sum = Developed_OpenSpace_sum + Developed_LowIntensity_sum + Developed_MediumIntensity_sum + Developed_HighIntensity_sum
    Forest_sum = Deciduous_Forest_sum + Evergreen_Forest_sum + Mixed_Forest_sum
    
    Count_sum = numpy.sum(Count)

    #CALCULATE PERCENT OF EACH NLCD
    OpenWater_percent = float(OpenWater_sum/Count_sum*100)
    Perennial_SnowIce_percent = float(Perennial_SnowIce_sum/Count_sum*100)
    Developed_OpenSpace_percent = float(Developed_OpenSpace_sum/Count_sum*100)
    Developed_LowIntensity_percent = float(Developed_LowIntensity_sum/Count_sum*100)
    Developed_MediumIntensity_percent = float(Developed_MediumIntensity_sum/Count_sum*100)
    Developed_HighIntensity_percent = float(Developed_HighIntensity_sum/Count_sum*100)
    Barren_Land_percent = float(Barren_Land_sum/Count_sum*100)
    Deciduous_Forest_percent = float(Deciduous_Forest_sum/Count_sum*100)
    Evergreen_Forest_percent = float(Evergreen_Forest_sum/Count_sum*100)
    Mixed_Forest_percent = float(Mixed_Forest_sum/Count_sum*100)
    Shrub_Scrub_percent = float(Shrub_Scrub_sum/Count_sum*100)
    Herbaceuous_percent = float(Herbaceuous_sum/Count_sum*100)
    Hay_Pasture_percent = float(Hay_Pasture_sum/Count_sum*100)
    Cultivated_Crops_percent = float(Cultivated_Crops_sum/Count_sum*100)
    Woody_Wetlands_percent = float(Woody_Wetlands_sum/Count_sum*100)
    Emergent_Herbaceuous_Wetlands_percent = float(Emergent_Herbaceuous_Wetlands_sum/Count_sum*100)

    Developed_percent = float(Developed_sum/Count_sum*100)
    Forest_percent = float(Forest_sum/Count_sum*100)

    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
    nlcd_file.write(name + ',' + str(OpenWater_percent) + ',' + str(Perennial_SnowIce_percent) + ',' + \
                    str(Developed_OpenSpace_percent) + ',' + str(Developed_LowIntensity_percent) + ',' + str(Developed_MediumIntensity_percent) + ',' + \
                    str(Developed_HighIntensity_percent) + ',' + str(Barren_Land_percent) + ',' + str(Deciduous_Forest_percent) + ',' + \
                    str(Evergreen_Forest_percent) + ',' + str(Mixed_Forest_percent) + ',' + str(Shrub_Scrub_percent) + ',' + \
                    str(Herbaceuous_percent) + ',' + str(Hay_Pasture_percent) + ',' +str(Cultivated_Crops_percent) + ',' + str(Woody_Wetlands_percent) + ',' \
                    + str(Emergent_Herbaceuous_Wetlands_percent) + ',,' + str(Developed_percent) + ',' + str(Forest_percent) + '\n')

    csv_file.close()  
nlcd_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
print 'nlcd Summary File is', nlcd_file
raw_input('Press Enter to continue...')
