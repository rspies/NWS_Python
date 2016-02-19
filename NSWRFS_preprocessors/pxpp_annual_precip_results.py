# created by Ryan Spies 
# 7/6/2015
# Python 2.7
# Description: parse through PXPP output master file for station annual precip

import os
import os.path
maindir = os.getcwd()

################### user input #########################
file_dir = 'final' # 'initial', 'final'
file_name = 'pxpp_riogrande_07062015.20150706.203418'
########################################################
file_open = open(maindir + os.sep + file_dir + os.sep + file_name,'r')
summary_out = open(maindir + os.sep + file_dir + '_riogrande_pxpp_summary.csv','w')
summary_out.write('Station,Annual Precip\n')
for line in file_open:
    if line[:9] == '0STATION ':
        sep = line.split()
        if 'I.D.=' in sep:
            x = sep.index('I.D.=')
            station = sep[x+1]
    if line[:19] == ' MEAN PRECIPITATION':
        spl = line.split()
        annual_ppt = spl[-1]
        summary_out.write(station+','+annual_ppt+'\n')
        print station + ' -> ' + annual_ppt
summary_out.close()
file_open.close()
print 'Completed!'
