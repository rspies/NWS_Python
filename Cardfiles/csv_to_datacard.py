#Created on July 23, 2015
#@author: rspies
# Lynker Technologies
# Python 2.7
# Description: parse through a csv file with date and variable and generate a 
# formatted datacard for chps import. Note: script does not check for missing 
# time steps

import os
import datetime
import collections
maindir = os.getcwd()
os.chdir("../..")
maindir = os.getcwd() + os.sep

################### user input #########################
station_dir = maindir + 'Calibration_NWS/NERFC/NERFC_FY2016/datacards/MAT/'
csv_dir = station_dir + os.sep + 'chps_modified_csv' + os.sep 
out_dir = station_dir + os.sep + 'final_datacard'
variable = 'MAT'
chps_shift = 'yes' # shift time back by 1 timestep (csv from CHPS shifts forward compared to original datacard)
variable_name = 'TEMP' #'inflow' or 'outflow'
start = datetime.datetime(1950,1,1,0)
header_lines = 2 # header lines in csv
timestep = 6 # time step in hours
date_time_format = "%Y-%m-%d %H:%M:%S"
#data_format = 'f9.3'
basin_list = ['CFDM1','NWFM1','JVLV1LWR','JVLV1UPR'] # name of location
loc_name = {'CFDM1':'NARRAGUAGAS CHERRYFD','NWFM1':'SHEEPSCOT NWHITEFLD','JVLV1LWR':'LO JEFFERSONVIL','JVLV1UPR':'UP JEFFERSONVIL'} #
########################################################
var_units = {'QME':'CFSD','MAP':'MM','MAT':'DEGF'}
var_dim = {'QME':'L3','MAP':'L','MAT':'TEMP'}

for basin_id in basin_list:
    count = 0
    csv_file = csv_dir + basin_id + '_final.csv'
    read_file = open(csv_file,'r')
    dates = collections.OrderedDict()
    print 'parsing file: ' + basin_id + ' -> ' + csv_file
    for line in read_file:
        count += 1
        if count > header_lines:
            sep = line.split(',')
            date = datetime.datetime.strptime(sep[0], date_time_format)
            if chps_shift == 'yes':
                date = date - datetime.timedelta(hours=timestep)
            data = sep[1].strip()
            if data == '':
                data = -999
            elif float(data) < 0 and variable != 'MAT':
                data = -999
            if date >= start:
                dates[date] = data
    #### data output to formatted datacard
    write_file = open(out_dir + os.sep + 'modified_' + basin_id + '.' + variable.upper(),'wb')
    write_file.write('$ Datacard Time Series created at ' + str(datetime.datetime.now().date()) + ' from CSV Conversion Script\n')
    write_file.write('$ Data type: ' + variable_name + '\n')
    write_file.write('$ PERIOD OF RECORD= ' + str(min(dates).month)+'/'+str(min(dates).year) + ' THRU ' + str(max(dates).month)+'/'+str(max(dates).year)+'\n')
    #write_file.write('$ \n')
    write_file.write('$ Symbol for missing data = -999.00 \n')
    write_file.write('$ ' + 'TYPE=' + variable + '    ' + 'UNITS=' + var_units[variable] + '    ' + 'DIMENSIONS=' + variable_name + '    ' + 'TIME INTERVAL=' + str(timestep) + ' HOURS\n')
    write_file.write('{:12s}  {:4s} {:4s} {:4s} {:2d}   {:12s}    {:12s}'.format('DATACARD', variable, var_dim[variable],var_units[variable],int(timestep),basin_id,loc_name[basin_id]))
    write_file.write('\n')
    #write_file.write('datacard      ' + variable + '  ' + var_dim[variable] + '   '+ var_units[variable] +'   ' + str(timestep) + '   '+basin_id+'          '+loc_name+'\n')
    if min(dates).month >=10 and max(dates).month >= 10:
        write_file.write(str(min(dates).month)+'  '+str(min(dates).year)+' '+str(max(dates).month)+'   '+str(max(dates).year)+'  1   F9.3'+'\n')    
    elif min(dates).month >=10:
        write_file.write(str(min(dates).month)+'  '+str(min(dates).year)+'  '+str(max(dates).month)+'   '+str(max(dates).year)+'  1   F9.3'+'\n')
    elif max(dates).month >=10:
        write_file.write(' ' + str(min(dates).month)+'  '+str(min(dates).year)+' '+str(max(dates).month)+'   '+str(max(dates).year)+'  1   F9.3'+'\n')
    else:
        write_file.write(' ' + str(min(dates).month)+'  '+str(min(dates).year)+'  '+str(max(dates).month)+'   '+str(max(dates).year)+'  1   F9.3'+'\n')
    month_prev = min(dates).month
    hr_count = 0
    for each in dates:
        if each.month == month_prev:
            hr_count += 1
        else:
            hr_count = 1
        if int(each.month) < 10:
            space1 = '    '
        else:
            space1 = '   '
        if hr_count < 10:
            space2= '   '
        elif hr_count <100:
            space2= '  '
        else:
            space2= ' '
        ### write data to datacard ###
        write_file.write('{:12s}{:2d}{:02d}{:4d}{:9.3f}'.format(basin_id,int(each.month),int(str(each.year)[-2:]),hr_count,float(dates[each])))
        write_file.write('\n')
        #write_file.write(basin_id + space1 + str(each.month)+str(each.year)[2:] + space2 +  str(hr_count) + "%10.2f" % float(dates[each]) + '\n')
        month_prev = each.month
    write_file.close()
    read_file.close()
print 'Completed!'