# created by Ryan Spies 
# 2/19/2015
# Python 2.7
# Description: parse through a summary file of NHDS site info obtained from website
# and split out individual cardfiles for each site. Also creates a summary csv file
# with calculated valid data points and percent of total. Used to display in arcmap

import os
import datetime
import dateutil.parser
maindir = os.getcwd()
workingdir = maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep +'raw_data'

################### user input #########################
variable = 'ptpx'  # choices: 'ptpx', 'tamn', or 'tamx'
timestep = 'daily' # choices: 'hourly' or 'daily'
station_file =  workingdir + os.sep + 'nhds_' + timestep +os.sep + 'nhds_site_locations_' + timestep + '.txt'
daily_obs_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + 'site_obs_time.csv'
data_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + os.sep + variable + os.sep + 'sw_ak_' + variable + '_1960_2013.txt'
out_dir = workingdir + os.sep + 'nhds_' + timestep +os.sep + os.sep + variable + os.sep + 'cardfiles' + os.sep
bad_ptpx_file = workingdir + os.sep + 'nhds_' + timestep +os.sep + 'questionable_ptpx_check_' + timestep + '.txt'
########################################################
if variable == 'tamn':
    ext = '.tmn'; taplot = 'nhds_' + variable + '.taplot'; tap_open = open(workingdir + os.sep + 'nhds_' + timestep + os.sep + variable + os.sep + taplot, 'wb')
if variable == 'tamx':
    ext = '.tmx'; taplot = 'nhds_' + variable + '.taplot'; tap_open = open(workingdir + os.sep + 'nhds_' + timestep + os.sep + variable + os.sep + taplot, 'wb')
if variable == 'ptpx':
    ext = '.ptp'
    bad_ptpx_summary = open(bad_ptpx_file,'wb')
    check_chps = open(maindir[:-16] + 'Calibration_NWS'+ os.sep +'APRFC_FY2015'+ os.sep + 'CHPS_suspect_map.csv','r')
    set_miss_dates = []    
    for line in check_chps:     # check csv file with dates of suspect MAP data (from CHPS)
        date_chps = dateutil.parser.parse(line)
        set_miss_dates.append(date_chps.date())
if timestep == 'hourly':
    year_factor = float(24*365)
if timestep == 'daily':
    year_factor = float(365)

### parse summary file for station info ###
summary_file = open(workingdir + os.sep + 'nhds_summary_' + variable + '_' + timestep + '.csv','w')
summary_file.write('NAME,SITE_ID,LAT,LON,ELEV,TOTAL_DATA,YEARS_DATA,PCT_AVAIL,YEAR_START,YEAR_END\n')
station_summary = {}; elev_list = []
read_stations = open(station_file,'r')
for line in read_stations:
    if line[0] != '#':
        name = line[13:40].strip()      # find the station name
        number = line[40:47].strip()    # find the station id num (6 digit)
        site_id = number.split()[1]     # find the station id num (4 digit)
        split = filter(None,line[47:].strip().split('   ')) # filter out blank entries in list
        lat = split[0]; lon = '-' +split[1]; elev = split[2].strip(); types = split[5]
        station_summary[site_id] = [name,number,lat,lon,elev]
        elev_list.append(float(elev)) # used to fin max/min for taplot header line

### parse observation time csv file for daily data (taplot card) ###        
if timestep == 'daily':
    if variable == 'tamn' or variable == 'tamx':
        daily_obs = {}
        obs_time = open(daily_obs_file,'r')
        for line in obs_time:
            sep = line.split(',')
            if sep[0].strip() != 'LOCATION' and sep[0].strip() != '':
                daily_obs[sep[0]] = sep[8]
        obs_time.close()
        
### taplot header line ###
if variable == 'tamn' or variable == 'tamx':
    if len(station_summary) <= 26:
        total_stations =  len(station_summary)
    else:
        total_stations = 26
    units = 'ENGL'
    desc = "'KUSKOKWIM BASINS SW ALASKA'"
    max_elev = max(elev_list); min_elev = min(elev_list)
    tap_open.write('@A ')
    tap_open.write('{:2d} {:4s} {:30s} {:4.0f} {:4.0f}'.format(total_stations,units,desc,max_elev,min_elev))
    tap_open.write('\n')
    
### parse data and create individual datacard files ###
read_data = open(data_file,'r') 
site_check = 'xxxx' # dummy site check to ignore first few empty lines
count_all = 0; count_missing = 0; prev_month = 13; day_count = 0     
for each in read_data:
    if each[:8] == 'datacard':
        start_header = each
        header = each.split()
        site_check = header[5]
        site_id_data = header[5].split('-')[1] # find the station id num (4 digit)
    if each[:1] == ' ' or each[:1] == '1': # find the second line of each site's header to start new cardfile
        if len(filter(None,each.split())) <= 7: # ignore station data at end of temp data
            header2 = each.split()
            date_start = header2[0] + header2[1]; date_end = header2[2] + header2[3]
            #cardfile = open(out_dir + header[5] + '_NHDS.' + date_start + '.' + date_end + ext,'wb') # <- name may be too long for MAT input card
            cardfile = open(out_dir + header[5] + '_NHDS' + ext,'wb')            
            cardfile.write(start_header)
            cardfile.write(each)
    if variable == 'tamn' or variable == 'tamx': # find the taplot lines for temperature data
        if each[:1] == ' ' or each[:1] == '1' or each[:1] == '@' or each[:1] == '-':
            if each[:2] == '@F':
                name = each[5:25].strip()
                lat_taplot = float(each[29:].split()[0]); lon_taplot = float(each[29:].split()[1]); elev_taplot = int(float(each[29:].split()[3]))
                if name in daily_obs:
                    time_of_obs = int(daily_obs[name])/100
                else:
                    print 'Observation time not available for: ' + name + ' -> using 1700 as estimate'
                    time_of_obs = int(17)
                if len(name) <= 15:
                    tap_open.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+name + ' NHDS'+"'",lat_taplot,lon_taplot,time_of_obs,elev_taplot))
                else:
                    tap_open.write('{:2s} {:20s} {:6.2f} {:6.2f} {:2d} {:4d}'.format('@F',"'"+name +"'",lat_taplot,lon_taplot,time_of_obs,elev_taplot))
                tap_open.write('\n')
            elif each[:2] == '@G' or each[:2] == '@H': # find taplot lines at end of data
                tap_open.write(each.rstrip() + ' ')
            elif len(filter(None,each.split())) >= 7:
                tap_open.write(' '.join(each.split()))
                tap_open.write('\n')
    if each[:1] != '$' and each[:11] == site_check: # find data lines corresponding to the current site id
        parse = each[20:].strip().split() # parse through data in columns 4-9 in each line of data
        parse_month = int((each[:20].split()[1])[:-2])
        parse_year = int((each[:20].split()[1])[-2:])
        if parse_year <= 15:
            parse_year = parse_year + 2000
        else:
            parse_year = parse_year + 1900
        if parse_month >=4 and parse_month <= 9:
            thresh = 2.0
        else:
            thresh = 1.5
        for value in parse:
            count_all += 1
            if value == '-999.00':
                count_missing += 1
        if variable == 'ptpx':
            check_list = []
            for value in parse:
                check_list.append(float(value))
            if any(check >= thresh for check in check_list) == True: # check if any values in line are >= 2.0 inches
                bad_ptpx_summary.write(each) # write instance to questionable_ptpx_check_.txt 
                if any(check >= thresh for check in check_list) == True: # replace values with new_value = value/10
                    cardfile.write(each[:22])
                    for value in parse:
                        if parse_month == prev_month:
                            day_count += 1
                        else:
                            day_count = 1
                            prev_month = parse_month
                        day_check = datetime.datetime(parse_year,parse_month,day_count).date()
                        if float(value) >= thresh:
                            new_value = float(value)/10
                            cardfile.write("%7.2f" % new_value)
                            cardfile.write('  ')
                        else:
                            cardfile.write("%7.2f" % float(value))
                            cardfile.write('  ')
                    cardfile.write('\n')
            else:
                if timestep == 'daily':
                    cardfile.write(each[:22])
                    for value in parse:
                        if parse_month == prev_month:
                            day_count += 1
                        else:
                            day_count = 1
                            prev_month = parse_month
                        day_check = datetime.datetime(parse_year,parse_month,day_count).date()
                        if day_check in set_miss_dates:
                            if float(value) >= (thresh - 1.25):
                                new_value = -999.00
                                cardfile.write("%7.2f" % new_value)
                                cardfile.write('  ')
                                bad_ptpx_summary.write(site_check + ' ' + str(day_check) + ' old_value: ' + str(value) + ' new_value: ' + str(new_value) + '\n') # write instance to questionable_ptpx_check_.txt 
                            else:
                                cardfile.write("%7.2f" % float(value))
                                cardfile.write('  ')
                        else:
                            cardfile.write("%7.2f" % float(value))
                            cardfile.write('  ')
                    cardfile.write('\n')
                else:
                    cardfile.write(each)
        else:
            cardfile.write(each) 
    if each[:1] == '$' and count_all > 0: # find the break btw station data -> calculate site summary
        percent_data = round(((count_all - count_missing)/float(count_all))*100,1)
        station_summary[site_id_data].append(count_all-count_missing)
        station_summary[site_id_data].append(round((count_all-count_missing)/year_factor,2))
        station_summary[site_id_data].append(percent_data)
        station_summary[site_id_data].append(date_start[-4:])
        station_summary[site_id_data].append(date_end[-4:])
        count_all = 0; count_missing = 0
        print site_id_data + ' -> ' + str(percent_data) + '%'
        prev_month = 13
        
### populate summary csv file
for site in station_summary:
    for item in station_summary[site]:
        summary_file.write(str(item) + ',')
    summary_file.write('\n')

summary_file.close()
if variable == 'tamn' or variable == 'tamx':
    tap_open.close() 
if variable == 'ptpx':
    bad_ptpx_summary.close() 
cardfile.close()
read_stations.close()
print 'Completed!'
