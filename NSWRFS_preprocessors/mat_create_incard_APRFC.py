# created by Ryan Spies 
# 3/24/2015
# Python 2.7
# Description: generate an input file with for the MAT preprocessor
# MAT input format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part3/_pdf/38mat.pdf

import os
import math
import dateutil
os.chdir("../..")
maindir = os.getcwd()

################### user input #########################
########################################################
RFC = 'APRFC_FY2017'
run_type = 'MAT' # choices: 'CONS' or 'MAT'
fxgroup = 'ANAK'
consis_check = 'off' # choices: 'on' or 'off' (on will generate consistency check card, off will generate MAT card)
year1 = 1960; year2 = 2015
networks = ['nhds_daily','raws_hourly']  # choices: 'asos_hourly','nhds_daily','raws_hourly','scan_hourly'

workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep + RFC[:5] + os.sep + RFC + os.sep + 'MAP_MAT_development' + os.sep + 'station_data'
daily_obs_file = workingdir + os.sep + 'nhds_daily' + os.sep + 'nhds_site_obs_time_' + fxgroup+ '.csv'      # file with the obs time changes for some nhds daily stations
limit_stations = [] #['PANI','PASV','5769','3009','3215','3573','0754','7570','7783','5366','AKIL','AMCK','APOO','ASTR','ATEL']
## define basins below
if fxgroup == 'ANAK':
    mat_basins = ['KNKA2LWR','KNKA2UPR','KNKA2GL'] #
if fxgroup == 'NWAK':
    mat_basins = ['ABLA2LWR','ABLA2UPR','KIAA2LWR','KIAA2UPR','WULA2LWR','WULA2UPR']
mat_basins_desc = {'ABLA2LWR':'ABLA2 LOWER','ABLA2UPR':'ABLA2 UPPER','KIAA2LWR':'KIAA2 LOWER','KIAA2UPR':'KIAA2 UPPER','WULA2LWR':'WULA2 LOWER'
                    ,'WULA2UPR':'WULA2 UPPER','KNKA2LWR':'KNKA2 LOWER','KNKA2UPR':'KNKA2 UPPER','KNKA2GL':'KNKA2 GLACIER'}
mat_basins_area = {'ABLA2LWR':4710,'ABLA2UPR':1701,'KIAA2LWR':2699,'KIAA2UPR':372,'WULA2LWR':440
                    ,'WULA2UPR':265,'KNKA2LWR':318,'KNKA2UPR':413,'KNKA2GL':488}
                    
if consis_check == 'on':
    mtp_basins = [fxgroup + '_consis_check']
    consis_input = 0
    out_ext = '_consis_check.mat'
    ctmp = ','; ctim = ',,'; cons = 'CONS'; cont = 'STOP' # @B CARD -- note: need n+1 commas for defaults (n is number of default variables)
    output_MAT = 'OUTN' # @D CARD input
else:
    consis_input = len(mat_basins)
    out_ext = '.mat'
    ctmp = 'CTMP'; ctim = 'CTIM'; cons = ',,'; cont = 'CONT' # @B CARD -- note: need n+1 commas for defaults (n is number of default variables)
    output_MAT = 'OUT' # @D CARD input
                    
dummy_file = workingdir + os.sep + 'MAT_input' + os.sep + fxgroup + '_dummy_station_input_info.csv'
########################################################
################## end user input #######################

if len(networks) > 1:
    out_file = open(workingdir + os.sep + 'MAT_input' + os.sep +  'MAT_input_'+fxgroup+'_' + str(year1) + '_' + str(year2) + out_ext,'wb')
else:
    out_file = open(workingdir + os.sep + 'MAT_input' + os.sep + 'MAT_' + networks[0] + '.mat','wb')
print 'Creating file -> ' +  str(out_file)
################ A card block ####################
month1 = 10; year1 = 1960; month2 = 9; year2 = 2015
out_file.write('{:2s} {:2d} {:4d} {:2d} {:4d}'.format('@A',month1,year1,month2,year2))
out_file.write('\n')
################ B card block ####################
MAT_compute = consis_input; tempck_num = 0; MAT_units = 'ENGL'; mnt = 'MNT'
# inputs for B card read from above -- dependant on consis_check vs MAT
out_file.write('{:2s} {:2d} {:2d} {:4s} {:3s} {:4s} {:4s} {:4s} {:4s}'.format('@B',MAT_compute,tempck_num,MAT_units,mnt,ctmp,ctim,cons,cont))
out_file.write('\n')
################ C card block ####################
# ignored for TEMPCK runs and consistency checks without MAT
#if tempck_num > 0 or MAT_compute == 0: 
weight_option = 'PRE' #default is grid -> ignores power
power = 2.0; min_power = 0.01
out_file.write('{:2s} {:4s} {:3.1f} {:4.2f}'.format('@C',weight_option,power,min_power))
out_file.write('\n')
################ D card block ####################
# ignored for TEMPCK runs and consistency checks without MAT
#if tempck_num > 0 or MAT_compute > 0: 
print_option = ','; null = ',,'; MAT_units = 'ENGL'; dir_name = 'FY17_CALB'; summary_table = 'SUMT'; summary_card = 'SUMP'
out_file.write('{:2s} {:4s} {:1s} {:4s} {:4s} {:10s} {:4s} {:4s}'.format('@D',print_option,null,output_MAT,MAT_units,dir_name,summary_table,summary_card))
out_file.write('\n')
################ E card block ####################
station_count = 0
for network in networks:
    if network == 'nhds_daily': # nhds_daily.taplot vs asos.taplot naming difference
        count_open = open(workingdir + os.sep + 'taplot_input' + os.sep + fxgroup + '_' + network + '.taplot','r')
    else:
        count_open = open(workingdir + os.sep + 'taplot_input' + os.sep + fxgroup + '_' + network + '.taplot','r')
    for line in count_open:
        station_count += int(line.split()[1])
        break
    count_open.close()
if len(limit_stations) > 0:
    station_count = len(limit_stations)
station_count += tempck_num # +1 for a tempck run?
if consis_check != 'on':
    station_count += len(mat_basins) # add dummy stations to count
if station_count > 50:
    print 'Warning -> more than 50 stations (limit of MAT)'
out_file.write('{:2s} {:2d}'.format('@E',station_count))
out_file.write('\n')
################ F/G/H card block ####################
stations_input = []; stations_available = {} # create a dictionary of available stations (name and id)
write_gh_cards = False # don't write G and H stations if station is not in limit_stations list (unless list is not used)
if len(limit_stations) == 0:
    add_station = True
else:
    add_station = False
for network in networks:
    line_prev = ''
    if network == 'nhds_daily': # nhds_daily.taplot vs asos.taplot naming difference
        taplot_open = open(workingdir + os.sep + 'taplot_input' + os.sep + fxgroup + '_' + network + '.taplot','r')
        summary_open = open(workingdir + os.sep + 'station_summaries' + os.sep +  'nhds_summary_tamx_daily_' + fxgroup + '.csv','r')
    else:
        taplot_open = open(workingdir + os.sep + 'taplot_input' + os.sep + fxgroup + '_' + network + '.taplot','r')
        summary_open = open(workingdir + os.sep + 'station_summaries' + os.sep + fxgroup + '_' + network[:4] + '_summary_tamx_hourly.csv','r')
    for entry in summary_open:
        sep = entry.split(',')
        if sep[0].strip() != 'NAME':
            stations_available[sep[0].upper()] = (str(sep[1])[-4:])
            if add_station == True:
                limit_stations.append(str(sep[1])[-4:])
    summary_open.close()
    for line in taplot_open: # F/G/H cards copied from taplot
        if line[:2] == '@F':
            site_name = (line.split("'")[1].replace(' ' + network[:4].upper(),'')).upper()
            if network[:4].upper() == 'SCAN':
                site_name = (line.split("'")[1].upper())
            if stations_available[site_name] in limit_stations: # check if station is specified as a final chosen site
                stations_input.append(stations_available[site_name])
                print 'Station added to output card: ' + stations_available[site_name]
                out_file.write(line)
                write_gh_cards = True
            else:
                write_gh_cards = False
        if line[:2] == '@G' or line[:2] == '@H':
            if write_gh_cards == True:
                out_file.write(line)
    taplot_open.close()
####### add dummy stations ########
if consis_check != 'on':
    open_dummy = open(dummy_file,'r'); check_basins = []; fe = 20.0
    for line in open_dummy:
        min_string = ''; max_string = '' # strings to append dummy station values from csv
        sep = line.split(',')
        if sep[0] != 'Basin':
            basin = sep[0]; lat = float(sep[2]); lon = float(sep[3]); elev = float(sep[4]); dummy = 'DUMMY'; obs_time = 24 # obs_time?
            for idx, val in enumerate(sep): # loop through all min/max values and append to appropriate string
                if idx > 4 and idx % 2 == True:
                    min_string = min_string + val.strip() + ' '
                if idx > 4 and idx % 2 == False:
                    max_string = max_string + val.strip() + ' '
            check_basins.append(basin)
            out_file.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d} {:5s}'.format('@F',"'"+str(basin + ' Synthetic')+"'",abs(float(lat)),abs(float(lon)),obs_time,int(elev),dummy))
            out_file.write('\n')            
            out_file.write('@G  ' + str(fe) + ' ' + max_string + '\n')
            out_file.write('@H  ' + str(fe) + ' ' + min_string + '\n')
    open_dummy.close()
    ################ I card block ####################
    # area information and predetermined weights
    if check_basins != mat_basins: # check order of syntetic stations matches order of basins
        print 'Order of MAT basins does not match order in synthetic info csv...'
    basin_index = len(stations_input)
    for mat_basin in check_basins:
        basin_index += 1
        area_id = mat_basin; area_desc = "'"+mat_basins_desc[mat_basin]+"'"; area = mat_basins_area[mat_basin]; area_units = 'MI2'; basin_name = 'FY17_CALB'; file_name = area_id
        out_file.write('{:2s} {:12s} {:20s} {:5d} {:3s} {:12s} {:12s}'.format('@I',area_id,area_desc,area,area_units,basin_name,file_name))
        out_file.write('\n')
    ################ J card block ####################
    # omit when using predetermined weights
        if weight_option != 'PRE': # omit J and L if not using pre-determined weights
            basn = 'BASN'; basin_id = 'MCGA2'; desc_info = 'test'; lat_lon_pairs = '(xxx.x,xxx.x)'
            out_file.write('{:2s} {:4s} {:8s} {:20s} {:13s}'.format('@J',area_id,area_desc,area,area_units,basin_name,file_name))
            out_file.write('\n')
    ################ L card block ####################
    # only needed for predetermined weights
        count = 1
        out_file.write('@L ')
        while count <= len(stations_input) + len(check_basins):
            if basin_index == count:
                weight = 1.0
            else:
                weight = 0.0
            out_file.write('{:4.2f}'.format(weight))
            out_file.write(' ')
            if count % 10 == 0:
                out_file.write('\n')
            count += 1
        out_file.write('\n')

################ M card block ####################
if ctim == 'CTIM': # omit unless observation time corrections specified in B card
    if 'nhds_daily' in networks:
        obs_time_file = open(daily_obs_file,'r')
        print 'Adding M block -> obs time history...'
        for station_num, station_input in enumerate(stations_input):
            obs_time_file = open(daily_obs_file,'r')
            prev_station = ''; prev_obs = ''
            for line in obs_time_file:
                sep = line.split(',')
                if sep[0] != 'COOP ID' and sep[0] != '':
                    site_id = str(sep[0])[-4:]
                    if site_id == station_input:
                        #print 'Obs time change found: ' + station_input
                        begin_date = dateutil.parser.parse(sep[1])
                        if sep[8] != '': # ignore missing obs time instances
                            time_obs = int(float(sep[8])/100)
                            if site_id == prev_station: # check for repeat obs_time instances for same site
                                if time_obs != prev_obs:
                                    out_file.write('@M ' + str(station_num + 1) + ' ' + str(begin_date.month) + ' ' + str(begin_date.year) + ' ' + str(time_obs) + '\n')
                            else:
                                out_file.write('@M ' + str(station_num + 1) + ' ' + str(begin_date.month) + ' ' + str(begin_date.year) + ' ' + str(time_obs) + '\n')
                            prev_station = site_id; prev_obs = time_obs
            obs_time_file.close()
        out_file.write('@M 999\n')
################ O card block ####################
if ctmp == 'CTMP': # omit unless temperature corrections specified in B card
    out_file.write('@O\n')
    out_file.write('@O  999\n')
################ Q card block ####################
out_file.write('@Q\n')
station_list = {}
for network in networks:
    if network == 'nhds_daily':
        for each_file in (os.listdir(workingdir + os.sep + network + os.sep + 'tamx' + os.sep + 'cardfiles'+ os.sep + fxgroup)):
            station_list[each_file[3:7]] = '/' + fxgroup + '/' + (each_file[:-4])

    else:
        for each_file in (os.listdir(workingdir + os.sep + network + os.sep + 'cardfiles_temp'+ os.sep + fxgroup)):
            if each_file[:-4] not in station_list:
                station_list[each_file[3:7]] =  '/' + fxgroup + '/' + (each_file[:-4])

for station in stations_input:
    if station in station_list:
        out_file.write('{:4s} {:20s}'.format('TAMX',station_list[station] + '.tmx'))
        out_file.write('\n')
        out_file.write('{:4s} {:20s}'.format('TAMN',station_list[station] + '.tmn'))
        out_file.write('\n')
        #print station_list[station]
################ R card block ####################
if cons == 'CONS': # omit unless consistency check option is specified in B card
    stations_group = station_count; number_groups = int(math.ceil(station_count/float(stations_group))) 
    out_file.write('{:2s} {:2d} {:2d}'.format('@R',number_groups,stations_group))
    out_file.write('\n')
################ S card block ####################
out_file.write('@S\n')
count_stations = 1
while count_stations <= len(stations_input):
    if (count_stations % 20) != False:
        out_file.write(str(count_stations) + ' ')
    else:
        out_file.write(str(count_stations) + '\n')
        #if count_stations != station_count:
            #out_file.write('@S ')
    count_stations += 1
out_file.write('\n')
out_file.write('@S\n')
################ T card block ####################
if tempck_num > 0: # only needed for a TEMPCK run
    out_file.write('@T\n')
out_file.close()
print 'MAT card completed!'
print 'Remember to add @O card manually!!!!!!!!!!!'
