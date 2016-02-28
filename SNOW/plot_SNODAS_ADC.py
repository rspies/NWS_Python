# Created on September 30, 2014
# @author: rspies
# Python 2.7
# This script plots a scatter plot of the NOHRSC SNODAS modeled SWE and SCA
# using downloaded data from NOHRSC website
# http://www.nohrsc.noaa.gov/interactive/html/graph.html?brfc=nwrfc

import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
import pandas as pd

os.chdir("../..") # change dir to \\NWS
maindir = os.getcwd()

################################# User Input #########################################
############ User input ################
RFC = 'NWRFC_FY2016'
fx_group = ''
workingdir = maindir + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep
adc_plot = 'off' # 'on' or 'off' -> off only runs the chps csv conversion

if fx_group != '':
    task_csv = RFC[:5] + '_fy16_task_summary_' + fx_group + '.csv'
    download_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'download_data' + os.sep + fx_group + os.sep
    chps_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'chps_csv' + os.sep + fx_group + os.sep
    summary_file = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'NOHRSC_data_download_summary_' + fx_group + '.csv'
    adc_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'ADC_plots' + os.sep + fx_group + os.sep
else:
    task_csv = RFC[:5] + '_fy16_task_summary.csv'
    download_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'download_data' + os.sep
    chps_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'chps_csv' + os.sep
    summary_file = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'NOHRSC_data_download_summary.csv'
    adc_dir = workingdir + 'data_csv' + os.sep + 'NOHRSC_snow' + os.sep + 'ADC_plots' + os.sep
######################################################################################

# read summary file
read_csv = open(summary_file,'r')
info = pd.read_csv(read_csv,sep=',',header=0)
read_csv.close()

# collect basin list and info
if 'Basin' in info:
    basin_list = info['Basin'].tolist()
else:
    print '"Basin" not in csv header...'
if 'SHEF_ID' in info:
    shef_list = info['SHEF_ID'].tolist()
else:
    print '"SHEF_ID" not in csv header...'
if 'SNODAS_area_sq_mi' in info:
    area_list = info['SNODAS_area_sq_mi'].tolist()
else:
    print '"SNODAS_area_sq_mi" not in csv header...'
    
# combine list into dict
basin_area = dict(zip(basin_list, area_list))
basin_shef = dict(zip(basin_list, shef_list))    
    
print basin_list
#basin_list = [2912] # manually run basins here 
for each_basin in basin_list:
    basin = str(each_basin)
    data_csv = open(download_dir  + basin + '_snodas.csv','r')   
    print 'Parsing: ' + basin + '...'
    df = pd.read_csv(data_csv,sep=',',header=0,parse_dates='date',index_col=['date'],na_values=[' ','',' \n'])
    #df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H')
    ts = df.resample(rule='24H', how='last', base=0)
    ts.columns = ['snow_cover','swe_min','swe_mean','swe_max','sca_min','sca_mean','sca_max'] # rename columns
    
    if len(ts) > 20: # check that there is adequate data in dataframe (20 days)
        # output data to csv for possible CHPS import
        chps_swe = open(chps_dir + basin + '_SWE.csv','w')
        chps_sca = open(chps_dir + basin + '_SCA.csv','w')
        chps_swe.write('Location Names,'+basin+'\n')
        chps_swe.write('Location Ids,'+basin+'\n')
        chps_swe.write('Time,SNWE [in]\n')
        chps_sca.write('Location Names,'+basin+'\n')
        chps_sca.write('Location Ids,'+basin+'\n')
        chps_sca.write('Time,SASC [%]\n')
        ts.to_csv(chps_swe, na_rep='-999.0',columns=['swe_mean'],mode='a',date_format='%Y-%m-%d %H:%M:%S',header=False)
        ts.to_csv(chps_sca, na_rep='-999.0',columns=['snow_cover'],mode='a',date_format='%Y-%m-%d %H:%M:%S',header=False)
    
        # close files
        data_csv.close()
        chps_swe.close(); chps_sca.close()        

        ########################################################################################
        if adc_plot == 'on':        
        
            # clip out missing or days with 0 SCA/SWE for plotting
            ts = ts[ts.swe_mean != 0]
            #ts = ts[ts.swe_mean != ' ']
            ts = ts[ts.swe_mean.notnull()]
            ts = ts[ts.snow_cover != 0]
            #ts = ts[ts.snow_cover != ' ']
            ts = ts[ts.snow_cover.notnull()]
            
            # convert to list for plotting
            SWE = ts['swe_mean'].tolist()
            SCA = ts['snow_cover'].tolist()
            
        
            print 'Creating figure...'
            fig, ax1 = plt.subplots(figsize=(10,9))
            #Plot the data
            ax1.scatter(SCA, SWE, color='k', marker='o', zorder=5)
            
            #ax1.minorticks_on()
            ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
            ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
            
            #majorLocator = MultipleLocator(10)
            #ax1.xaxis.set_major_locator(majorLocator)
            ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
            
            ax1.set_xlabel('Areal Extent of Snow Cover (%)')
            ax1.set_ylabel('SWE (in)')
            
            plt.ylim(ymin=0)
            plt.xlim(xmax=101)
            plt.xlim(xmin=0)
            
            # add second y-axis with metric units
            y1, y2=ax1.get_ylim()
            ax2=ax1.twinx()
            ax2.set_ylim(y1*25.4, y2*25.4)
            ax2.set_yticks(range(int(y1*25.4), int(y2*25.4), 2))
            majorLocator = plt.MaxNLocator(10)
            ax2.yaxis.set_major_locator(majorLocator)
            ax2.set_ylabel('SWE (mm)')
            
            #add plot legend with location and size
            #ax1.legend(loc='upper left', prop={'size':10})
                
            plt.title(basin_shef[each_basin] + '\nSNODAS SWE vs. SCA (2002-2015 Daily Data) : Model Area=' + str(basin_area[each_basin]) + ' sq mi')
                
            figname = adc_dir + basin + '_ADC.png'
            plt.savefig(figname, dpi=100,bbox_inches='tight')
            
            plt.clf()    
            plt.close()
            #Turn interactive plot mode off (don't show figures)
            plt.ioff()    

print 'Script Completed'
