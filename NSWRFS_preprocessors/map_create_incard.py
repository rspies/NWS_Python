# created by Ryan Spies 
# 4/13/2015
# Python 2.7
# Description: generate an input file with for the MAP preprocessor
# MAP input format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part3/_pdf/37map.pdf

import os
import dateutil
maindir = os.getcwd()
workingdir = maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep +'raw_data'

################### user input #########################
card_type = 'MAP' 
networks = ['raws_hourly','nhds_hourly','nhds_daily']  # choices: 'asos_hourly','nhds_daily','raws_hourly','scan_hourly'
state = 'AK'
daily_obs_file = workingdir + os.sep + 'nhds_daily' + os.sep + 'site_info_history.csv' # file with the obs time changes for some nhds stations
pxpp_output = workingdir + os.sep + 'MAP_input' + os.sep + 'pxpp_1960_2013_kusko_04242015_output.txt' # file with the pxpp output -> template for MAP input
map_weights = workingdir + os.sep + 'MAP_input' + os.sep + 'pre_weights' + os.sep # file with the pxpp output -> template for MAP input
out_file = open(workingdir + os.sep + 'MAP_input' + os.sep + 'MAP_KUSKO_BASINS_04242015.map','wb')
## define basins below
map_basins = ['MCGA2UPR','MCGA2LWR','MCGA2GL','KLCA2UPR','KLCA2LWR','CJXA2LWR','CJXA2UPR','CJXA2GL','ANKA2LWR','ANKA2UPR']
map_basins_desc = {'MCGA2UPR':'McGrath_Upper','MCGA2LWR':'McGrath_Lower','MCGA2GL':'McGrath_Glacier','KLCA2UPR':'Liskys_Upper','KLCA2LWR':'Liskys_Lower',
              'CJXA2LWR':'Crooked_Lower','CJXA2UPR':'Crooked_Upper','CJXA2GL':'Crooked_Glacier','ANKA2LWR':'Aniak_Lower','ANKA2UPR':'Aniak_Upper'}
map_basins_area = {'MCGA2UPR':4578,'MCGA2LWR':6753,'MCGA2GL':234,'KLCA2UPR':1028,'KLCA2LWR':3050,
              'CJXA2LWR':8846,'CJXA2UPR':6465,'CJXA2GL':143,'ANKA2LWR':2503,'ANKA2UPR':1905}
########################################################
print 'Creating file -> ' +  str(out_file)
################ A card block ####################
# data pulled from pxpp output punch file
open_pxpp = open(pxpp_output,'r')
for entry in open_pxpp:
    if entry[:2] == '@A':
        out_file.write(entry)
        break
open_pxpp.close()
################ B card block ####################
MAP_compute = len(map_basins); station_weight = 'PRE'; null = '0'; cont = 'CONT'; interval = '6'; adj = 'ADJ'; cons = 'SESN'
winter = 10; summer = 5; ctim = 'CTIM' # note: need n+1 commas for defaults (n is number of default variables)
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
    if line[:2] == '@D' or line[:2] == '@F' or line[:2] == '@G':
        out_file.write(line)
    if line[:2] == '@F':
        site_desc = str((line.split("'")[1]))
        stations_desc.append(site_desc)
    if line[:2] == '@G':
        site_name = str((line.split()[14]))
        stations_input.append(site_name)
open_pxpp.close()
################ I card block ####################
# area information and predetermined weights
for map_basin in map_basins:
    area_id = map_basin; area_desc = map_basins_desc[map_basin]; area = map_basins_area[map_basin]; area_units = 'MI2'; basin_name = 'KUSKO_BASINS'; file_name = area_id
    out_file.write('{:2s} {:12s} {:20s} {:5d} {:3s} {:12s} {:12s}'.format('@I',area_id,area_desc,area,area_units,basin_name,file_name))
    out_file.write('\n')
################ J card block ####################
# omit when using predetermined weights
################ L card block ####################
# only needed for predetermined weights
    count = 1
    out_file.write('@L\n')
    open_weights = open(map_weights + map_basin + '.csv','r')
    for each in open_weights:
        station = each.split(',')[0].strip()
        weight = each.split(',')[7].strip()
        if station != 'Station': #ignore header line in weight file
            if station == stations_input[count-1]: # check station order is correct
                if weight != '':
                    weight = float(weight)
                else:
                    weight = 0.0
                out_file.write('{:4.3f}'.format(weight))
                out_file.write(' ')
                if count % 10 == 0:
                    out_file.write('\n')
                count += 1
            else:
                print 'Station order differs from stations input...'
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
                        if station_input[:2] == 'AK': # ignores hourly NHDS sites ('ak')
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
    if entry[:2] == '@Q' or entry[:2] == 'AK' or entry[:2] == '@R' or entry[:2] == '@S' or entry[:2] == '  ':
        out_file.write(entry)
open_pxpp.close()
out_file.write('\n')
out_file.close()
print 'Completed!!'