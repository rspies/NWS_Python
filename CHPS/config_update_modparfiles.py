# created by Ryan Spies 
# rspies@lynkertech.com
# 12/8/2016
# Python 2.7
# Description: copy/updated updated ModuleParFiles to a config directory
# useful for moving new UHG files to the appropriate basin folder in the config

# Must be run from the main "/Config" directory

import os 
import shutil
import zipfile
maindir = os.getcwd()

########################### User Input ########################################
RFC = 'MBRFC'

# original ColdStatesFiles directory
updated_dir = 'D:\Projects\NWS\Calibration_NWS\MBRFC\MBRFC_FY2017\unit_hydrographs\modified_UHG\subbasins' 
# new ColdStatesFiles directory (e.g. ColdStatesFiles_updated)
config_dir =  'D:\Software\github_sync\FY17\mbrfc_calb_17\Config\ModuleParFiles' 

######################### End User Input ######################################
count = 0
if RFC not in updated_dir or RFC.lower() not in config_dir:
    print 'Check that updated and config directories are correct - ' + RFC + ' missing from dir structure'
else:
    for mod_file in os.listdir(updated_dir):
        if os.path.isfile(updated_dir + os.sep + mod_file): # check if item is a file (ignore directories)
            print mod_file
            basin = str(mod_file.split('_')[1])[:5] #limit basin name to 5 char id
            if os.path.exists(config_dir + os.sep + basin) is True: # check if basin dir exists in config
                if os.path.isfile(config_dir + os.sep + basin + os.sep + mod_file): # check if modparfile alreay exists in config (just a check)
                    print 'Replacing existing version of file...'
                shutil.copy(updated_dir + os.sep + mod_file,config_dir + os.sep + basin) # copy new modparfile to config basin dir
                count += 1
            else:
                print 'Basin Directory not found: ' + config_dir + os.sep + basin
    
print 'Copied ' + str(count) + ' files'
print 'Script Completed!'
    

