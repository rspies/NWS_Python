# created by Ryan Spies 
# 3/11/2015
# Python 2.7
# Description: generate an input file with the pxpp station data using the summary
# file and a list of the cardfiles
# pxpp input format: http://www.nws.noaa.gov/oh/hrl/nwsrfs/users_manual/part3/_pdf/37pxpp.pdf

import os
import os.path
os.chdir("../..")
maindir = os.getcwd()

################### user input #########################
variable = 'ptpx'  # choices: 'ptpx'
RFC = 'SERFC_FY2016'
linux_dir = ''
networks = ['nhds_daily','nhds_hourly','usgs_daily']  # choices: 'raws_hourly','asos_hourly','nhds_daily','nhds_hourly','scan_hourly','CONAGUA'
########################################################

state_abbr = {'50':'AK','41':'TX','29':'NM','01':'AL','09':'GA','31':'NC','38':'SC','40':'TN','44':'VA'}
workingdir = maindir + os.sep + 'Calibration_NWS'+ os.sep + RFC[:5] + os.sep + RFC + os.sep +'station_data'
basin_stations_file = workingdir + os.sep + 'basin_stations.csv'

basin_file = open(basin_stations_file,'r')
basin_list = []; basin_base_site = {}; basin_stations = {}
for line in basin_file:
    items = line.split(',')
    if items[0] != 'Basin':
        ch5id = items[0]
        basin_list.append(ch5id)
        basin_base_site[ch5id] =items[1]
        basin_stations[ch5id]=[]
        for each in items[2:]:
            basin_stations[ch5id].append(each.rstrip('\n'))
basin_file.close()
#basin_list = ['WODS1']
for basin in basin_list:
    print 'Creating pxpp file for ' + basin

    ### header ###
    month1 = 1; year1 = 1950; month2 = 9; year2 = 2014; base_station = basin_base_site[basin] # base station defined in basin stations csv
    out_file = open(workingdir + os.sep + 'pxpp_input' + os.sep + str(year1) + '-' + str(year2) + os.sep + basin + '_pxpp_' + str(year1) + '_' + str(year2) + '_02122016.txt','wb')
    final_summary = open(workingdir + os.sep + 'pxpp_input' + os.sep + str(year1) + '-' + str(year2) + os.sep + basin + '_pxpp_station_' + str(year1) + '_' + str(year2) + '_summary.csv','wb')
    lat_lon_default = ' '; obs_time_daily = 17; elev_units = 'FT'; winter = 11; summer = 3
    out_file.write('{:5d}{:5d}{:5d}{:5d}  {:8s}  {:4s}  {:2d} {:4s}{:5d}{:5d}'.format(
    month1,year1,month2,year2,base_station,lat_lon_default,obs_time_daily,elev_units,winter,summer))
    out_file.write('\n')
    corr_tables = 'YEAR'; cons_plot = 'YEAR'; cons_date = 'YES'; prec_summary = 'YES'; prec_units = 'IN'; MAP_output = 1; MAP_monthly = 1
    out_file.write('{:4s} {:4s} {:4s} {:4s} {:4s}     {:1d}    {:1d}'.format(
    corr_tables,cons_plot,cons_date,prec_summary,prec_units,MAP_output,MAP_monthly))
    out_file.write('\n')
    station_list = []; count_summary = 1
    ### end header ###
    for network in networks:
        timestep = network.split('_')[1]
        if network[:4] == 'raws' or network[:4] == 'asos' or network[:4] == 'scan':
            card_dir = workingdir + os.sep + network +os.sep + 'cardfiles_ptpx' + os.sep
            station_file =  workingdir + os.sep + network[:4] + '_summary_' + variable + '_' + timestep + '.csv'
            ignore_file = workingdir + os.sep + network[:4] + '_all'  + '_ignore_stations.csv'
        if network[:4] == 'nhds' or network[:4] == 'usgs':
            card_dir = workingdir + os.sep + network[:4] + '_' + timestep +os.sep + variable + os.sep + 'cardfiles' + os.sep
            station_file =  workingdir + os.sep + 'station_summaries' + os.sep + network[:4] + '_summary_' + variable + '_' + timestep + '_all.csv'
            ignore_file = workingdir + os.sep + network[:4] + '_all'  + '_ignore_stations.csv'
        if network[:4] == 'CONA':
            card_dir = workingdir + os.sep + 'CONAGUA'  + os.sep + variable + os.sep + 'cardfiles' + os.sep + timestep + os.sep
            station_file =  workingdir + os.sep + network.split('_')[0] + '_summary_' + variable + '_' + timestep + '.csv'
            ignore_file = workingdir + os.sep + network.split('_')[0] + '_all'  + '_ignore_stations.csv'
    
        ### create list of stations that will not be processed ###
        ignore_list = ['SC6657','SC3742','sc3742','VA8241','VA8249','va8249','GA8854','GA7499'] # these stations were reported by pxpp to "HAVE INSUFFICIENT DATA TO ESTIMATE MISSING MONTHS" or user defined sites to leave out of processing
        if os.path.isfile(ignore_file) == True:
            ignore_sites = open(ignore_file,'r')
            for each in ignore_sites:
                ignore_list.append(each.strip())
            ignore_sites.close()
        else:
            print 'Ignore station file not used...'
            ignore_sites = []
        ### station info ###
        card_names = os.listdir(card_dir)
        open_summary = open(station_file,'r')
    
        for line in open_summary:
            if network == networks[0] and count_summary == 1:
                # write header line to output summary file
                final_summary.write(line.strip('\n') + ',' + 'TIME_STEP' + ',' + 'ID\n')
                count_summary += 1
            sep = line.split(',')
            state_num = (sep[1])[:2]
            #print sep[1]
            if sep[0] != 'NAME': # ignore header line
                if sep[1] in basin_stations[basin]: # check if station is included in basin-station list
                    if network.split('_')[0] == 'CONAGUA':
                        state = 'MX'
                    else:
                        state = state_abbr[state_num]
                    if timestep == 'hourly': # name duplicate NHDS hourly stations with lower case state (hourly/daily issue)
                        site_id = state.lower() + str(sep[1].split(' ')[-1])
                    else:
                        site_id = state + str(sep[1].split(' ')[-1])
                    file_check = state + '-' + str(sep[1].split(' ')[-1]) # use the site id to search for corresponding card file below
                    #print file_check
                    if site_id not in ignore_list:   # ignore specified stations 
                        print 'SITE ----> ' + site_id
                        for each in os.listdir(card_dir + os.sep + state):
                            if file_check in each:
                                station_list.append(site_id)
                                file_name = each
                                print file_name
                                name = (sep[0])[:22] + ' ' + network[:4].upper();lat = sep[2]; lon = abs(float(sep[3].strip('-'))); elev = sep[4]
                                file_type = 'CARD'
                                if timestep == 'daily':
                                    time_int = 24
                                if timestep == 'hourly':
                                    time_int = 1
                                out_file.write('{:8s}   {:8.4f} {:8.4f}  {:6.0f}  {:2d}    {:4s}    {:20s}'.format(
                                site_id,float(lat),float(lon),float(elev),time_int,file_type,name))
                                out_file.write('\n')
                                out_file.write(linux_dir+network[:4].upper()+'_'+timestep+'/'+state+'/'+file_name)
                                out_file.write('\n')
                                final_summary.write(line.strip('\n').rstrip(',') + ',' + timestep + ',' + site_id + '\n')
                
    out_file.write('ENDSTAN\n')
    ### end station info ###
    
    ### corrections ###
    out_file.write('ENDCORR\n')
    ### end corrections ### 
       
    ### group stations section ###
    plot_groups = 1
    station_groups = len(station_list)
    out_file.write('{:5d}{:5d}'.format(plot_groups,station_groups))
    out_file.write('\n')
    count = 1
    for station in station_list:
        if count % 5 == 0:
            out_file.write('{:8s}  {:4s}'.format(station,'YES'))
            out_file.write('\n')
        else:
            out_file.write('{:8s}  '.format(station))
        if count == len(station_list) and count % 5 != 0:
            while count % 5 != 0:
                station = ' '
                out_file.write('{:8s}  '.format(station))
                count += 1
            out_file.write('{:4s}'.format('YES'))
        count += 1
    ### end group stations ###
        
    open_summary.close()
    out_file.close()
    final_summary.close()
print 'Completed!'