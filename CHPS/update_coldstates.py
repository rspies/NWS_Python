# created by Ryan Spies 
# 3/5/2015
# Python 2.7
# Description: create a new ColdStateFiles directory by copying the old directory
# and replace the zip file with a new file containg the moduleparfile from 
# from the exported calibration mod and a copy of the original statesI.txt
# Key features: extracts file from zip file, creates new zip file, checks if directory exists,
# check if file exists, copy directory tree

import os 
import shutil
import zipfile
os.chdir("../..")
maindir = os.getcwd()

########################### User Input ########################################
RFC = 'NERFC_FY2016'
calb_type = 'final' # choices: 'initial', 'draft', 'final'
# original ColdStatesFiles directory
cold_dir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep +'ColdStateFile_updates' + os.sep + 'ColdStateFiles_01292016' + os.sep 
# new ColdStatesFiles directory (e.g. ColdStatesFiles_updated)
new_cold_dir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep +'ColdStateFile_updates' + os.sep + 'updated_ColdStateFiles' + os.sep 
# directory with the calibrated parameter mods (sub_directories: SAC_SMA, SNOW17, UH, Lag_K)
param_dir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Working_Calib_Files' + os.sep + calb_type + '_calb' + os.sep
######################### End User Input ######################################

for basin in os.listdir(cold_dir):
    print basin
    basin_dir = cold_dir + basin
    # check if the new coldstatefiles directory contains the basin sub-directory
    # if the directory doesn't exist copy structure from the original ColdStateFiles directory
    new_basin_dir = new_cold_dir+basin
    if os.path.exists(new_cold_dir+basin) is False:
        shutil.copytree(basin_dir,new_basin_dir)
    else:
        print 'Directory already exsists: ' + new_basin_dir
    # loop through files in each zip file
    for zip_file in os.listdir(basin_dir):
        # grab the model component from zip file name -> use to locate mods and name files below
        if zip_file[:3] == 'LAG':
            model_name = ((zip_file.split())[0]).rstrip() + '.xml'
            model_dir = 'Lag_K'
        elif zip_file[:3] == 'SAC':
            model_name = ((zip_file.split())[0]).rstrip() + '.xml'
            model_dir = 'SAC_SMA'
        elif zip_file[:3] == 'SNO':
            model_name = ((zip_file.split())[0]).rstrip() + '.xml'
            model_dir = 'SNOW17'
        elif zip_file[:3] == 'RSN':
            model_name = ((zip_file.split())[0]).rstrip() + '.xml'
            model_dir = 'RSNWELEV'
        elif zip_file[:3] == 'UNI':
            model_name = ((zip_file.split())[0]).rstrip() + '.xml'
            model_dir = 'UH'
        elif zip_file[:3] == 'GLA':
            model_name = ((zip_file.split())[0]).rstrip() + '.xml'
            model_dir = 'Glacier'
        else:
            print 'Unknown zip file...' + str(zip_file)
            model_dir = ''; model_name = 'na'
        # create new zip file to overwrite any existing zip files
        new_open_zip = zipfile.ZipFile(new_basin_dir + os.sep + zip_file,'w')
        open_zip = zipfile.ZipFile(basin_dir + os.sep + zip_file,'r')
        # locate the corresponding ModuleParFile from the exported mods directory
        add_file = param_dir + model_dir + os.sep + model_name
        if os.path.isfile(add_file) is True: 
            # add the .xml moduleparfile to the new zip file and rename 'params_previous.xml'
            new_open_zip.write(add_file, arcname = 'params_previous.xml')
            # extract the 'statesI.txt' from the original ColdStateFiles directory to the working dir (new_basin_dir)
            open_zip.extract('statesI.txt',new_basin_dir)
            # add the extracted 'statesI.txt' to the new zip file
            new_open_zip.write(new_basin_dir + os.sep +'statesI.txt', arcname = 'statesI.txt')
            # remove the extracted copy of 'statesI.txt' from the working dir (new_basin_dir)
            os.remove(new_basin_dir + os.sep +'statesI.txt')
        else:
            print 'ModuleParFile does not exsists: ' + add_file
        # close files
        open_zip.close()
        new_open_zip.close()

print 'Completed!'
    

