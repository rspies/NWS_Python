# created by Ryan Spies - amec foster wheeler
# 2/19/2015
# Python 2.7

import os
import datetime
import collections
maindir = os.getcwd()

################### user input #########################
station_file = maindir[:-21] + '/FEWS/chps_calb/wgrfc_calb/Import/backup/pixml_mapx/MAPX_Calib_Export.201404301706.txt'
pixml_file = maindir + os.sep + 'BTVA2_mapx_test.txt'
out_dir = maindir + os.sep + 'output_cardfiles'
variable = 'MAPX'
start = datetime.datetime(2000,1,1,0)
########################################################

basins = []
read_file = open(pixml_file,'r')
for line in read_file:
    strip = line.strip()
    if '<locationId>' in strip:
        basin_id = strip[12:18].rstrip('<')
        print basin_id
        dates = collections.OrderedDict()
    if '<event date' in strip:
        sep = strip.split('"')
        date = datetime.datetime.strptime(sep[1]+'-'+str(sep[3])[:2], "%Y-%m-%d-%H")
        precip = sep[5]
        if date >= start:
            dates[date] = precip
    if '</series>' in strip and basin_id not in basins:
        write_file = open(out_dir + os.sep + 'MAPX_' + basin_id + '.txt','w')
        write_file.write('$ Datacard Time Series created at ' + str(datetime.datetime.now()) + ' from PIXML Conversion Script\n')
        write_file.write('$ Data type: ' + variable + '\n')
        write_file.write('$ Symbol for missing data = -999.0 \n')
        write_file.write('$ \n')
        write_file.write('DATACARD      ' + variable + '  L   '+ 'MM'+'   1   '+basin_id+'          '+basin_id+'\n')
        write_file.write(str(min(dates).month)+'  '+str(min(dates).year)+'  '+str(max(dates).month)+'   '+str(min(dates).year)+'  1   f10.4'+'\n')
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
            write_file.write(basin_id + space1 + str(each.month)+str(each.year)[2:] + space2 +  str(hr_count) + "%10.4f" % float(dates[each]) + '\n')
            month_prev = each.month
        write_file.close()
        basins.append(basin_id)
read_file.close()
print 'Completed!'