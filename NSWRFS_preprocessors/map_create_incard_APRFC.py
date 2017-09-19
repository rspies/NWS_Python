# created by Ryan Spies 
# 4/13/2015
# Python 2.7
# Description: generate an input file with for the MAP preprocessor
# MAP input format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part3/_pdf/37map.pdf

import os
import dateutil
os.chdir("../..")
maindir = os.getcwd()

################### user input #########################
RFC = 'APRFC_FY2017'
fxgroup = 'NWAK'
year1 = '1965'; year2 = '2010'
card_type = 'MAP' 
weight_type = 'SEAS' # choices: 'PRE' or 'SEAS'
consis_check = 'off' # choices: 'on' or 'off'
networks = ['nhds_hourly','nhds_daily','raws_hourly']         # choices: 'asos_hourly','nhds_daily','raws_hourly','scan_hourly'

workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep + RFC[:5] + os.sep + RFC + os.sep + 'MAP_MAT_development' + os.sep + 'station_data'
daily_obs_file = workingdir + os.sep + 'nhds_daily' + os.sep + 'nhds_site_obs_time_' + fxgroup+ '.csv'      # file with the obs time changes for some nhds daily stations
map_weights = workingdir + os.sep + 'MAP_input' + os.sep + 'pre_weights' + os.sep           # file with the pxpp output -> template for MAP input
basin_coords = workingdir + os.sep + 'MAP_input' + os.sep + 'vertices_summary.txt'

## define basins below ###
if fxgroup == 'ANAK':
    map_basins = ['KNKA2LWR','KNKA2UPR','KNKA2GL'] #
if fxgroup == 'NWAK':
    map_basins = ['ABLA2LWR','ABLA2UPR','KIAA2LWR','KIAA2UPR','WULA2LWR','WULA2UPR']
map_basins_desc = {'ABLA2LWR':'ABLA2 LOWER','ABLA2UPR':'ABLA2 UPPER','KIAA2LWR':'KIAA2 LOWER','KIAA2UPR':'KIAA2 UPPER','WULA2LWR':'WULA2 LOWER'
                    ,'WULA2UPR':'WULA2 UPPER','KNKA2LWR':'KNKA2 LOWER','KNKA2UPR':'KNKA2 UPPER','KNKA2GL':'KNKA2 GLACIER'}
map_basins_area = {'ABLA2LWR':4710,'ABLA2UPR':1701,'KIAA2LWR':2699,'KIAA2UPR':372,'WULA2LWR':440
                    ,'WULA2UPR':265,'KNKA2LWR':318,'KNKA2UPR':413,'KNKA2GL':488}
if consis_check == 'on':
    map_basins = [fxgroup + '_consis_check']
    consis_input = 0
    out_ext = '_consis_check.map'
else:
    consis_input = len(map_basins)
    out_ext = '.map'
########################################################

out_file = open(workingdir + os.sep + 'MAP_input' + os.sep + year1 + '-' + year2 + os.sep + 'MAP_input_'+fxgroup+'_' + year1 + '_' + year2 + '_' + weight_type + out_ext,'wb')
pxpp_output = workingdir + os.sep + 'MAP_input' + os.sep + year1 + '-' + year2 + os.sep + 'pxpp_punch' + os.sep + 'ptpx_' + fxgroup + '_breaks_pun.txt' # file with the pxpp output -> template for MAP input
print 'Creating file -> ' +  str('MAP_input_'+fxgroup+'_' + year1 + '_' + year2 + '.map')
################ A card block ####################
# data pulled from pxpp output punch file
open_pxpp = open(pxpp_output,'r')
for entry in open_pxpp:
    if entry[:2] == '@A':
        out_file.write(entry)
        break
open_pxpp.close()
################ B card block ####################
MAP_compute = consis_input; station_weight = weight_type; null = '0'; cont = 'CONT'; interval = '6'; adj = 'ADJ'; cons = 'SESN'
winter = 10; summer = 4; ctim = 'CTIM' # note: need n+1 commas for defaults (n is number of default variables)
out_file.write('{:2s} {:2d} {:4s} {:1s} {:4s} {:1s} {:3s} {:4s} {:2d} {:1d} {:4s}'.format('@B',MAP_compute,station_weight,null,cont,interval,adj,cons,winter,summer,ctim))
out_file.write('\n')
################ C card block ####################
mean_precip = 'NORM'; map_output = ''; prec_compare = ''
out_file.write('{:2s} {:4s} {:4s} {:4s}'.format('@C',mean_precip,map_output,prec_compare))
out_file.write('\n')
################ D/F/G card block ####################
# data pulled from pxpp output punch file
stations_input = []; stations_desc = [] # create a dictionary of available stations (name and id)
open_pxpp = open(pxpp_output,'r')
for line in open_pxpp:
    if line[:2] == '@D': # or line[:2] == '@F' or line[:2] == '@G':
        out_file.write(line)
    if line[:2] == '@F':
        site_desc = str((line.split("'")[1]))
        stations_desc.append(site_desc)
        f_line = line
    if line[:2] == '@G':
        g_line = line
        site_name = str((line.split()[-1]))
        stations_input.append(site_name)
        # find the initial observation time 
        obs_time_file = open(daily_obs_file,'r')
        time_obs = '7.' # default obs time if 
        if site_name[:2].isupper() == True: # ignores hourly NHDS sites ('ak') -> set to 0. obs time
            for inst in obs_time_file:
                sep = inst.split(',')
                if sep[0] != 'COOP ID' and sep[0] != '':
                    site_id = str(sep[0])[-4:]
                    if site_id == site_name[-4:]:
                        if sep[9] != '': # ignore missing obs time instances
                            time_obs = str(int(float(sep[9])/100))
                            if len(time_obs) == 1:
                                time_obs = time_obs + '.'
                            break # only find the first instance of obs time -> M card will correct obs time changes
            f_line = f_line.rstrip('\n') + '    ' + time_obs + '\n'
        out_file.write(f_line)
        out_file.write(g_line[:3])
        ## added below block to add spacing for monthly station climo values > 9.99 (prevent data overlapping?)
        parse_line = g_line[3:63]
        mclimos = [parse_line[i:i+5] for i in range(0, len(parse_line), 5)]
        extra_space = 4 # use this to determine if previous line was 5 or 4 chars
        for i, value in enumerate(mclimos):
            if extra_space == 5 and len(value.replace(' ','')) == 5:
                out_file.write(' ')
            elif i > 0 and extra_space == 4 and len(value.replace(' ','')) == 5:
                out_file.write(' ')
            out_file.write(value)
            extra_space = len(value.replace(' ',''))
        out_file.write(g_line[64:])
        obs_time_file.close()
        
open_pxpp.close()
################ I card block ####################
# area information and predetermined weights
for map_basin in map_basins:
    if MAP_compute > 0: # only add @I card for MAP generation run - not consistency check run
        area_id = map_basin; area_desc = map_basins_desc[map_basin].replace(' ','_'); area = map_basins_area[map_basin]; area_units = 'MI2'; basin_name = 'FY17_CALB'; file_name = area_id
        out_file.write('{:2s} {:12s} {:20s} {:5d} {:3s} {:12s} {:12s}'.format('@I',area_id,area_desc,area,area_units,basin_name,file_name))
        out_file.write('\n')
################ J card block ####################
# omit when using predetermined weights
    if station_weight == 'THIE' or station_weight == 'GRID':
        #base_units = 'ENGL'; 
        #out_file.write('{:2s} {:4s} {:8s} {:20s} {:3s} {:12s} {:12s}'.format('@J',base_units,map_basin,area_desc))
        out_file.write('{:2s} '.format('@J'))
        out_file.write('(')
        find_coords = open(basin_coords,'r')
        for line in find_coords:
            sep = line.split('\t'); coord_count = 1
            if sep[0] == map_basin:
                for pair in sep[2:-1]:
                    out_file.write('{:11s}'.format((pair.rstrip('\n')).replace(' ','0')))
                    if coord_count == len(sep[2:-1]):
                        out_file.write(')\n')
                    elif coord_count % 5 == 0 and coord_count > 1:
                        out_file.write('\n    ')
                    else:
                        out_file.write('   ')
                    coord_count += 1
        find_coords.close()
################ L card block ####################
# only needed for predetermined weights
   #### Annual Weights ######
    if station_weight == 'PRE' and consis_check != 'on':
        count = 1; wpairs = {}
        out_file.write('@L\n')
        open_weights = open(map_weights + map_basin + '.csv','r')
        for each in open_weights:
            if each.split(',')[0].strip() != 'Station': # skip header line
                station = each.split(',')[0].strip()
                weight = each.split(',')[7].strip()
                wpairs[station] = weight
        if len(wpairs) != len(stations_input):
            print '!!! Number of stations specified if @F/@G not equal to num of stations in weights csv!!!'
        for point in stations_input: # iterate @F/@G stations
            if point in wpairs: # check station is list in pre weights csv
                idweight = wpairs[point]
                if idweight == '' or idweight == '\n':
                    idweight = 0.0
                out_file.write('{:4.3f}'.format(float(idweight)))
                out_file.write(' ')
                if count % 10 == 0:
                    out_file.write('\n')
                count += 1
            else:
                print '!!!! Station/weight not found --> ' + point
        out_file.write('\n')
        print 'Added pre-determined weights for: ' + map_basin
   #### Season weights used instead of annual weights ##########
    if station_weight == 'SEAS' and consis_check != 'on':
        count = 1; wpairs = {}; spairs = {}
        out_file.write('@L\n')
        wopen_weights = open(map_weights + 'winter' + os.sep + map_basin + '.csv','r')
        for each in wopen_weights: # loop winter weights csv
            if each.split(',')[0].strip() != 'Station': # skip header line
                station = each.split(',')[0].strip()
                weight = each.split(',')[7].strip()
                wpairs[station] = weight
        if len(wpairs) != len(stations_input):
            print '!!! Number of stations specified in @F/@G not equal to num of stations in weights csv!!!'
        sopen_weights = open(map_weights + 'summer' + os.sep + map_basin + '.csv','r')
        for each in sopen_weights: # loop summer weights csv
            if each.split(',')[0].strip() != 'Station': # skip header line
                station = each.split(',')[0].strip()
                weight = each.split(',')[7].strip()
                spairs[station] = weight
        if len(spairs) != len(stations_input):
            print '!!! Number of stations specified in @F/@G not equal to num of stations in weights csv!!!'
        ### add station weights to card file ####
        for point in stations_input: # iterate @F/@G stations
            if point in wpairs: # check station is list in pre weights csv
                idweight = wpairs[point]
                if idweight == '' or idweight == '\n':
                    idweight = 0.0
                out_file.write('{:4.3f}'.format(float(idweight)))
                out_file.write(' ')
                if count % 10 == 0:
                    out_file.write('\n')
                count += 1
            else:
                print '!!!! Winter Station/weight not found --> ' + point
        for point in stations_input: # iterate @F/@G stations
            if point in spairs: # check station is list in pre weights csv
                idweight = spairs[point]
                if idweight == '' or idweight == '\n':
                    idweight = 0.0
                out_file.write('{:4.3f}'.format(float(idweight)))
                out_file.write(' ')
                if count % 10 == 0:
                    out_file.write('\n')
                count += 1
            else:
                print '!!!! Summer Station/weight not found --> ' + point
        out_file.write('\n')
        print 'Added pre-determined weights for: ' + map_basin
################ M card block ####################
if ctim == 'CTIM': # omit unless observation time corrections specified in B card
    if 'nhds_daily' in networks:
        print 'Adding M block - obs time history...'
        for station_num, station_input in enumerate(stations_input):
            obs_time_file = open(daily_obs_file,'r')
            prev_station = ''; prev_obs = ''
            for line in obs_time_file:
                sep = line.split(',')
                if sep[0] != 'COOP ID' and sep[0] != '':
                    site_id = str(sep[0])[-4:]
                    if site_id == station_input[-4:]:
                        if station_input[:2].isupper() == True: # ignores hourly NHDS sites ('ak')
                            #print 'Obs time change found: ' + station_input
                            begin_date = dateutil.parser.parse(sep[1])
                            if sep[9] != '': # ignore missing obs time instances
                                time_obs = int(float(sep[9])/100)
                                if site_id == prev_station: # check for repeat obs_time instances for same site
                                    if time_obs != prev_obs:
                                        out_file.write('@M ' + str(station_num + 1) + ' ' + str(begin_date.month) + ' ' + str(begin_date.year) + ' ' + str(time_obs) + '\n')
                                else:
                                    out_file.write('@M ' + str(station_num + 1) + ' ' + str(begin_date.month) + ' ' + str(begin_date.year) + ' ' + str(time_obs) + '\n')
                                prev_station = site_id; prev_obs = time_obs
            obs_time_file.close()
        out_file.write('@M 999\n')
################ O/Q/R/S card block ####################
# data pulled from pxpp output punch file
# O card only used when ADJ specified in B card
if adj == 'ADJ':
    open_pxpp = open(pxpp_output,'r')
    for entry in open_pxpp:
        if entry[:2] == '@O':
            if entry[:5] == '@O 99':
                out_file.write('@O 999\n')
            else:
                out_file.write(entry)
    open_pxpp.close()
open_pxpp = open(pxpp_output,'r')
for entry in open_pxpp:
    if entry[:2] == '@Q' or entry[:4] == 'NHDS' or entry[:4] == 'USGS' or entry[:1] == '/' or entry[:2] == '@R' or entry[:2] == '@S' or entry[:2] == '  ':
        out_file.write(entry)
open_pxpp.close()
out_file.write('\n')
out_file.close()
print 'Completed!!'