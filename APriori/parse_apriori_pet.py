###################################################################################
# parse_apriori_pet.py
# Ryan Spies (amec.com)
# 7/25/2014
# Description: parse through the .csv files created by arcpy script (gis toolbox)
# creat basin output summary table of PE, PE adj, and PED data
###################################################################################
import os

os.chdir("../..")
maindir = os.getcwd()

######################## User Input ###############################
RFC = 'MARFC_FY2017'
basins_dir = maindir + '\\GIS\\' + RFC[:5] + os.sep + RFC + '\\Apriori\\'
summary = open(basins_dir + 'apriori_ETD_summary.csv','w')
###################################################################
summary.write('Calculated Apriori ETD = PE * PEadj (units = mm/day)\n')
basins = os.listdir(basins_dir)
months_sort = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
summary.write('basin,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec\n')

for each in basins:
    print each
    if each[-4:] != '.csv':
        months = {'jan':[],'feb':[],'mar':[],'apr':[],'may':[],'jun':[],'jul':[],'aug':[],'sep':[],'oct':[],'nov':[],'dec':[]}
        fopen = open(basins_dir + each + '\\' + each + '_apriori_parameters.csv','r')
        for row in fopen:
            line = row.split(',')
            if line[0] != 'Parameter':
                par_name = line[0].split('_')
                if par_name[1] == 'pe': # PE
                    month = par_name[2]
                    pe = line[1]
                    if month in months:
                        months[month].append(pe)
                if par_name[1] == 'peadj': # PE_adj
                    month = par_name[2]
                    peadj = line[1]
                    months[month].append(peadj)
                if par_name[1] == 'etd': # ETD
                    month = par_name[2]
                    etd = line[1]
                    months[month].append(etd)
        fopen.close()
        fnew = open(basins_dir + each + '\\' + each + '_apriori_PET.csv','w')
        fnew.write('month'+','+'PE'+','+'PEadj'+','+'ETD'+'\n')
        summary.write(each+',')
        for key in months_sort:
            fnew.write(key+','+months[key][2]+','+months[key][1]+','+months[key][0]+'\n')
            summary.write(months[key][0]+',')
        summary.write('\n')
        fnew.close()

summary.close() 
print 'Completed!!'
