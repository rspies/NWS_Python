# created by Ryan Spies 
# 1/28/2016
# Python 2.7
# Bokeh updated to 0.11
# Description: generate an interactive plot of QME vs. SQME from the CHPS export csv
# Output to html file for viewing interactive plot

from bokeh.plotting import Figure, output_file, show, save #importing figure (lower case f) results in increasing file size with each plot
from bokeh.models import Range1d
import os
import pandas as pd
#import datetime

os.chdir("../..")
maindir = os.getcwd() + os.sep + 'Calibration_NWS' + os.sep
################## User Input ########################
RFC = 'NWRFC_FY2016'
sim_type = 'draft'
plot_type = 'normal' # choices: 'log' or 'normal'
######################################################
input_dir = maindir + RFC[:5] + os.sep + RFC + os.sep + 'Calibration_TimeSeries' + os.sep + sim_type

for input_file in os.listdir(input_dir+ os.sep + 'QME_SQME'):
    print input_file
    basin = input_file.split('_')[0]
    read_file = open(input_dir + os.sep + 'QME_SQME' + os.sep + input_file, 'r')
    test = pd.read_csv(read_file,sep=',',skiprows=2,
                usecols=[0,1,2],parse_dates=['date'],names=['date', 'OBS', 'SQIN'])
    ### assign column data to variables
    print 'Populating data arrays for obs & calibrated streamflow...'
    
    date_calib = test['date'].tolist()  # convert to list (indexible)
    Q_calib = test['SQIN'].tolist()
    discharge = test['OBS'].tolist()
    read_file.close()
    
    # find max flow for plotting limit
    max_find = []
    max_find.append(max(Q_calib))
    max_find.append(max(discharge))
    max_Q = int(max(max_find)) + 5
    
    # output to static HTML file
    output_file(input_dir + os.sep + 'interactive_plots' + os.sep + basin + '_QME_SQME_'+ sim_type + '.html')
    
    # create a new plot
    # log plot add this:  y_axis_type="log"
    print 'Creating bokeh plot...'
    if plot_type != 'log':
        p = Figure(
           tools="xpan,xwheel_zoom,xbox_zoom,reset,resize,save",
           y_range = Range1d(start=0,end=max_Q,bounds=(0,max_Q)), x_range = Range1d(start=date_calib[0],end=date_calib[-1],
           bounds=(date_calib[0],date_calib[-1])),
           title=basin + ' Daily Streamflow (CMS)', x_axis_type="datetime",
           x_axis_label='Date', y_axis_label='Streamflow (CMSD)',plot_width=1300, plot_height=600, lod_factor=20, lod_threshold=50
        )
    elif plot_type == 'log':
        p = Figure(
           tools="xpan,xwheel_zoom,xbox_zoom,reset,resize,save",
           y_range = Range1d(start=0,end=max_Q,bounds=(0,max_Q)), x_range = Range1d(start=date_calib[0],end=date_calib[-1],
           bounds=(date_calib[0],date_calib[-1])),
           title=basin + ' Daily Streamflow (CMS)', x_axis_type="datetime",
           x_axis_label='Date', y_axis_label='Streamflow (CMSD)', y_axis_type="log", plot_width=1300, plot_height=600, lod_factor=20, lod_threshold=50
        )
    #p.y_range = DataRange1d(bounds=(0,150))
    
    # add some renderers
    p.line(date_calib, discharge, legend="Observed - QME", line_width=3, line_color = "black")
    #p.circle(date_calib, discharge, legend="Observed - QME", fill_color="white", size=3)
    p.line(date_calib, Q_calib, legend="Simulated - SQME", line_width=3, line_color="red")
    #p.circle(date_calib, Q_calib, legend="Simulated - SQME", fill_color="red", line_color="red", size=3)
    #p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")
    
    # show the results
    #show(p)
    print 'Saving plot...'
    save(p)