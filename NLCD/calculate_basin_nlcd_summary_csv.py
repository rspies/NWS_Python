#_calculate_basin_nlcd_summary.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#modified by Ryan Spies to use .csv files from arcpy script
#Description: calculates basin % land classification
#from .csv files output from python arcpy

#import script modules
import glob
import os
import numpy
import csv
os.chdir("../..")
maindir = os.getcwd()

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC
RFC = 'APRFC_FY2017'
fx_group = '' # leave blank if not processing by fx group
#FOLDER PATH OF NLCD .csv DATA FILES
csv_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\NLCD\\data_files\\' + fx_group
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\NLCD\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'
if fx_group != '':
    nlcd_file = open(output_folderPath + RFC[:5] + '_' + fx_group + '_' + RFC[-6:] + '_NLCD_Summary.csv', 'w')
else:
    nlcd_file = open(output_folderPath + RFC + '_NLCD_Summary.csv', 'w')
if RFC == 'APRFC': # add Alaska only land cover classes
    nlcd_file.write('Basin,' + '%Open Water,' + '%Perennial Snow/Ice,' + \
                    '%Developed Open Space,' + '%Developed Low Intensity,' + '%Developed Medium Intensity,' + '%Developed High Intensity,' + \
                    '%Barren Land,' + '%Deciduous Forest,' + '%Evergreen Forest,' + '%Mixed Forest,' + '%Dwarf Scrub,' + '%Shrub/Scrub,' + '%Herbaceous,' + \
                    '%Sedge/Herbaceous,' + '%Lichens,' + '%Moss,' + '%Hay/Pasture,' + '%Cultivated Crops,' + '%Woody Wetlands,' + '%Emergent Herbaceous Wetlands,' + ',' + \
                    '%Developed,' + '%Forest,' + '\n')
else:
    nlcd_file.write('Basin,' + '%Open Water,' + '%Perennial Snow/Ice,' + \
                    '%Developed Open Space,' + '%Developed Low Intensity,' + '%Developed Medium Intensity,' + '%Developed High Intensity,' + \
                    '%Barren Land,' + '%Deciduous Forest,' + '%Evergreen Forest,' + '%Mixed Forest,' + '%Shrub/Scrub,' + '%Herbaceous,' + \
                    '%Hay/Pasture,' + '%Cultivated Crops,' + '%Woody Wetlands,' + '%Emergent Herbaceous Wetlands,' + ',' + \
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
    Dwarf_Scrub = []
    Shrub_Scrub = []
    Herbaceous = []
    Sedge = []
    Lichens = []
    Moss = []
    Hay_Pasture = []
    Cultivated_Crops = []
    Woody_Wetlands = []
    Emergent_Herbaceous_Wetlands = []

    Count = []

    #GET THE RASTER GRID COUNT OF EACH LAND CLASSIFICATION
    for row in data_file:
        LandCover = str(row[3])
        count = float(row[2])
        code = int(row[1])
        if LandCover == 'Open Water' or code == 11:
            Open_Water.append(count)
            Count.append(count)
        if LandCover == 'Perennial Snow/Ice' or code == 12:
            Perennial_SnowIce.append(count)
            Count.append(count)
        if LandCover == 'Developed, Open Space'or code == 22:
            Developed_OpenSpace.append(count)
            Count.append(count)
        if LandCover == 'Developed, Low Intensity'or code == 22:
            Developed_LowIntensity.append(count)
            Count.append(count)
        if LandCover == 'Developed, Medium Intensity'or code == 23:
            Developed_MediumIntensity.append(count)
            Count.append(count)
        if LandCover == 'Developed, High Intensity'or code == 24:
            Developed_HighIntensity.append(count)
            Count.append(count)
        if LandCover == 'Barren Land'or code == 31:
            Barren_Land.append(count)
            Count.append(count)
        if LandCover == 'Deciduous Forest' or code == 41:
            Deciduous_Forest.append(count)
            Count.append(count)
        if LandCover == 'Evergreen Forest' or code == 42:
            Evergreen_Forest.append(count)
            Count.append(count)
        if LandCover == 'Mixed Forest' or code == 43:
            Mixed_Forest.append(count)
            Count.append(count)
        if LandCover == 'Dwarf Scrub' or code == 51:
            Dwarf_Scrub.append(count)
            Count.append(count)
        if LandCover == 'Shrub/Scrub' or code == 52:
            Shrub_Scrub.append(count)
            Count.append(count)
        if LandCover == 'Herbaceous' or code == 71:
            Herbaceous.append(count)
            Count.append(count)
        if LandCover == 'Sedge/Herbaceous' or code == 72:
            Sedge.append(count)
            Count.append(count)
        if LandCover == 'Lichens' or code == 73:
            Lichens.append(count)
            Count.append(count)
        if LandCover == 'Moss' or code == 74:
            Moss.append(count)
            Count.append(count)
        if LandCover == 'Hay/Pasture' or code == 81:
            Hay_Pasture.append(count)
            Count.append(count)
        if LandCover == 'Cultivated Crops' or code == 82:
            Cultivated_Crops.append(count)
            Count.append(count)
        if LandCover == 'Woody Wetlands' or code == 90:
            Woody_Wetlands.append(count)
            Count.append(count)
        if LandCover == 'Emergent Herbaceous Wetlands' or code == 95:
            Emergent_Herbaceous_Wetlands.append(count)
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
    Dwarf_Scrub_sum = numpy.sum(Dwarf_Scrub)
    Shrub_Scrub_sum = numpy.sum(Shrub_Scrub)
    Herbaceous_sum = numpy.sum(Herbaceous)
    Sedge_sum = numpy.sum(Sedge)
    Lichens_sum = numpy.sum(Lichens)
    Moss_sum = numpy.sum(Moss)
    Hay_Pasture_sum = numpy.sum(Hay_Pasture)
    Cultivated_Crops_sum = numpy.sum(Cultivated_Crops)
    Woody_Wetlands_sum = numpy.sum(Woody_Wetlands)
    Emergent_Herbaceous_Wetlands_sum = numpy.sum(Emergent_Herbaceous_Wetlands)

    Developed_sum = Developed_OpenSpace_sum + Developed_LowIntensity_sum + Developed_MediumIntensity_sum + Developed_HighIntensity_sum
    Forest_sum = Deciduous_Forest_sum + Evergreen_Forest_sum + Mixed_Forest_sum
    
    Count_sum = numpy.sum(Count)

    #CALCULATE PERCENT OF EACH NLCD
    OpenWater_percent = float((OpenWater_sum/Count_sum)*100)
    Perennial_SnowIce_percent = float((Perennial_SnowIce_sum/Count_sum)*100)
    Developed_OpenSpace_percent = float((Developed_OpenSpace_sum/Count_sum)*100)
    Developed_LowIntensity_percent = float((Developed_LowIntensity_sum/Count_sum)*100)
    Developed_MediumIntensity_percent = float((Developed_MediumIntensity_sum/Count_sum)*100)
    Developed_HighIntensity_percent = float((Developed_HighIntensity_sum/Count_sum)*100)
    Barren_Land_percent = float((Barren_Land_sum/Count_sum)*100)
    Deciduous_Forest_percent = float((Deciduous_Forest_sum/Count_sum)*100)
    Evergreen_Forest_percent = float((Evergreen_Forest_sum/Count_sum)*100)
    Mixed_Forest_percent = float((Mixed_Forest_sum/Count_sum)*100)
    Dwarf_Scrub_percent = float((Dwarf_Scrub_sum/Count_sum)*100)
    Shrub_Scrub_percent = float((Shrub_Scrub_sum/Count_sum)*100)
    Herbaceous_percent = float((Herbaceous_sum/Count_sum)*100)
    Sedge_percent = float((Sedge_sum/Count_sum)*100)
    Lichens_percent = float((Lichens_sum/Count_sum)*100)
    Moss_percent = float((Moss_sum/Count_sum)*100)
    Hay_Pasture_percent = float((Hay_Pasture_sum/Count_sum)*100)
    Cultivated_Crops_percent = float((Cultivated_Crops_sum/Count_sum)*100)
    Woody_Wetlands_percent = float((Woody_Wetlands_sum/Count_sum)*100)
    Emergent_Herbaceous_Wetlands_percent = float((Emergent_Herbaceous_Wetlands_sum/Count_sum)*100)

    Developed_percent = float((Developed_sum/Count_sum)*100)
    Forest_percent = float((Forest_sum/Count_sum)*100)

    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
    if RFC == 'APRFC': # add Alaska only land cover classes
        nlcd_file.write(name + ',' + str(OpenWater_percent) + ',' + str(Perennial_SnowIce_percent) + ',' + \
                        str(Developed_OpenSpace_percent) + ',' + str(Developed_LowIntensity_percent) + ',' + str(Developed_MediumIntensity_percent) + ',' + \
                        str(Developed_HighIntensity_percent) + ',' + str(Barren_Land_percent) + ',' + str(Deciduous_Forest_percent) + ',' + \
                        str(Evergreen_Forest_percent) + ',' + str(Mixed_Forest_percent) + ',' + str(Dwarf_Scrub_percent) + ',' + str(Shrub_Scrub_percent) + ',' + \
                        str(Herbaceous_percent) + ',' + str(Sedge_percent) + ',' + str(Lichens_percent) + ',' + str(Moss_percent) + ',' + str(Hay_Pasture_percent) + ',' +str(Cultivated_Crops_percent) + ',' + str(Woody_Wetlands_percent) + ',' \
                        + str(Emergent_Herbaceous_Wetlands_percent) + ',,' + str(Developed_percent) + ',' + str(Forest_percent) + '\n')
    else:
        nlcd_file.write(name + ',' + str(OpenWater_percent) + ',' + str(Perennial_SnowIce_percent) + ',' + \
                        str(Developed_OpenSpace_percent) + ',' + str(Developed_LowIntensity_percent) + ',' + str(Developed_MediumIntensity_percent) + ',' + \
                        str(Developed_HighIntensity_percent) + ',' + str(Barren_Land_percent) + ',' + str(Deciduous_Forest_percent) + ',' + \
                        str(Evergreen_Forest_percent) + ',' + str(Mixed_Forest_percent) + ',' + str(Shrub_Scrub_percent) + ',' + \
                        str(Herbaceous_percent) + ',' + str(Hay_Pasture_percent) + ',' +str(Cultivated_Crops_percent) + ',' + str(Woody_Wetlands_percent) + ',' \
                        + str(Emergent_Herbaceous_Wetlands_percent) + ',,' + str(Developed_percent) + ',' + str(Forest_percent) + '\n')

    csv_file.close()  
nlcd_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
print 'nlcd Summary File is', nlcd_file
#raw_input('Press Enter to continue...')
