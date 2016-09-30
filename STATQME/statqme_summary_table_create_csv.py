#Created on September 16, 2014
#@author: rspies
# Python 2.7
# This script parses through the HTML reports created by CHPS and outputs a 
# csv file with summary statistics

import os
from bs4 import BeautifulSoup
import csv
os.chdir('../..')

############################## User Input ###################################
RFC = 'WGRFC_FY2016'
fx_group = '' # leave blank if not processing by fx group
sim_type = 'initial-CalibrationPeriod' # specific to type of simulation: 'initial' or 'draft' or 'final' and 'CalibrationPeriod' or 'ValidationPeriod'
variables = ['local', 'outflow', 'inflow'] # choices: 'local', 'outflow', 'inflow'

if fx_group == '':
    maindir = os.getcwd() + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries'
else:
    maindir = os.getcwd() + os.sep + 'Calibration_NWS' + os.sep + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + fx_group    
html_folder = maindir + os.sep + 'statqme_html_reports' + os.sep + 'statqme-' + sim_type + os.sep
########################### End User Input ##################################
for variable in variables:
    print 'Processing -> ' + variable + ' for ' + RFC + ' --> ' + fx_group
    #html_folder_inflow = maindir + '\\statqme_inflow_reports\\final_inflow\\'
    #html_folder_output = maindir + '\\statqme_output_reports\\'
    months = ['Basin','October','November','December','January','February','March','April','May','June','July','August','September','Year Avg.']
    abv_months = ['Basin','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Year Avg.']
    basin_fit_summary ={}
    output_csv_dir = maindir + os.sep + 'statqme_' + variable + '_csv' + os.sep + sim_type + os.sep 
    if os.path.exists(output_csv_dir) == False:
        os.makedirs(output_csv_dir)
    
    ###################### Output Files #####################################
    ##### monthly stats new csv file ####
    month_csv_pbias = open(output_csv_dir + variable + '_monthly_mean_pbias_' + sim_type + '.csv','wb')
    month_csv_bias = open(output_csv_dir + variable + '_monthly_mean_bias_' + sim_type + '.csv','wb')
    month_csv_rms = open(output_csv_dir + variable + '_monthly_mean_percent_daily_rms_error_' + sim_type + '.csv','wb')
    mpbias = csv.writer(month_csv_pbias)
    mbias = csv.writer(month_csv_bias)
    mrms = csv.writer(month_csv_rms)
    mpbias.writerow(['Mean Monthly % Bias'])
    mbias.writerow(['Mean Monthly Bias (CMSD)'])
    mrms.writerow(['Monthly % Daily RMS Error'])
    mpbias.writerow(abv_months)
    mbias.writerow(abv_months)
    mrms.writerow(abv_months)
    ##### daily fit stats new csv ####
    basin_fit_stats = open(output_csv_dir + variable + '_all_fit_stats_' + sim_type + '.csv','wb')
    basin_fit = csv.writer(basin_fit_stats)
    basin_fit.writerow(['MULTI-YEAR STATISTICAL SUMMARY'])
    basin_fit.writerow(['Basin','Correlation Coef', 'Daily RMS Error (CMSD)', 'Daily Absolute Error (CMSD)'])
    ##### complete simulation period summary ####
    basin_all_sim_stats = open(output_csv_dir + variable + '_all_sim_stats_' + sim_type + '.csv','wb')
    basin_all_sim = csv.writer(basin_all_sim_stats)
    basin_all_sim.writerow(['SIMULATION PERIOD STATISTICAL SUMMARY'])
    basin_all_sim.writerow(['Basin','Mean SQME (CMSD)','Mean QME (CMSD)','Mean % Bias','Mean Bias (CMSD)','Correlation Coef', 'Daily RMS Error (CMSD)', 'Daily Absolute Error (CMSD)','Daily Data Points'])
    ##### flow interval stats new csv file ####
    output_flow_dir = output_csv_dir + os.sep + 'flow_categories' + os.sep
    if os.path.exists(output_flow_dir) == False:
        os.makedirs(output_flow_dir)
    flow_cat_new = open(output_flow_dir + '_all_basins_' + variable + '_flow_categories_stats_' + sim_type + '.csv','wb')
    flow_cat = csv.writer(flow_cat_new)
    ########################################################################
    ignore_list = ['PCFM7','LK2F1','OLNF1','TREF1']
    html_files = {}
    # finds both inflow, outflow, and local html reports individually
    basins = []
    for each in sorted([f for f in os.listdir(html_folder) if f.endswith('.html')]):
        basin_name = each.split('_')[-1].strip('.html')
        name = each
        if variable == 'outflow' and basin_name not in ignore_list and 'output' in name and 'inflow' not in name:
            basins.append(basin_name); html_files[basin_name]=name
        if variable == 'inflow' and basin_name not in ignore_list and 'inflow' in name:
            basins.append(basin_name); html_files[basin_name]=name
        if variable == 'local' and basin_name not in ignore_list and 'local' in name:
            basins.append(basin_name); html_files[basin_name]=name
    print basins
    
    for basin in basins:
        print basin
        html_file = open(html_folder + os.sep + html_files[basin],'r')
        print html_files[basin]
        #test_file = open(maindir + '\\temp.txt','w')
        month_data = {'October':[],'November':[],'December':[],'January':[],'February':[],'March':[],
                      'April':[],'May':[],'June':[],'July':[],'August':[],'September':[],'Year Avg.':[]}
        
        soup = BeautifulSoup(html_file) # read in html file
        #test_file.write(soup.prettify())
        
        ############### Monthly Stats - All Years #####################
        # SQME River Discharge Simulated Mean CMSD, QME River Discharge Observed Mean CMSD, % BIAS, MONTHLY BIAS CMSD, 
        # MAXIMUM ERROR CMSD, % AVERAGE ABSOLUTE ERROR, % DAILY RMS ERROR
        month_check = ''; count = 1 # script outputs the desired variable twice (only take odd index)
        for child in soup.find(id="tableStyle4_scrollable").descendants:
            each = str(child.string).strip()
            #print repr(each)
            if each in months:
                month_check = each
            if month_check != '' and each != month_check:
                if count % 2 ==1: 
                    month_data[month_check].append(each)
                count += 1
        ### Seperate section for year averge stats ###
        month_check = ''; count = 1
        for child in soup.find(id="tableStyle5_scrollable").descendants:
            each = str(child.string).strip()
            #print repr(each)
            if each in months or each == 'Year Avg.':
                month_check = each
            if month_check != '' and each != month_check:
                if count % 2 ==1: 
                    month_data[month_check].append(each)
                count += 1
        #for child in soup.find(id="tableStyle4_scrollable").descendants:
        #    print child
        #    print(child.string)
        
        ############### Fit Statistics - All Years #####################
        #  DAILY RMS ERROR CMSD, DAILY ABSOLUTE ERROR CMSD, CORRELATION COEF,
        #  LINE OF BEST FIT A, LINE OF BEST FIT B       
        count = 1    
        for child in soup.find(id="tableStyle3_scrollable").descendants:
            each = str(child.string).strip()
            #print repr(each)
            if each != 'None' and each != 'Year Avg':
                if count % 2 ==1 and each != '':  
                    if basin in basin_fit_summary:
                        basin_fit_summary[basin].append(each)
                    else:
                        basin_fit_summary[basin]=[each]
                count += 1
        
        ################### Flow Interval Statistics ######################
        #### interval values ####
        count = 1
        flow_int = {'a':[],'b':[],'c':[],'d':[],'e':[],'f':[],'g':[]}
        cats = ['a','b','c','d','e','f','g']    
        for child in soup.find(id="tableStyle7").descendants:
            each = str(child.string).strip()
            if each != 'None' and each != 'FLOW INTERVAL' and each != 'CMSD' and each != '' and each != '-':
                #print str(count) + ' : ' + each
                if count % 2 ==1: 
                    if count <= 4:
                        flow_int['a'].append(each)
                    if count > 4 and count <=8:
                        flow_int['b'].append(each)
                    if count > 8 and count <=12:
                        flow_int['c'].append(each)
                    if count > 12 and count <=16:
                        flow_int['d'].append(each)
                    if count > 16 and count <=20:
                        flow_int['e'].append(each)
                    if count > 20 and count <=24:
                        flow_int['f'].append(each)
                    if count > 24 and count <=26:
                        flow_int['g'].append(each)
                        flow_int['g'].append(' - ')
                count += 1
        #### statistics ####
        # number of cases, sqme river discharge simulated mean (cmsd), QME river discharge obs mean (cmsd),
        # % bias, bias (sim-obs) mm, max error (cmsd), % avg absolute error, % daily rms error
        count = 1   
        check_missing = [15,31,47,63,79,95,111] #index of "# of cases" to look for missing rows
        for child in soup.find(id="tableStyle6").descendants:
            #print child.string
            if str(child.string) == ' ': #check for missing values in flow cat
                each = '--'
            else:
                each = str(child.string).strip()
            if each != 'None' and each != 'FLOW INTERVAL' and each != 'CMSD' and each != '' and each != '\n' and each != '-':
                if count % 2 ==1: 
                    if count > 13 and count <=29:
                        flow_int['a'].append(each)
                    if count > 29 and count <=45:
                        flow_int['b'].append(each)
                    if count > 45 and count <=61:
                        flow_int['c'].append(each)
                    if count > 61 and count <=77:
                        flow_int['d'].append(each)
                    if count > 77 and count <=93:
                        flow_int['e'].append(each)
                    if count > 93 and count <=109:
                        flow_int['f'].append(each)
                    if count > 109 and count <=125:
                        flow_int['g'].append(each)
                    #print str(count) + ' : ' + each
                count += 1
            #print str(count) + '    ' + str(child.string) + '    ' + each
            #if count in check_missing and str(each) == '0':
            #    count+=14
        if basin in basin_fit_summary: # check that statistics data is available for basin (no data if no qme)
            dpoints = 0
            flow_cat_basin = open(output_csv_dir + os.sep + 'flow_categories' + os.sep + basin + '_' + variable + '_flow_categories_stats_' + sim_type + '.csv','wb')
            flow_cat_b = csv.writer(flow_cat_basin)
            flow_cat.writerow(''); flow_cat_b.writerow('')
            flow_cat.writerow([basin +' Flow Interval Statistics']);flow_cat_b.writerow([basin +' Flow Interval Statistics'])
            flow_cat.writerow(['From','To','Number of Cases','SQME River Discharge Simulated Mean (CMSD)','QME River Discharge Observed Mean (CMSD)','% Bias','Bias (Sim-Obs) MM','Maximum Error (CMSD)','Percent Average Absolute Error','Percent Daily RMS Error'])       
            flow_cat_b.writerow(['From','To','Number of Cases','SQME River Discharge Simulated Mean (CMSD)','QME River Discharge Observed Mean (CMSD)','% Bias','Bias (Sim-Obs) MM','Maximum Error (CMSD)','Percent Average Absolute Error','Percent Daily RMS Error'])    
            for cat in cats:
                data = []
                ### calculated number of data points
                if flow_int[cat][2] != ' ':
                    dpoints = dpoints + int(flow_int[cat][2])
                for each in flow_int[cat]:
                    data.append(each)
                flow_cat.writerow(data)
                flow_cat_b.writerow(data)
            flow_cat_basin.close() 
            ################ Write data to CSV file #################################
            mpbias.writerow([basin, month_data['October'][2],month_data['November'][2],month_data['December'][2],month_data['January'][2],month_data['February'][2],
                            month_data['March'][2],month_data['April'][2],month_data['May'][2],month_data['June'][2],month_data['July'][2],month_data['August'][2],month_data['September'][2],month_data['Year Avg.'][2]])
            mbias.writerow([basin, month_data['October'][3],month_data['November'][3],month_data['December'][3],month_data['January'][3],month_data['February'][3],
                            month_data['March'][3],month_data['April'][3],month_data['May'][3],month_data['June'][3],month_data['July'][3],month_data['August'][3],month_data['September'][3],month_data['Year Avg.'][3]])
            mrms.writerow([basin, month_data['October'][6],month_data['November'][6],month_data['December'][6],month_data['January'][6],month_data['February'][6],
                            month_data['March'][6],month_data['April'][6],month_data['May'][6],month_data['June'][6],month_data['July'][6],month_data['August'][6],month_data['September'][6],month_data['Year Avg.'][6]])
            basin_fit.writerow([basin, basin_fit_summary[basin][2], basin_fit_summary[basin][0], basin_fit_summary[basin][1]]) 
            basin_all_sim.writerow([basin, month_data['Year Avg.'][0], month_data['Year Avg.'][1], month_data['Year Avg.'][2], month_data['Year Avg.'][3], basin_fit_summary[basin][2], basin_fit_summary[basin][0], basin_fit_summary[basin][1], str(dpoints)])       
            html_file.close()
        else:
            print 'No data for basin: ' + basin         
    
    flow_cat_new.close() 
    month_csv_pbias.close()
    month_csv_bias.close()
    month_csv_rms.close()
    basin_fit_stats.close()
    basin_all_sim_stats.close()
print 'Completed!!'