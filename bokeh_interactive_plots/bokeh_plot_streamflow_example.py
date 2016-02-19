# created by Ryan Spies 
# 1/28/2016
# Python 2.7
# Bokeh updated to 0.11
# Description: generate an interactive plot of QME vs. SQME
# Output to html file for viewing

from bokeh.plotting import figure, output_file, show, save
from bokeh.models import Range1d
import os
import pandas as pd
#import datetime

maindir = os.getcwd()
input_dir = maindir + os.sep + 'example'

for input_file in os.listdir(input_dir):
    print input_file
    basin = input_file.split('_')[0]
    read_file = open(input_dir + os.sep + input_file, 'r')
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
    output_file("Ryan_Example_bokeh.html")
    
    # create a new plot
    print 'Creating bokeh plot...'
    p = figure(
       tools="xpan,xwheel_zoom,xbox_zoom,reset,resize,save",
       y_range = Range1d(start=0,end=max_Q,bounds=(0,max_Q)), x_range = Range1d(start=date_calib[0],end=date_calib[-1],
       bounds=(date_calib[0],date_calib[-1])),
       title=basin + ' Daily Streamflow (CMS)', x_axis_type="datetime",
       x_axis_label='Date', y_axis_label='Streamflow (CMSD)',plot_width=1300, plot_height=600, lod_factor=20, lod_threshold=50
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