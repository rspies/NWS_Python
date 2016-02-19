# created by Ryan Spies 
# 3/5/2015
# Python 2.7
# Description: parse through UHG .xml parameter files and create a new file with
# ordinates rounded to whole numbers (CHPS version currently leaves multiple decimals)

import os 
import glob
os.chdir("../..")
maindir = os.getcwd()

###############################################################################
RFC = 'APRFC_FY2015'
working_dir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC + os.sep + 'Working_Calib_Files' + os.sep + 'UH' + os.sep
original_files = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC + os.sep + 'Working_Calib_Files' + os.sep + 'UH_original_decimals' + os.sep
###############################################################################

for each in glob.glob(original_files+'/*.xml'):
    print os.path.basename(each)
    file_name = os.path.basename(each)
    read_orig = open(each,'r')
    new_file =open(working_dir + file_name,'w')
    for line in read_orig:
        if '<row A' not in line:
            new_file.write(line)
        else:
            sep = line.split('"')
            rounded = round(float(sep[1]),-1)
            new_file.write(sep[0] + '"' + "%.1f" % rounded + '"' + sep[2])    
    read_orig.close()
    new_file.close()
print 'Completed!'
        

