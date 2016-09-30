# created by Ryan Spies 
# rspies@lynkertech.com
# 2/23/2016
# Python 2.7
# Description: create a new ColdStateFiles directory by copying the old directory contents
# and replacing the params_previous.xml with a new file using the moduleparfile 
# Also copy the original statesI.txt to the new directory
# The script also renames the original ColdStateFiles directory to "ColdStateFiles_previous"
# and renames the new directory to "ColdStateFiles"

# Must be run from the main "/Config" directory

import os 
import shutil
import zipfile
maindir = os.getcwd()

########################### User Input ########################################
# original ColdStatesFiles directory
cold_dir = maindir + os.sep +'ColdStateFiles' 
# new ColdStatesFiles directory (e.g. ColdStatesFiles_updated)
new_cold_dir =  maindir + os.sep + 'updated_ColdStateFiles' 
# directory with the calibrated parameter mods (sub_directories: SAC_SMA, SNOW17, UH, Lag_K)
param_dir = maindir + os.sep +'updated_ModuleParFiles' + os.sep
######################### End User Input ######################################

for basin in os.listdir(cold_dir):
    print basin
    basin_dir = cold_dir + os.sep + basin
    # check if the new coldstatefiles directory contains the basin sub-directory
    # if the directory doesn't exist copy structure from the original ColdStateFiles directory
    new_basin_dir = new_cold_dir + os.sep + basin
    if os.path.exists(new_cold_dir + os.sep + basin) is False:
        shutil.copytree(basin_dir,new_basin_dir)
    else:
        print 'Directory already exsists: ' + new_basin_dir
    # loop through files in each zip file
    for zip_file in os.listdir(basin_dir):
        # grab the model component from zip file name -> use to locate mods and name files below
        model_name = ((zip_file.split())[0]).rstrip() + '.xml'
	model = model_name.split('_')[0]
        # locate the corresponding ModuleParFile from the exported mods directory
        add_file = param_dir + os.sep + model + os.sep + model_name
        if os.path.isfile(add_file) is True: 
	    # create new zip file to overwrite any existing zip files
            new_open_zip = zipfile.ZipFile(new_basin_dir + os.sep + zip_file,'w')
            open_zip = zipfile.ZipFile(basin_dir + os.sep + zip_file,'r')
            # add the .xml moduleparfile to the new zip file and rename 'params_previous.xml'
            new_open_zip.write(add_file, arcname = 'params_previous.xml')
            # extract the 'statesI.txt' from the original ColdStateFiles directory to the working dir (new_basin_dir)
            zip_files = open_zip.namelist()
            if 'statesI.txt' in zip_files:
                open_zip.extract('statesI.txt',new_basin_dir)
                # add the extracted 'statesI.txt' to the new zip file
                new_open_zip.write(new_basin_dir + os.sep +'statesI.txt', arcname = 'statesI.txt')
                # remove the extracted copy of 'statesI.txt' from the working dir (new_basin_dir)
                os.remove(new_basin_dir + os.sep +'statesI.txt')
            else:
                print 'statesI.txt not found in zip file: ' + basin + os.sep + model_name
        else:
            print 'ModuleParFile does not exsists: ' + basin + os.sep + model_name
        # close files
        open_zip.close()
        new_open_zip.close()

# rename directories to use the updated directory
#shutil.move(cold_dir, maindir + os.sep + 'ColdStateFiles_previous')
#shutil.move(new_cold_dir, maindir + os.sep + 'ColdStateFiles')
print 'Updated files to "ColdStateFiles" directory and renamed previous version "ColdStateFiles_previous"'

print 'Script Completed!'
    

