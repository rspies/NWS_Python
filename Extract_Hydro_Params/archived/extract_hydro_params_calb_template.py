#Extract_Hydro_Params.py
#Ryan Spies
#ryan.spies@amec.com
#AMEC
#Description: extracts SAC-SMA/UNITHG/LAG-K parameters values
#from CHPS configuration .xml files located in the Config->ModuleConfigFiles
#directory and ouputs a .csv file with all parameters

# NOTE: this script differs from the extract_hydro_params_XXRFC_sa.py by using
# the output UH and SACSMA calibration mods in the CHPS CALB SA version which 
# has a slightly different format than the original SA .xml modulparfiles

#-----------------------------------------------------------------------------
########################## START USER INPUT SECTION ##########################
RFC = 'SERFC'
param_source = 'final_calb' # choices: 'final_calb'
uh_plots = 'off' # choices: 'on' or 'off' to create a .png figure for each basin

#!!!!!! input directory: enter location of ModuleParFiles directory below ->
folderPath = 'P:\\NWS\\Calibration_NWS\\' + RFC + '\\Working_Calib_Files'
#!!!!!! output directory: enter ouput directory for .csv files below ->
csv_file_out = 'P:\\NWS\\Python\\Extract_Hydro_Params\\' + RFC + '\\Params_' + param_source
########################## END USER INPUT SECTION ############################
#-----------------------------------------------------------------------------

#import script modules
import os
import re
if uh_plots == 'on':
    import numpy
    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator
    from matplotlib.ticker import MultipleLocator

working_dir = os.getcwd()
print 'Script is Running...'

sac_line = 1
csv_file = open(csv_file_out +'\\' + RFC + '_SACSMA_Params_' + param_source + '.csv', 'w')
csv_file.write('BASIN,REXP,LZPK,LZFPM,PXADJ,RCI,PFREE,ZPERC,RIVA,MAPE_Input,PEADJ,LZTWM,'\
                   'RSERV,ADIMP,UZK,SIDE,LZFSM,LZSK,SMZC,UZTWM,UZFWM,PCTIM,EFC,'\
                   'JAN_ET,FEB_ET,MAR_ET,APR_ET,MAY_ET,JUN_ET,JUL_ET,AUG_ET,SEP_ET,OCT_ET,NOV_ET,DEC_ET' + '\n')

#SAC-SMA SECTION--------------------------------------------------------------
#loop through SACSMA files in folderPath
print 'Processing SACSMA parameters...'
for filename in os.listdir(folderPath + '\\SAC_SMA\\'):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('SACSMA_', '')
    name = name.replace('_UpdateStates.xml', '')
    #print name

    csv_file.write(name + ',')

    #Open .xml file and temporary .txt file to write .xml contents to
    xml_file = open(folderPath + '\\SAC_SMA\\' + filename, 'r')
    txt_file = open(working_dir +'\\' + name + '.txt', 'w')

    #Write contents of .xml file to the temporary .txt file
    for line in xml_file:
        txt_file.write(line)

    #Close the open files
    xml_file.close()
    txt_file.close()

    #Open .txt file with .xml contents in read mode and create output .txt file where parameters will be written
    txt_file = open(working_dir +'\\' + name + '.txt', 'r')
    output_file = open(working_dir +'\\' + name + '_SACSMA_Params.txt', 'w')

    #Write data headers
    output_file.write('PARAMETER,VALUE' + '\n')

    ###REXP
    #Find line number with REXP value
    #Line number is saved when loop breaks
    line_num = 0
    for line in txt_file:
        line_num += 1
        if 'REXP' in line:
            break

    #Set cursor back to beginning of txt_file that is being read
    txt_file.seek(0)

    #Section/line of .txt file with desired parameter value
    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        #Write only numbers and decimals to output file
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('REXP,' + line + '\n')

    ###LZPK
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'LZPK' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('LZPK,' + line + '\n')

    ###LZFPM
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'LZFPM' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]
    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('LZFPM,' + line + '\n')


    ###PXADJ
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'PXADJ' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('PXADJ,' + line + '\n')

    ###RUNOFF_COMPONENT_INTERVAL
    txt_file.seek(0)
    line_num=0
    if 'RUNOFF_COMPONENT_INTERVAL' not in txt_file.read():
        csv_file.write('N/A' + ',')
        output_file.write('RUNOFF_COMPONENT_INTERVAL,' + 'N/A' + '\n')
    else:
        txt_file.seek(0)
        for line in txt_file:
            line_num += 1
            if 'RUNOFF_COMPONENT_INTERVAL' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            csv_file.write(line + ',')
            output_file.write('RUNOFF_COMPONENT_INTERVAL,' + line + '\n')

    ###PFREE
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'PFREE' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('PFREE,' + line + '\n')

    ###ZPERC
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'ZPERC' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('ZPERC,' + line + '\n')

    ###RIVA
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'RIVA' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('RIVA,' + line + '\n')
        
    ###MAPE_Input
    txt_file.seek(0)
    line_num=0
    
    if 'MAPE' not in txt_file.read():
        csv_file.write('FALSE' + ',')
        output_file.write('MAPE_Input,' + 'FALSE' + '\n')
    else:
        txt_file.seek(0)
        for line in txt_file:
            line_num += 1
            if 'MAPE' in line:
                break
            
    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        if 'true' in line or 'TRUE' in line or 'True' in line:
            #line = 'TRUE'
            csv_file.write('TRUE' + ',')
            output_file.write('MAPE_Input,' + 'TRUE' + '\n')
        else:
            for line in section:
                if 'false' in line or 'FALSE' in line or 'False' in line:
                    #line = 'TRUE'
                    csv_file.write('FALSE' + ',')
                    output_file.write('MAPE_Input,' + 'FALSE' + '\n')
        
        
    ###PEADJ
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'PEADJ' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('PEADJ,' + line + '\n')

    ###LZTWM
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'LZTWM' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('LZTWM,' + line + '\n')

    ###RSERV
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'RSERV' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('RSERV,' + line + '\n')

    ###ADIMP
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'ADIMP' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('ADIMP,' + line + '\n')

    ###UZK
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'UZK' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('UZK,' + line + '\n')

    ###SIDE
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'SIDE' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('SIDE,' + line + '\n')

    ###LZFSM
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'LZFSM' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('LZFSM,' + line + '\n')

    ###LZSK
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'LZSK' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('LZSK,' + line + '\n')

    ###SMZC_INTERVAL
    txt_file.seek(0)
    line_num=0
    if 'SMZC_INTERVAL' not in txt_file.read():
        csv_file.write('N/A' + ',')
        output_file.write('SMZC_INTERVAL,' + 'N/A' + '\n')
    else:
        txt_file.seek(0)
        for line in txt_file:
            line_num += 1
            if 'SMZC_INTERVAL' in line:
                break
    
        txt_file.seek(0)
    
        section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]
    
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            csv_file.write(line + ',')
            output_file.write('SMZC_INTERVAL,' + line + '\n')

    ###UZTWM
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'UZTWM' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('UZTWM,' + line + '\n')

    ###UZFWM
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'UZFWM' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('UZFWM,' + line + '\n')

    ###PCTIM
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'PCTIM' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('PCTIM,' + line + '\n')

    ###EFC
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'EFC' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+sac_line:line_num+(sac_line+1)]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('EFC,' + line + '\n')

    ###ET_DEMAND_CURVE
    txt_file.seek(0)
    line_num=0
    for line in txt_file:
        line_num += 1
        if 'row A' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num-1:line_num]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('JAN_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num:line_num+1]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('FEB_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+1:line_num+2]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('MAR_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+2:line_num+3]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('APR_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+3:line_num+4]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('MAY_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+4:line_num+5]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('JUN_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+5:line_num+6]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('JUL_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+6:line_num+7]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('AUG_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+7:line_num+8]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('SEP_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+8:line_num+9]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('OCT_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+9:line_num+10]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('NOV_ET,' + line + '\n')

    txt_file.seek(0)

    section = txt_file.readlines()[line_num+10:line_num+11]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('DEC_ET,' + line + '\n')


    txt_file.close()
    output_file.close()

    #Delete temporary .txt file holding .xml contents
    os.remove(working_dir +'\\' + name + '.txt')

    os.remove(working_dir +'\\' + name + '_SACSMA_Params.txt')
    
    csv_file.write('\n')

csv_file.close()

#UNIT HG SECTION---------------------------------------------------------------
#loop through UNITHG .xlm files in folderPath
print 'Processing UH parameters...'
csv_file = open(csv_file_out +'\\' + RFC + '_UHG_Params_' + param_source + '.csv', 'w')

csv_file.write('BASIN, AREA (mi2),')
t = 0
while t < 600:
    csv_file.write(str(t) + ',')
    t += 6
csv_file.write('\n')


for filename in os.listdir(folderPath + '\\UH\\'):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('UNITHG_', '')
    name = name.replace('_UpdateStates.xml', '')
    #print name
    
    csv_file.write(name + ',')    
    
    #Open .xml file and temporary .txt file to write .xml contents to
    xml_file = open(folderPath + '\\UH\\' + filename, 'r')
    txt_file = open(working_dir +'\\' + name + '.txt', 'w')

    #Write contents of .xml file to the temporary .txt file
    for line in xml_file:
        txt_file.write(line)

    #Close the open files
    xml_file.close()
    txt_file.close()

    #Open .txt file with .xml contents in read mode and create output .txt file where parameters will be written
    txt_file = open(working_dir +'\\' + name + '.txt', 'r')
    output_file = open(working_dir +'\\' + name + '_UNITHG_Params.txt', 'w')

    #Write data headers
    output_file.write('PARAMETER,VALUE' + '\n')

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
        output_file.write('UHG_DURATION,' + line + '\n')

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
        output_file.write('UHG_INTERVAL,' + line + '\n')

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
        output_file.write('DRAINAGE_AREA,' + line + '\n')

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
        output_file.write('CONSTANT_BASE_FLOW,' + line + '\n')

    ###UHG_ORDINATES
    output_file.write ('\n' + 'UHG_ORDINATES' + '\n')
    output_file.write('0,0' + '\n')
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
            output_file.write(str(ordinate) + ',' + line + '\n')
            
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
            
        figname = csv_file_out +'\\' + name + '_UHG.png'
            
        plt.savefig(figname, dpi=100)
        
        plt.clf()    
        plt.close()
        #Turn interactive plot mode off (don't show figures)
        plt.ioff()    
    
    txt_file.close()
    output_file.close()
    
    csv_file.write('\n')    
    
    #Delete temporary .txt file holding .xml contents
    os.remove(working_dir +'\\' + name + '.txt')
    os.remove(working_dir +'\\' + name + '_UNITHG_Params.txt')  

csv_file.close() 

#LAG-K SECTION---------------------------------------------------------------
#loop through Lag-K .xlm files in folderPath
print 'Processing LAG-K parameters...'
csv_file = open(csv_file_out +'\\' + RFC + '_LAGK_Params_' + param_source + '.csv', 'w')

csv_file.write('BASIN,Current Outflow,Current Storage,JK,JLAG,LAG1,Q1,LAG2,Q2,LAG3,Q3,LAG4,Q4,LAG5,Q5,LAG6,Q6,LAG7,Q7,K1,KQ1,K2,KQ2,K3,KQ3,K4,KQ4,K5,KQ5,K6,KQ6,K7,KQ7'+'\n')

for filename in os.listdir(folderPath + '\\Lag_K\\'):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('LAGK_', '')
    name = name.replace('_UpdateStates.xml', '')
    #print name
    
    csv_file.write(name + ',')    
    
    #Open .xml file and temporary .txt file to write .xml contents to
    xml_file = open(folderPath + '\\Lag_K\\' + filename, 'r')
    txt_file = open(working_dir +'\\' + name + '.txt', 'w')

    #Write contents of .xml file to the temporary .txt file
    for line in xml_file:
        txt_file.write(line)

    #Close the open files
    xml_file.close()
    txt_file.close()

    #Open .txt file with .xml contents in read mode and create output .txt file where parameters will be written
    txt_file = open(working_dir +'\\' + name + '.txt', 'r')
    output_file = open(working_dir +'\\' + name + '_LAGK_Params.txt', 'w')

    ### CURRENT_OUTFLOW
    #Find line number with CURRENT_OUTFLOW value
    #Line number is saved when loop breaks
    line_num = 0
    check = 'na'
    for line in txt_file:
        line_num += 1
        if 'CURRENT_OUTFLOW' in line:
            check = 'go'
            break

    #Set cursor back to beginning of txt_file that is being read
    txt_file.seek(0)

    #Section/line of .txt file with desired parameter value
    section = txt_file.readlines()[line_num:line_num+1]
    if check != 'go':
        csv_file.write('na,')
        output_file.write('CURRENT_OUTFLOW,' + 'na' + '\n')
    else:
        for line in section:
            #Write only numbers and decimals to output file
            line = re.sub("[^0123456789\.\-]", "", line)
            csv_file.write(line + ',')
            output_file.write('CURRENT_OUTFLOW,' + line + '\n')

    ### CURRENT_STORAGE
    txt_file.seek(0)
    line_num = 0
    check = 'na'
    for line in txt_file:
        line_num += 1
        if 'CURRENT_STORAGE' in line:
            check = 'go'
            break

    txt_file.seek(0)
    section = txt_file.readlines()[line_num:line_num+1]
    if check != 'go':
        csv_file.write('na,')
        output_file.write('CURRENT_STORAGE,' + 'na' + '\n')
    else:
        for line in section:
            line = re.sub("[^0123456789\.\-]", "", line)
            csv_file.write(line + ',')
            output_file.write('CURRENT_STORAGE,' + line + '\n')
    
    ### JK
    txt_file.seek(0)
    line_num = 0
    for line in txt_file:
        line_num += 1
        if 'id="JK"' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num:line_num+1]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('JK,' + line + '\n')
        jk = int(line)
    
    ### JLAG
    txt_file.seek(0)
    line_num = 0
    for line in txt_file:
        line_num += 1
        if 'id="JLAG"' in line:
            break

    txt_file.seek(0)

    section = txt_file.readlines()[line_num:line_num+1]

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('JLAG,' + line + '\n')
        jlag = int(line)

    ### LAGQ
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

    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('LAGQ_PAIRS,' + line + '\n')
            
    if jlag == 0:
        jlag = 1
        csv_file.write('0' + ',')
    while jlag < 7:
        csv_file.write('' + ',' + '' + ',')
        jlag += 1      

    ### KQ
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
    
    for line in section:
        line = re.sub("[^0123456789\.\-]", "", line)
        csv_file.write(line + ',')
        output_file.write('KQ_PAIRS,' + line + '\n')
        
    if jk == 0:
        jk = 1
        csv_file.write('0' + ',')
    while jk < 7:
        csv_file.write('' + ',' + '' + ',')
        jk += 1

    txt_file.close()
    output_file.close()
    
    csv_file.write('\n')    
    
    #Delete temporary .txt file holding .xml contents
    os.remove(working_dir +'\\' + name + '.txt')
    os.remove(working_dir +'\\' + name + '_LAGK_Params.txt')  

csv_file.close() 
print 'Script Complete'
