# Ryan Spies
# 3/28/13
# Python 2.6.5
# This script converts .MAP and .MAT files into simple tab delimited text
# files for use in matlab

#!!!!!!!!!!! Units left in inches and degrees F !!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!! Data must be 6 hour time steps !!!!!!!!!!!!!!!!!!!!!!

import os
import datetime
os.chdir("../..")
maindir = os.getcwd()

######################## User Input Section ############################
path = os.getcwd()
rfc = 'LMRFC_FY2016'
variable = 'MAP'
map_dir = maindir + '\\Calibration_NWS\\' + rfc[:5] + os.sep + rfc + '\\datacards\\' + variable +'\\'
output_dir = maindir + '\\Calibration_NWS\\' + rfc[:5] + os.sep + rfc + '\\datacards\\' + variable +'\\' + variable + '_single_column\\'
###################### End User Input ##################################

# give directory of original RFC MAP/MAT files
rfc_files = os.listdir(map_dir)
#rfc_files=['notg1']
for basin_file in rfc_files:
    if basin_file == 'datacards_fromRFC':
        basin_files = os.listdir(map_dir + basin_file)
        for files in basin_files:
            variable = variable[:3]
            # locate only .mat and .map files
            if files[-5:] == variable + '06' or files[-3:] == variable:
                basin = files.split('.')[0]
                basin_title = str.upper(basin)
                #var = files[-5:]
                print basin_title + ' : ' + variable
                if files[-5:]== variable + '06':
                    variable = variable + '06'
        
                # enter file locations for old and new files
                file1 = map_dir + basin_file + '\\' + files
                fw = open(output_dir + '\\' + basin_title + '_' + variable + '.txt','w')
        
                fg = open(file1,'r')
                for each in fg:
                    if each[:20] == '$  PERIOD OF RECORD=':
                        start_year = int(each[23:27]); start_mn = int(each[20:22]); begin = start_year
                        end_year = int(each[-5:-1]); end_mn = int(each[-8:-6])
                        fg.close()
                        break
                years = []
                while start_year <= end_year:
                    years.append(start_year)
                    start_year += 1
                count_time = 0
                count_out = 0
                count_years = 0
        
                for yr_num in years:
                    count_years += 1
                    if yr_num == begin:
                        timestamp = datetime.datetime(yr_num,start_mn,1,6)
                    else:
                        timestamp = datetime.datetime(yr_num,1,1,6)
                    hours6 = datetime.timedelta(hours=6)
                    print yr_num
                # process data for specified years
        #        start = datetime.datetime(start_year,start_mn,1,0)
        #        end = datetime.datetime(end_year,end_mn+1,1,0)
        #        print start
        #        print end
        #        count_out = 0
        #        count_time = 0
        #        hours6 = datetime.timedelta(hours=6)
        #        timestamp = start
        #        while timestamp <= end:
        #            print timestamp
                    # load the RFC data file
                    fg = open(file1,'r')
                    count = 0 
                    for each in fg:
                        if count > 6:
                            spl = each.split()
                            # data format for years prior to 2000
                            if len(spl) == 8 or len(spl) == 6 or len(spl) == 4:
                                #mn = int(spl[0])
                                mnyr = spl[0]
                                yr = mnyr[-2:]
                                if int(yr) <= 14: #change format for years >= 2010
                                    yr = '20' + yr
                                else:
                                    yr = '19' + yr
                                mn = mnyr[:-2]
                                if yr == str(yr_num) and mn == str(timestamp.month):
                                    for num in spl:
                                        if len(num) > 4:
                                            # write output file in column format
                                            fw.write(str(timestamp) + '\t')
                                            fw.write(str(num) + '\n')
                                            timestamp = (timestamp + hours6)
                                            count_out += 1
                                            count_time += 1
                            
                            # data format for years 2000+
                            elif len(spl) == 9 or len(spl) == 7 or len(spl) == 5:
                                #mn = int(spl[0])
                                yr = spl[1]
                                mn = spl[0]
                                if len(yr) == 1:
                                    yr = '0' + yr
                                yr = '20' + yr
                                if yr == str(yr_num) and mn == str(timestamp.month):
                                    for num in spl:
                                        if len(num) > 4:
                                            # write output file in column format
                                            fw.write(str(timestamp) + '\t')
                                            fw.write(str(num) + '\n')
                                            timestamp = (timestamp + hours6)
                                            count_out += 1
                                            count_time += 1
                            else:
                                timestamp = (timestamp + hours6)
                                count_time += 1
                                print '### Caution: data not found -> ' + str(timestamp)
            
                                            
                        count += 1
                    fg.close()
                fw.close()
                print 'timesteps:\t' + str(count_time)
                print 'output:   \t' + str(count_out)

print 'Finito!!!'
