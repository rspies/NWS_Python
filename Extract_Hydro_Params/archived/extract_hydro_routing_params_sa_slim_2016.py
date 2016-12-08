# original: Extract_Hydro_Params.py
# Ryan Spies
# rspies@lynkertech.com
# Lynker Technologies
# Description: extracts SAC-SMA/Snow17/UNITHG/LAG-K/Tatum parameters values
# from CHPS configuration .xml files located in the Config->ModuleConfigFiles
# directory and ouputs a model .csv file with all parameters

# NOTE: this script only works with the original CHPS SA moduleparfile .xml files...
# not the CHPS CALB parameters from export mods

#import script modules
import os
os.chdir("../..")
maindir = os.path.abspath(os.curdir)

#-----------------------------------------------------------------------------
#START USER INPUT SECTION
#Enter RFC
RFC = 'NWRFC_FY2016'
param_source = 'pre_calb' # choices: 'pre_calb','sa'

#Turn on/off model parameter searchs # choices: 'on' or 'off'
sacsma = 'off'
snow = 'on' 
lagk = 'off'
uhg = 'off'

#Turn on/off plot choices
uh_plots = 'off' # choices: 'on' or 'off' -> UNIT-HG plots
lag_plots = 'off' # choices: 'on' or 'off' -> LAG/K plots
snow_plots = 'off' # choices: 'on' or 'off' -> areal depletion plots
#END USER INPUT SECTION
#-----------------------------------------------------------------------------

print 'Script is Running...'
# Find the directory location of the desired ModuleParFiles
if param_source == 'pre_calb':
    folderPath = 'D:\\Software\\CHPS_local\\chps_calb\\FY'+RFC[-4:]+'\\' + RFC[:5].lower() + '_calb\\Config\\ModuleParFiles\\*'
if param_source == 'sa':
    folderPath = 'D:\\Software\\CHPS_local\\chps_sa\\FY'+RFC[-2:]+'\\' + RFC[:5].lower() + '_sa\\Config\\ModuleParFiles\\*'
    #folderPath = maindir + '\\NWS\\CHPS\\chps_calb\\' + RFC.lower() + '_calb\\Config\\ModuleParFiles\\*'
print folderPath

#!!!!!! output directory: enter ouput directory for .csv files below ->
csv_file_out = maindir + '\\Python\\Extract_Hydro_Params\\' + RFC[:5] + os.sep + RFC + '\\Params_' + param_source

#import script modules
import re
import glob
from datetime import datetime
if uh_plots == 'on' or lag_plots == 'on':
    import numpy
    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator
    from matplotlib.ticker import MultipleLocator
    #Turn interactive plot mode off (don't show figures)
    plt.ioff() 

os.chdir("Python/Extract_Hydro_Params")
working_dir = os.getcwd()
print 'Script is Running...'

#SAC-SMA SECTION--------------------------------------------------------------
#loop through SACSMA files in folderPath
sac_params = ['REXP','LZPK','LZFPM','PXADJ','RUNOFF_COMPONENT_INTERVAL','PFREE','ZPERC','RIVA','MAPE_Input','MAPE_INPUT','PEADJ','LZTWM', \
                   'RSERV','ADIMP','UZK','SIDE','LZFSM','LZSK','SMZC','UZTWM','UZFWM','PCTIM','EFC']
#new_name_params = ['RCI','RUNOFF_COMPONENT_INTERVAL','MAPE_Input','MAPE_INPUT']
if sacsma == 'on':
    print 'Processing SACSMA parameters...'
    sac_line = 1
    csv_file = open(csv_file_out +'\\_' + RFC + '_SACSMA_Params_' + param_source + '_slim.csv', 'w')
    csv_file.write('BASIN,NAME,REXP,LZPK,LZFPM,PXADJ,RCI,PFREE,ZPERC,RIVA,MAPE_Input,PEADJ,LZTWM,'\
                   'RSERV,ADIMP,UZK,SIDE,LZFSM,LZSK,SMZC,UZTWM,UZFWM,PCTIM,EFC,'\
                   'JAN_ET,FEB_ET,MAR_ET,APR_ET,MAY_ET,JUN_ET,JUL_ET,AUG_ET,SEP_ET,OCT_ET,NOV_ET,DEC_ET' + '\n')
    for filename in glob.glob(os.path.join(folderPath, "SAC*.xml")):
        #print filename
    
        #Define output file name
        name = str(os.path.basename(filename)[:])
        name = name.replace('SACSMA_', '')
        name = name.replace('_UpdateStates.xml', '')
        spl_name = name.split('_')[1]
        print 'SAC-SMA -> ' + spl_name
        #print name
        csv_file.write(name + ',')
        csv_file.write(spl_name + ',')
    
        #Open .xml file and temporary .txt file to write .xml contents to
        xml_file = open(filename, 'r')
        found_param = []
        #loop through parameters in the 'sac_params' list
        for param in sac_params:
            
            #get line number that the paramter is on
            line_num = 0
            for line in xml_file:
                line_num += 1
                if param in line and 'dbl' not in line and 'bool' not in line: # param value on next line or next line + 1
                    case = 1; found_param.append(param)
                    break
                elif param in line and 'dbl' in line and 'bool' not in line: # param on same line?
                    case = 2; found_param.append(param)
                    break
        
            #Set cursor back to beginning of xml_file
            #xml_file.seek(0)
        
            #Section/line of .xml file with desired parameter value
            if param not in found_param:
                if param != 'MAPE_Input':
                    csv_file.write(',')
                if param != 'MAPE_Input' and param != 'MAPE_INPUT':
                    print 'Warning - parameter not found: ' + param
                xml_file.seek(0)
            else:
                xml_file.seek(0)
                if case == 1:
                    section = xml_file.readlines()[line_num:line_num+2] # param value on next line
                    if 'description' in section[0]:
                        line = section[1] # param value on next line + 1
                    else:
                        line = section[0]
                elif case == 2: # param on same line
                    section = xml_file.readlines()[line_num-1:line_num]
                    line = section[0]
                
                #Write only numbers and decimals to output file
                #also catch TRUE/FALSE booleans
                if "TRUE" in line or 'true' in line:
                    line = "TRUE"
                elif "FALSE" in line or 'false' in line:
                    line= "FALSE"
                else:
                    line = re.sub("[^0123456789\.\-]", "", line)
                csv_file.write(line + ',')
    
                #Set cursor back to beginning of xml_file before moving on to next parameter
                xml_file.seek(0)
                
        ###ET_DEMAND_CURVE
        xml_file.seek(0)
        line_num=0
        for line in xml_file:
            line_num += 1
            if 'row A' in line:
                break
    
        xml_file.seek(0)
        
        line_num_start=line_num-1
        line_num_end=line_num    
        x=0
        while x <12:    
        
            section = xml_file.readlines()[line_num_start:line_num_end]
        
            for line in section:
                line = re.sub("[^0123456789\.\-]", "", line)
                csv_file.write(line + ',')
                
            line_num_start+=1
            line_num_end+=1
            x+=1        
            
            xml_file.seek(0)
        
        xml_file.close()
        csv_file.write('\n')

    csv_file.close()

############################################################################################################################################################### 
#SNOW-17 SECTION---------------------------------------------------------------
#loop through SACSMA files in folderPath
if snow == 'on':
    snow_params = ['ALAT','ELEV','TAELEV','PXADJ','SCF','MFMAX','MFMIN','UADJ','SI','NMF','TIPM', \
                'MBASE','PXTEMP','PLWHC','DAYGM','MV','RAIN_SNOW_ELEV_INPUT_OPTION','SCTOL','WETOL']
                
    print 'Processing SNOW-17 parameters...'
    csv_file = open(csv_file_out + '\\' + '_' + RFC + '_SNOW17_Params_' + param_source + '_slim.csv', 'w')
    
    csv_file.write('BASIN,NAME,ALAT,ELEV,TAELEV,PXADJ,SCF,MFMAX,MFMIN,UADJ,SI,NMF,TIPM,'\
                    'MBASE,PXTEMP,PLWHC,DAYGM,MV,RAIN_SNOW_ELEV,SCTOL,WETOL,' + '\n')
    
    csv_adc = open(csv_file_out + '\\' + '_' + RFC + '_SNOW17_ADC_' + param_source + '_slim.csv', 'w')
    csv_adc.write('BASIN,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0\n')
    
    for filename in glob.glob(os.path.join(folderPath, "SNOW*.xml")):
        #print filename
        
        #Define output file name
        name = str(os.path.basename(filename)[:])
        name = name.replace('SNOW17_', '')
        name = name.replace('_UpdateStates.xml', '')
        spl_name = name.split('_')[1]
        print 'Snow17 -> ' + spl_name
        #print name
        csv_file.write(name + ',')
        csv_file.write(spl_name + ',')
    
        #Open .xml file and temporary .txt file to write .xml contents to
        xml_file = open(filename, 'r')
        found_param = []
        #loop through parameters in the 'sac_params' list
        for param in snow_params:
            #Open .xml file and temporary .txt file to write .xml contents to
            xml_file = open(filename, 'r')
            #get line number that the paramter is on
            line_num = 0
            for line in xml_file:
                line_num += 1
                if param in line and 'dbl' not in line and 'bool' not in line: # param value on next line or next line + 1
                    case = 1; found_param.append(param)
                    break
                elif param in line and 'dbl' in line and 'bool' not in line: # param on same line?
                    case = 2; found_param.append(param)
                    break
        
            #Set cursor back to beginning of xml_file
            xml_file.seek(0)
        
            #Section/line of .xml file with desired parameter value
            if param not in found_param:
                csv_file.write(',')
                if param != 'RAIN_SNOW_ELEV_INPUT_OPTION':
                    print 'Warning - parameter not found: ' + param
                xml_file.seek(0)
            else:
                xml_file.seek(0)
                if case == 1:
                    section = xml_file.readlines()[line_num:line_num+2] # param value on next line
                    if 'description' in section[0]:
                        line = section[1] # param value on next line + 1
                    else:
                        line = section[0]
                elif case == 2: # param on same line
                    section = xml_file.readlines()[line_num-1:line_num]
                    line = section[0]
                
                #Write only numbers and decimals to output file
                #also catch TRUE/FALSE booleans
                if "TRUE" in line or 'true' in line:
                    line = "TRUE"
                elif "FALSE" in line or 'false' in line:
                    line= "FALSE"
                else:
                    line = re.sub("[^0123456789\.\-]", "", line)
                csv_file.write(line + ',')
        csv_file.write('\n')
            
        ### AEC and ADC ###
        xml_file.seek(0)
        
        AREA = []
        ELEV = []
        SCA = []
        csv_adc.write(spl_name+',')
        #### Area Elevation Curve     
        for line in xml_file:
            ### find area and elev data
            if 'row A' in line and 'B=' in line:
                line = re.sub("[^0123456789\.\-\"]", "", line)
                line = line.replace('""', ',')
                line = line.replace ('"', '')
                s1,s2 = line.split(',')
                AREA.append(s2)
                ELEV.append(s1)
            ### find SCA data
            if 'row A' in line and 'B=' not in line:
                line = re.sub("[^0123456789\.\-\"]", "", line)
                line = line.replace('""', ',')
                line = line.replace ('"', '')
                s1 = line.split(',')
                SCA.append(s1)
                csv_adc.write(s1[0]+',')
        csv_adc.write('\n')
            
        ### AEC and ADC PLOTS ###
        if snow_plots == 'on':
            if len(AREA) > 0:                
                fig, ax1 = plt.subplots()                
                #Plot the data
                ax1.plot(ELEV, AREA, color='black', label='AEC', linewidth='2', zorder=5)
                ax1.plot(ELEV, AREA, 'o', color='black', ms=8, zorder=5, alpha=0.75)
                #ax1.fill_between(x, AREA,facecolor='gray', alpha=0.25)    
                
                #ax1.minorticks_on()
                ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
                ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
                
                majorLocator = MultipleLocator(.10)
                ax1.yaxis.set_major_locator(majorLocator)
                ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
                ax1.set_xlabel('Elevation')
                ax1.set_ylabel('Area (% Below)')                    
                ax1.set_ylim([-0.05,1.05])
                
                #add plot legend with location and size
                ax1.legend(loc='upper left', prop={'size':10})
                    
                plt.title(name + ' Area Elevation Curve') 
                
                output_folder = csv_file_out +'\\AEC_plots\\'
                if os.path.exists(output_folder) == False:
                    os.makedirs(output_folder)
                figname = output_folder + name + '_AEC_slim.png'
                
                plt.savefig(figname, dpi=100)
                plt.clf()    
                plt.close()

            ### Area Depletion Curve
            SWE = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
            
            fig, ax1 = plt.subplots()                
            #Plot the data
            ax1.plot(SCA, SWE, color='black', label='ADC', linewidth='2', zorder=5)
            ax1.plot(SCA, SWE, 'o', color='black', ms=8, zorder=5, alpha=0.75)
            #ax1.fill_between(x, AREA,facecolor='gray', alpha=0.25)    
            
            #ax1.minorticks_on()
            ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
            ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
            
            majorLocator = MultipleLocator(.10)
            ax1.yaxis.set_major_locator(majorLocator)
            ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax1.set_xlabel('Areal Extent of Snow Cover (decimal)')
            ax1.set_ylabel('WE/A(i)')                    
            ax1.set_ylim([0.0,1.0])
            ax1.set_xlim([0.0,1.0])
            
            #add plot legend with location and size
            ax1.legend(loc='upper left', prop={'size':10})
                
            plt.title(name + ' Area Depletion Curve')

            output_folder = csv_file_out +'\\ADC_plots\\'
            if os.path.exists(output_folder) == False:
                os.makedirs(output_folder)
            figname = output_folder + name + '_ADC_slim.png'            
            
            plt.savefig(figname, dpi=100)
            plt.clf()    
            plt.close()
        xml_file.close()
    csv_file.close() 
    csv_adc.close()
  
###############################################################################
#UNIT HG SECTION---------------------------------------------------------------
#loop through UNITHG .xlm files in folderPath
if uhg == 'on':
    print 'Processing UH parameters...'
    csv_file = open(csv_file_out + '\\' + '_' + RFC + '_UHG_Params_' + param_source + '_slim.csv', 'w')
    
    csv_file.write('BASIN, AREA (mi2), Interval (hours),')
    t = 0
    while t < 600:
        csv_file.write(str(t) + ',')
        t += 6
    csv_file.write('\n')
    
    
    for filename in glob.glob(os.path.join(folderPath, "UNITHG*.xml")):
        #print filename
    
        #Define output file name
        name = str(os.path.basename(filename)[:])
        name = name.replace('UNITHG_', '')
        name = name.replace('_UpdateStates.xml', '')
        print 'UHG - > ' + name
        #print name
        
        csv_file.write(name + ',')    
        
        #Open .xml file and temporary .txt file to write .xml contents to
        xml_file = open(filename, 'r')
        txt_file = open(working_dir +'\\' + name + '.txt', 'w')
    
        #Write contents of .xml file to the temporary .txt file
        for line in xml_file:
            txt_file.write(line)
    
        #Close the open files
        xml_file.close()
        txt_file.close()
    
        #Open .txt file with .xml contents in read mode and create output .txt file where parameters will be written
        txt_file = open(working_dir +'\\' + name + '.txt', 'r')
    
        ###UHG_DURATION
        #Find line number with UHG_DURATION value
        #Line number is saved when loop breaks
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'UHG_DURATION' in line:
                break
    
        #Set cursor back to beginning of txt_file that is being read
        txt_file.seek(0)
    
        #Section/line of .txt file with desired parameter value
        section = txt_file.readlines()[line_num:line_num+1]
    
        for line in section:
            #Write only numbers and decimals to output file
            line = re.sub("[^0123456789\.\-]", "", line)
    
        ###DRAINAGE_AREA
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'DRAINAGE_AREA' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num:line_num+1]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            area = line
            csv_file.write(area + ',')
            
        ###UHG_INTERVAL
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'UHG_INTERVAL' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num:line_num+1]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            interval = line
            csv_file.write(interval + ',')
    
        ###CONSTANT_BASE_FLOW
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'CONSTANT_BASE_FLOW' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num:line_num+1]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
    
        ###UHG_ORDINATES
        txt_file.seek(0)
    
        UHG_time = []
        UHG_flow = []
        
        #Set time 0 values
        ordinate = 0
        flow = 0
        csv_file.write('0' + ',')
        UHG_time.append(ordinate)
        UHG_flow.append(ordinate)
        
        for line in txt_file:
            if 'row A' in line:
                ordinate = ordinate + 6
                UHG_time.append(ordinate)
                line = re.sub("[^0123456789\.\-]", "", line)
                line_float = float(line)
                csv_file.write(line + ',')
                UHG_flow.append(line_float)
                
        #Get max UHG time value
        if uh_plots == 'on':
            max_time = numpy.max(UHG_time)
            x = range(0,max_time+6,6)
    
            fig, ax1 = plt.subplots()
            
            #Plot the data
            ax1.plot(UHG_time, UHG_flow, color='black', label='UHG', linewidth='2', zorder=5)
            ax1.plot(UHG_time, UHG_flow, 'o', color='black', ms=8, zorder=5, alpha=0.75)
            ax1.fill_between(x,UHG_flow,facecolor='gray', alpha=0.25)    
            
            #ax1.minorticks_on()
            ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
            ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
            
            majorLocator = MultipleLocator(6)
            ax1.xaxis.set_major_locator(majorLocator)
            
            ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
            
            ax1.set_xlabel('Time (hr)')
            ax1.set_ylabel('Flow (cfs)')
            
            #Make tick labels smaller/rotate for long UHGs
            if max_time >= 100:
                for label in ax1.xaxis.get_ticklabels():       
                    label.set_fontsize(8)
            if max_time >= 160:
                for label in ax1.xaxis.get_ticklabels():       
                    label.set_fontsize(6)
                    plt.xticks(rotation=90)
                    majorLocator = MultipleLocator(12)
                    ax1.xaxis.set_major_locator(majorLocator)
                    
            ax1.set_xlim([0,max_time+3])
            plt.ylim(ymin=0)
        
            #add plot legend with location and size
            ax1.legend(loc='upper right', prop={'size':10})
                
            plt.title(name + ' UHG / ' + 'Area (mi2) = ' + area)
                
            output_folder = csv_file_out +'\\UHG_plots\\'
            if os.path.exists(output_folder) == False:
                os.makedirs(output_folder)
            figname = output_folder + name + '_UHG.png'
                
            plt.savefig(figname, dpi=100, bbox_inches='tight')
            
            plt.clf()    
            plt.close()
        
        txt_file.close()
        
        csv_file.write('\n')    
        
        #Delete temporary .txt file holding .xml contents
        os.remove(working_dir +'\\' + name + '.txt')
    
    csv_file.close() 

#LAG-K SECTION---------------------------------------------------------------
#loop through Lag-K .xlm files in folderPath
if lagk == 'on':
    print 'Processing LAG-K parameters...'
    lag_params = ['CURRENT_OUTFLOW','CURRENT_STORAGE','TSIDA','SETLAG','SETK']
    new_lag_params = ['CURRENT_OUTFLOW','CURRENT_STORAGE','INFLOW_TS_ID','CONSTANT_LAG_VALUE','CONSTANT_K_VALUE']
    csv_file = open(csv_file_out + '\\' + '_' + RFC + '_LAGK_Params_' + param_source + '_slim.csv', 'w')
    
    csv_file.write('BASIN,Current Outflow,Current Storage,Inflow Basin,SETLAG,SETK,JK,JLAG,LAG1,Q1,LAG2,Q2,LAG3,Q3,LAG4,Q4,LAG5,Q5,LAG6,Q6,LAG7,Q7,LAG8,Q8,LAG9,Q9,LAG10,Q10,LAG11,Q11,LAG12,Q12,LAG13,Q13,LAG14,Q14,K1,KQ1,K2,KQ2,K3,KQ3,K4,KQ4,K5,KQ5,K6,KQ6,K7,KQ7,K8,KQ8,K9,KQ9,K10,KQ10,K11,KQ11,K12,KQ12,K13,KQ13,K14,KQ14'+'\n')
    
    for filename in glob.glob(os.path.join(folderPath, "LAGK*.xml")):
        #print filename
        lag_time = []
        lag_Q = []
        K_time = []
        K_Q = []
    
        #Define output file name
        name = str(os.path.basename(filename)[:])
        name = name.replace('LAGK_', '')
        name = name.replace('_UpdateStates.xml', '')
        print 'LAG/K -> ' + name
        
        csv_file.write(name + ',')    
        
        #Open .xml file and temporary .txt file to write .xml contents to
        xml_file = open(filename, 'r')
        txt_file = open(working_dir +'\\' + name + '.txt', 'w')
            
        #Write contents of .xml file to the temporary .txt file
        for line in xml_file:
            txt_file.write(line)
    
        #Close the open files
        xml_file.close()
        txt_file.close()
    
        #Open .txt file with .xml contents in read mode and create output .txt file where parameters will be written
        txt_file = open(working_dir +'\\' + name + '.txt', 'r')
            
        ### CURRENT_OUTFLOW
        #Find line number with CURRENT_OUTFLOW value
        #Line number is saved when loop breaks
        var_count = 0
        for variable in lag_params:
            xml_file = open(filename, 'r')
            line_num = 0
            check = 'na'
            for line in xml_file:
                line_num += 1
                if variable in line or new_lag_params[var_count] in line:
                    check = 'go'
                    xml_file.close()
                    break
            xml_file = open(filename,'r')
            #Section/line of .txt file with desired parameter value
            section = xml_file.readlines()[line_num:line_num+2]
            if check != 'go':
                csv_file.write('na,')
            else:
                for line in section:
                    if 'parameter' not in line and 'description' not in line:
                        #Write only numbers and decimals to output file
                        #line = re.sub("[^0123456789\.\-]", "", line)
                        parse = line.replace('>', '"')
                        parse = parse.replace('<','"')
                        par_value = parse.split('"')[2]
                        csv_file.write(par_value + ',')
                        if variable == 'TSIDA' or variable == 'INFLOW_TS_ID':
                            inflow_basin = par_value
            xml_file.close()
            var_count += 1
        xml_file = open(filename, 'r')
        
        #################### JK ####################
        ### parameter names have been updated to include new names with the CHPS LAG/K mod release ###
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'id="JK"' in line or 'id="NUMBER_OF_KQ_PAIRS"' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num:line_num+2]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            if line != '': # ignore description line in new xml format
                csv_file.write(line + ',')
                jk = int(line)
        
        #################### JLAG ####################
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'id="JLAG"' in line or 'id="NUMBER_OF_LAGQ_PAIRS"' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num:line_num+2]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            if line != '': # ignore description line in new xml format
                csv_file.write(line + ',')
                jlag = int(line)
    
        #################### LAGQ ####################
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'LAGQ_PAIRS' in line:
                break
    
        txt_file.seek(0)
        if jlag == 0:
            end_line = 3
        else:
            end_line = (jlag * 2)+2
    
        section = txt_file.readlines()[line_num+2:line_num+end_line]
    
        count = 0
        for line in section:
            ### old format ###
            if 'row A' in line and 'B' not in line:
                spl = line.split('"')
                if jlag != 0:
                    csv_file.write(spl[1] + ',')
                if count % 2 ==0:
                    lag_time.append(float(spl[1]))
                else:
                    lag_Q.append(float(spl[1]))
                count += 1
            ### new format ###
            if 'row A' in line and 'B' in line:
                spl = line.split('"')
                if jlag != 0:
                    csv_file.write(spl[1] + ',' + spl[3] + ',')
                lag_time.append(float(spl[1]))
                lag_Q.append(float(spl[3]))
        #print lag_time
        #print lag_Q
                
        if jlag == 0:
            jlag = 1
            csv_file.write(',' + ',')
        while jlag < 14:
            csv_file.write('' + ',' + '' + ',')
            jlag += 1      
    
        #################### KQ ####################
        txt_file.seek(0)
        line_num = 0
        for line in txt_file:
            line_num += 1
            if 'KQ_PAIRS' in line:
                break
    
        txt_file.seek(0)
        end_line = (jk * 2)+3
        
        txt_file.seek(0)
        if jk == 0:
            end_line = 3
        else:
            end_line = (jk * 2)+2
    
        section = txt_file.readlines()[line_num+2:line_num+end_line]
        count = 0
        for line in section:
            ### old format ###
            if 'row A' in line and 'B' not in line:
                spl = line.split('"')
                if jk != 0:
                    csv_file.write(spl[1] + ',')
                if count % 2 ==0:
                    K_time.append(float(spl[1]))
                else:
                    K_Q.append(float(spl[1]))
                count += 1
            ### new format ###
            if 'row A' in line and 'B' in line:
                spl = line.split('"')
                if jk != 0:
                    csv_file.write(',' + ',')
                K_time.append(float(spl[1]))
                K_Q.append(float(spl[3]))
        #print K_time
        #print K_Q
            
        if jk == 0:
            jk = 1
            csv_file.write('' + ',')
        while jk < 14:
            csv_file.write('' + ',' + '' + ',')
            jk += 1
    
        txt_file.close()
        csv_file.write('\n')
    
        ######################## LAG/K Plots ###########################
        if lag_plots == 'on' and len(K_time)>1 and len(lag_time)>1: 
            #Get max Lag/K time value
            max_time = numpy.max(lag_time + K_time)
            x = range(0,int(max_time)+6,6)
            fig, ax1 = plt.subplots()
            
            #Plot the data
            ax1.plot(lag_time, lag_Q, 'g-o', label='LAG', linewidth='2', zorder=5, ms=5)
            ax1.plot(K_time, K_Q, 'r-o', label='K', linewidth='2', zorder=5, ms=5)
            #ax1.fill_between(x,UHG_flow,facecolor='gray', alpha=0.25)    
            
            #ax1.minorticks_on()
            ax1.grid(which='major', axis='both', color='black', linestyle='-', zorder=3)
            ax1.grid(which='minor', axis='both', color='grey', linestyle='-', zorder=3)
            
            majorLocator = MultipleLocator(6)
            ax1.xaxis.set_major_locator(majorLocator)
            
            ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
            
            ax1.set_xlabel('Time (hr)')
            ax1.set_ylabel('Flow (cfs)')
            
            #Make tick labels smaller/rotate for long UHGs
            if max_time >= 100:
                for label in ax1.xaxis.get_ticklabels():       
                    label.set_fontsize(8)
            if max_time >= 160:
                for label in ax1.xaxis.get_ticklabels():       
                    label.set_fontsize(6)
                    plt.xticks(rotation=90)
                    majorLocator = MultipleLocator(12)
                    ax1.xaxis.set_major_locator(majorLocator)
                    
            ax1.set_xlim([0,max_time+3])
            plt.ylim(ymin=0)
            
            #add plot legend with location and size
            ax1.legend(loc='upper right', prop={'size':10})
                
            plt.title(name[:5] + ': ' + inflow_basin + ' LAG/K Parameters')
                
            output_folder = csv_file_out +'\\LAGK_plots\\'
            if os.path.exists(output_folder) == False:
                os.makedirs(output_folder)
            figname = output_folder + name + '_LAGK.png'
                
            plt.savefig(figname, dpi=100, bbox_inches='tight')
            
            plt.clf()    
            plt.close()
            
        #Delete temporary .txt file holding .xml contents
        os.remove(working_dir +'\\' + name + '.txt')
    
    csv_file.close() 
###################################################################################################################################    
print 'Script Complete'
print str(datetime.now())
