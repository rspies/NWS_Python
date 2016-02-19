# created by Ryan Spies 
# Generated: 2/14/2016
# Python 2.7
# Description: basemap plot of basin shapefiles

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os

os.chdir("../..")
maindir = os.getcwd()

################### user input #########################
shp_file = maindir + os.sep + 'GIS\SERFC\SERFC_FY2016\Shapefiles_fromSERFC\calb_basins\calb_basins'
out_map = maindir + os.sep + 'GIS\\SERFC\\SERFC_FY2016\\map_output\\basemap_plots'
################# end user input #########################
fig = plt.figure()
m = Basemap(llcrnrlon=-86.0,llcrnrlat=30.3,urcrnrlon=-80.5,urcrnrlat=35.5,
             resolution='i', projection='cyl')

m.arcgisimage(service='World_Shaded_Relief', xpixels = 1500, verbose= True)
m.drawmapboundary(fill_color='aqua')
#m.fillcontinents(color='#ddaa66',lake_color='aqua')
m.drawcoastlines()
m.drawstates(color='1.0', linewidth=1.0)
m.drawrivers(color='#0000ff')

m.readshapefile(shp_file, 'SERFC _basins')

plt.savefig(out_map + os.sep + 'SERFC_basins.png', dpi=200, bbox_inches='tight')
plt.show()
print 'Map completed!!'