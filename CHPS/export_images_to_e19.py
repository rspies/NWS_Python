#python script to organize image files into an e19 folder
#Author: Ryan Spies
#rspies@lynker.com

import os
from shutil import copyfile
from PIL import Image

plot_dir = r'D:\projects\2021_twdb_wgrfc_calb\water_balance\figures'
e19_dir = r'D:\projects\2021_twdb_wgrfc_calb\water_balance\figures\E19'
basin_name_loc = 0 # this is the ordinate of the plot name that contains the basinid when split by "_"

mod_resolution = "True" # "True" or "False" to modify image resolution for better display in CHPS
basewidth = 1000

filename_append = "_watbal_summary"

if not os.path.isdir(e19_dir):
    os.mkdir(e19_dir)
else:
    print('Directory already exists: ' + e19_dir)

for plot in os.listdir(plot_dir):
    print(plot)
    if plot != "E19":
        ## Get basin id from plot file name
        basin_id = plot.replace('.','_').split("_")[basin_name_loc]
        ## Create path to basin dir in e19
        basin_dir = e19_dir + os.sep + basin_id + "_calb"
        ## Create output dir if it doesn't already exist
        if not os.path.isdir(basin_dir):
            os.mkdir(basin_dir)
        ## Copy src file to dst
        dst_plot = basin_dir + os.sep + plot[:-4] + filename_append + plot[-4:]
        copyfile(plot_dir + os.sep + plot, dst_plot)
        if mod_resolution == "True":
            img = Image.open(dst_plot)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.save(dst_plot)
    