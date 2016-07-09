# Created on 2/19/2016
# @author: rspies (rspies@lynkertech.com)
# Python 2.7
# Loop through UNIT-HG CHPS ModuleParFiles and update the UHG ordinates
# uses xml ElementTree editor to parse xml files
# input a csv with the updated zone area and UHG oridinates 

import os

os.chdir("../..") # change dir to \\AMEC\\NWS
maindir = os.getcwd()

############ User input ################
RFC = 'MBRFC_FY2016'
fx_group = 'BigYel' # set to '' if not used
if fx_group != '':
    workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'unit_hydrographs' + os.sep + fx_group.lower() + os.sep
else:
    workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'unit_hydrographs' + os.sep
updated_uhg = workingdir + fx_group + '_new_unithg_ordinates_fix.csv'
output_dir = workingdir + 'modified_UH_06092016' + os.sep
log_file = workingdir + 'log.txt'
########################################

log = open(log_file,'w')
## read csv with update UHG ordinates and area for each basin/zone
basin_list = []; basin_area = {}; basin_ordinates = {}
csv_open = open(updated_uhg,'r')
for line in csv_open:
    split = line.split(',')
    name = split[1]; area = split[2]; ordinates = split[3:]
    if len(ordinates[0]) > 0 and str(area) != '0' and str(area) != 'area':
        basin_list.append(name)
        basin_area[name] = str("%.1f" % float(area))
        basin_ordinates[name] = ordinates
    elif len(ordinates[0]) > 0 and str(area) == '0':
        print 'Skipping basin: ' + name + '... missing area value (zone not used in config)'
        log.write('Skipping basin: ' + name + '... missing area value (zone not used in config?)\n')
    elif len(ordinates[0]) == 0 and str(area) != '0':
        print 'Skipping basin: ' + name + '... missing ordinates'
        log.write('Skipping basin: ' + name + '... missing ordinates from original UHG file\n')
csv_open.close()

# remove LOC basins that have UPR and LWR zones (LOC not used)
final_list = []
for each in basin_list:
    if each[-3:] == 'LOC':
        if each[:-3] + 'UPR' not in basin_list:
            final_list.append(each)
    if each[-3:] != 'LOC':
        final_list.append(each)
print final_list
    
#basin_list = ['BBRW4LWR'] # manually run individual basins

for basin in final_list:
    print 'Processing basin: ' + basin
    ch5id = basin[:5]
    if os.path.exists(workingdir + 'orig_sa_UH' + os.sep + 'UNITHG_' + ch5id + '_' + basin + '_UpdateStates.xml') == True:
        orig = open(workingdir + 'orig_sa_UH' + os.sep + 'UNITHG_' + ch5id + '_' + basin + '_UpdateStates.xml','r')
        #print 'found path'
    else:
        orig = open(workingdir + 'UNITHG_default_UpdateStates.xml','r')
        log.write(basin + ': original_SA_UHG file missing -> using default file') # use a default file for new basin (UHG parfile doesn't exist in SA)
    if not os.path.exists(output_dir + ch5id.lower()):
        os.makedirs(output_dir + ch5id.lower())
    new = open(output_dir + ch5id.lower() + os.sep + 'UNITHG_' + ch5id + '_' + basin + '_UpdateStates.xml', 'w')
    for line in orig:
        if 'id="DRAINAGE_AREA' in line:
            find_area = True
            new.write(line)
        elif 'dblValue' in line and find_area == True:
            sep = (line.replace('>',',').replace('</',',')).split(',')
            new.write(sep[0]+'>'+str(basin_area[basin])+'</'+sep[2]+'>\n')
            find_area = False
        elif '</table>' in line:
            uh_prev = 'x'
            for uh in basin_ordinates[basin]:
                if uh_prev != '"        <row A=""0.0""/>"':
                    new.write(uh.replace('""','"')[1:-1])
                    new.write('\n')
                    uh_prev = uh
            new.write(line)
        else:
            if '<row A=' not in line:
                new.write(line)
    
    orig.close()
    new.close()
log.close()
print 'Script completed!!'