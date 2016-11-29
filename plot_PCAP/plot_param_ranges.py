#plot_param_ranges
#python script to plot SAC/Snow param ranges 
#data plotted: pre-calb, draft calb, final calb, Anderson, apriori
#Author: Ryan Spies
#rspies@lynkertech.com
#Lynker Technologies

print "Start Script"

import os
import matplotlib.pyplot as plt
plt.ioff()
import matplotlib.patches as patches
import matplotlib.image as image
from matplotlib.path import Path
import matplotlib.patheffects as PathEffects
import pandas as pd
from pylab import *

os.chdir("../..")
maindir = os.getcwd()
############################### User Input ####################################
rfc = 'NERFC_FY2017'
fx_group = '' # leave blank if not processing by fx group
plot_type = 'initial' # choices: 'initial', 'draft' or 'final' #version of the calibrated params to use (initial/pre-calb is always plotted)
group_limits = 'on' # 'on' or 'off' -> on calculates the mean of all tasked calibration basins in the initial param csv
sac_plot = 'on' # plot sacsma
snow_plot = 'on' # plot snow17 
e19 = 'on' # create e19 folder with lower res image for chps display
wm_image = maindir + os.sep + 'Python' + os.sep + 'Extract_Hydro_Params' + os.sep + 'Lynker Logo for On-Screen.jpg' # lynker logo for plot

if fx_group == '':
    csv_read_init = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'Params_pre_calb' + os.sep 
    csv_read_apri = maindir + os.sep + 'GIS' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'Apriori'
    csv_dir_calb = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc  + os.sep + 'Params_'+plot_type+'_calb' + os.sep 
else:
    csv_read_init = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + fx_group + os.sep + 'Params_pre_calb' + os.sep
    csv_read_apri = maindir + os.sep + 'GIS' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'Apriori' + os.sep + fx_group 
    csv_dir_calb = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + fx_group + os.sep + 'Params_'+plot_type+'_calb' + os.sep
############################ End User Input ###################################

if sac_plot == 'on':
    print 'Creating SAC-SMA plots...'
    #### read data into pandas dataframes
    csv_sac_ander = open(maindir + os.sep + 'Python' + os.sep + 'Extract_Hydro_Params' + os.sep + 'Anderson_SACSMA_param_ranges.csv', 'r')
    csv_read_init_sac = open(csv_read_init + '_' + rfc + '_SACSMA_Params_pre_calb_slim.csv', 'r')
    data_init = pd.read_csv(csv_read_init_sac, delimiter=',', index_col=False, skip_footer=0, header=0).set_index('NAME') #reindex to avoid data shifting
    data_ander = pd.read_csv(csv_sac_ander, delimiter=',', skip_footer=0, header=0).set_index('Anderson') #reindex to avoid data shifting
    csv_read_init_sac.close(); csv_sac_ander.close()
    
    if plot_type == 'draft' or plot_type == 'final': 
        csv_read_calb = open(csv_dir_calb + '_' + rfc + '_SACSMA_Params_'+plot_type+'_calb_slim.csv', 'r')
        data_calb = pd.read_csv(csv_read_calb, delimiter=',', index_col=False, skip_footer=0, header=0).set_index('NAME') #reindex to avoid data shifting
        csv_read_calb.close()
    
    sac_pars = ['UZTWM','UZFWM','UZK','PCTIM','ADIMP','EFC','SIDE','RSERV','PXADJ','LZTWM','LZFSM','LZSK','LZFPM','LZPK','REXP','ZPERC','PFREE','RIVA']
    if plot_type == 'initial':
        all_basins = data_init.index.values.tolist() #list of all basins from the pre_calb parameter csv
    else:
        all_basins = data_calb.index.values.tolist() #list of all basins from the calb parameter csv
    
    for basin in all_basins:
        print basin
        count = 1; plot_num = 1; x=1.1; apbasin = basin
        if len(basin)>5: # trim off 'LOC' ending on some ch5id's for apriori lookup
            apbasin = basin.replace("LOC", "")
            print apbasin + ' --> basin name longer than 5 char'
        if os.path.isfile(csv_read_apri + os.sep + apbasin + os.sep + apbasin + '_apriori_parameters.csv'):
            data_apri = pd.read_csv(csv_read_apri + os.sep + apbasin + os.sep + apbasin + '_apriori_parameters.csv', delimiter=',', index_col=False, skip_footer=0, header=0).set_index('Parameter')
            data_apri = data_apri.to_dict()
        else:
            if os.path.isfile(csv_read_apri + os.sep + apbasin[:5] + os.sep + apbasin[:5] + '_apriori_parameters.csv'):
                apbasin = basin[:5]
                data_apri = pd.read_csv(csv_read_apri + os.sep + apbasin + os.sep + apbasin + '_apriori_parameters.csv', delimiter=',', index_col=False, skip_footer=0, header=0).set_index('Parameter')
                data_apri = data_apri.to_dict()
                print 'Warning Apriori file found for: ' + basin[:5] + '--> not exact match to ' + basin
                print 'Continuing...' 
            else:
                print basin + ' apriori file missing...'
                data_apri = {}
        
        fig = plt.figure(figsize=(8,3.5))          
        fig.suptitle(basin + ' SAC-SMA '  + 'Parameters',y=1.02,fontsize=14)
        codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
        tk = 0.3; tg = 0.2; ta = 0.1
        for param in sac_pars:
            #print 'Plotting: ' + param
            ax1 = plt.subplot(2,9,plot_num)            
            
            #### rectangle plot for anderson range (http://matplotlib.org/users/path_tutorial.html)
            and_verts = [(x-tk, data_ander.loc['MIN',param]), # left, bottom
            (x-tk, data_ander.loc['MAX',param]), # left, top
            (x+tk, data_ander.loc['MAX',param]), # right, top
            (x+tk, data_ander.loc['MIN',param]), # right, bottom
            (0., 0.)]
            path = Path(and_verts, codes)
            patch = patches.PathPatch(path, facecolor='oRange', lw=.5, zorder=2, alpha=0.7,label='Anderson/Lynker Range')
            ax1.add_patch(patch)
            
            #### rectangle plot for apriori range 
            if len(data_apri)>0 and apbasin + '_sac_' + param.lower() in data_apri['Max']:
                and_verts = [(x-ta, data_apri['Min'][apbasin+'_sac_'+param.lower()]), # left, bottom
                (x-ta, data_apri['Max'][apbasin+'_sac_'+param.lower()]), # left, top
                (x+ta, data_apri['Max'][apbasin+'_sac_'+param.lower()]), # right, top
                (x+ta, data_apri['Min'][apbasin+'_sac_'+param.lower()]), # right, bottom
                (0., 0.)]
                path = Path(and_verts, codes)
                patch = patches.PathPatch(path, facecolor='green', lw=.5, zorder=4, alpha=0.7,label='Apriori Range')
                ax1.add_patch(patch)
                
                    
            #### calculate and plot all tasked basin param limits - max/min (regional limits)
            if group_limits == 'on':
                gmax = data_init[param].max()
                gmin = data_init[param].min()
                and_verts = [(x-tg, gmin), # left, bottom
                (x-tg, gmax), # left, top
                (x+tg, gmax), # right, top
                (x+tg, gmin), # right, bottom
                (0., 0.)]
                path = Path(and_verts, codes)
                patch = patches.PathPatch(path, facecolor='#cc66ff', lw=.5, zorder=3, alpha=0.4,label='FX-Group Range')
                ax1.add_patch(patch)
            
            #### plot initial param value with red bar marker
            ax1.plot(x,data_init.loc[basin,param], color='red', markersize=20, marker='_', mew=1.6, linewidth=2, zorder=5, label = rfc[:5] + ' Initial')
            
            #### plot draft/final calb param value with blue bar marker
            if plot_type == 'draft' or plot_type == 'final':
                ax1.plot(x,data_calb.loc[basin,param], color='blue', markersize=20, marker='_', mew=1.6, linewidth=2, zorder=5, alpha = 0.7, label = 'Lynker ' + 'Calb')
            
            ############## plot settings below #################
            ax1.minorticks_on()
            ax1.grid(which='major', axis='y', color='grey', linestyle='-', zorder=3, alpha=0.3)
            
            ax1.set_ylim([ax1.get_yticks()[0]-(ax1.get_yticks()[1]-ax1.get_yticks()[0])/2,ax1.get_yticks()[-1]+(ax1.get_yticks()[1]-ax1.get_yticks()[0])/2]) # extend y-axis limits 10%
            if float(ax1.get_yticks()[0]) == 0:
                ax1.set_ylim([ax1.get_yticks()[0]-ax1.get_yticks()[1]/2,ax1.get_yticks()[-1]+(ax1.get_yticks()[1]-ax1.get_yticks()[0])/2])
            ax1.set_yticks(ax1.get_yticks()[1:-1]) # trim first and last ylabels to prevent overlap of chart area
            
            #### define pad to move ytick labels inside plot
            if len(str(ax1.get_yticks()[-1]))<=4 and float(ax1.get_yticks()[-1]) > 2.0:
                ax1.tick_params(direction='in', pad=-12)
            elif len(str(ax1.get_yticks()[-1]))<=4:
                ax1.tick_params(direction='in', pad=-17)
            elif len(str(ax1.get_yticks()[-1]))<=5:
                ax1.tick_params(direction='in', pad=-18)
            else:
                ax1.tick_params(direction='in', pad=-19)
            ax1.tick_params(labelsize=5)
            
            ax1.set_xlim([0,2])
            ax1.get_xaxis().set_visible(False)
            
            #### add annotated labels to data points for initial
            ax1.annotate(str(data_init.loc[basin,param]), (x+.35,data_init.loc[basin,param]), fontsize='5',zorder=7, color='red')
            #### add annotated labels to data points for draft/final
            if plot_type == 'draft' or plot_type == 'final': 
                ax1.annotate(str(data_calb.loc[basin,param]), (x-0.25,data_calb.loc[basin,param]), fontsize='4.5', zorder=7, color='blue', path_effects=[
            PathEffects.withStroke(linewidth=2, foreground="w")])
            
            plt.ioff()
            plt.title(param, fontsize='10')
            count +=2; plot_num += 1
            
            #### add a single legend outside the subplots
            if param == 'LZTWM':
                ax1.legend(fontsize=6,bbox_to_anchor=(8.5, 0.00),ncol=5, frameon=False,markerscale=0.5)
                
        ### add Lynker logo watermark in plot corner
        im = image.imread(wm_image)
        newax = fig.add_axes([0.85,0.95, 0.1, 0.1], anchor='NE') # create axis to place image (x,y,scalex,scaley)
        newax.imshow(im, alpha = 0.3, extent=(0,1,1,1.4))
        newax.axis('off')
        #plt.imshow(im, aspect='auto', extent=(1,1,1,1), zorder=-100)
            
        print 'Saving figure...'
        if fx_group == '':
            figname = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'SACSMA' + os.sep + basin + '_sacsma_param_' + plot_type + '_analysis.png'
            basin_e19 = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'E19' + os.sep + basin + '_calb'
        else:
            figname = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + fx_group + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'SACSMA' + os.sep + basin + '_sacsma_param_' + plot_type + '_analysis.png'
            basin_e19 = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + fx_group + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'E19' + os.sep + basin + '_calb'
        
        plt.tight_layout()
        subplots_adjust(left=None, bottom=None, right=None, top=0.9, wspace=0.1, hspace=0.2) #adjust white space 
        plt.savefig(figname, bbox_inches='tight', dpi=350)
        if e19 == 'on':
            print 'Saving E19 figure...'
            ### for E19 chps display basin directories
            if os.path.isdir(basin_e19) == False:
                os.mkdir(basin_e19)
            ### for E19 chps display
            plt.savefig(basin_e19 + os.sep + basin + '_sacsma_param_' + plot_type + '_analysis.png', bbox_inches='tight', dpi=150)
        plt.close()
        plt.show()

############################################################################

if snow_plot == 'on':
    print 'Creating SNOW-17 plots...'
    #### read data into pandas dataframes
    csv_snow_ander = open(maindir + os.sep + 'Python' + os.sep + 'Extract_Hydro_Params' + os.sep + 'Anderson_SNOW17_param_ranges.csv', 'r')
    csv_read_init_snow = open(csv_read_init + '_' + rfc + '_SNOW17_Params_pre_calb_slim.csv', 'r')
    data_init = pd.read_csv(csv_read_init_snow, delimiter=',', index_col=False, skip_footer=0, header=0).set_index('NAME') #reindex to avoid data shifting
    data_ander = pd.read_csv(csv_snow_ander, delimiter=',', skip_footer=0, header=0).set_index('Anderson') #reindex to avoid data shifting
    csv_read_init_snow.close(); csv_snow_ander.close()
    
    if plot_type == 'draft' or plot_type == 'final': 
        csv_read_calb = open(csv_dir_calb + '_' + rfc + '_SNOW17_Params_'+plot_type+'_calb_slim.csv', 'r')
        data_calb = pd.read_csv(csv_read_calb, delimiter=',', index_col=False, skip_footer=0, header=0).set_index('NAME') #reindex to avoid data shifting
        csv_read_calb.close()
    
    snow_pars = ['SCF','MFMAX','MFMIN','UADJ','SI','PLWHC','PXTEMP','TIPM','NMF']
    if plot_type == 'initial':
        all_basins = data_init.index.values.tolist() #list of all basins from the pre_calb parameter csv
    else:
        all_basins = data_calb.index.values.tolist() #list of all basins from the calb parameter csv
    
    for basin in all_basins:
        print basin
        count = 1; plot_num = 1; x=1.1; apbasin = basin
        if len(basin)>5: # trim off 'LOC' ending on some ch5id's for apriori lookup
            apbasin = basin.replace("LOC", "")
            print apbasin + ' --> basin name longer than 5 char'
        if os.path.isfile(csv_read_apri + os.sep + apbasin + os.sep + apbasin + '_apriori_parameters.csv'):
            data_apri = pd.read_csv(csv_read_apri + os.sep + apbasin + os.sep + apbasin + '_apriori_parameters.csv', delimiter=',', index_col=False, skip_footer=0, header=0).set_index('Parameter')
            data_apri = data_apri.to_dict()
        else:
            if os.path.isfile(csv_read_apri + os.sep + apbasin[:5] + os.sep + apbasin[:5] + '_apriori_parameters.csv'):
                apbasin = basin[:5]
                data_apri = pd.read_csv(csv_read_apri + os.sep + apbasin + os.sep + apbasin + '_apriori_parameters.csv', delimiter=',', index_col=False, skip_footer=0, header=0).set_index('Parameter')
                data_apri = data_apri.to_dict()
                print 'Warning Apriori file found for: ' + basin[:5] + '--> not exact match to ' + basin
                print 'Continuing...' 
            else:
                print basin + ' apriori file missing...'
                data_apri = {}
        
        fig = plt.figure(figsize=(8,1.75))          
        fig.suptitle(basin + ' SNOW-17 ' + 'Parameters',y=1.14,fontsize=14)
        codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
        tk = 0.3; tg = 0.2; ta = 0.1
        for param in snow_pars:
            #print 'Plotting: ' + param
            ax1 = plt.subplot(1,9,plot_num)            
            
            #### rectangle plot for anderson range (http://matplotlib.org/users/path_tutorial.html)
            and_verts = [(x-tk, data_ander.loc['MIN',param]), # left, bottom
            (x-tk, data_ander.loc['MAX',param]), # left, top
            (x+tk, data_ander.loc['MAX',param]), # right, top
            (x+tk, data_ander.loc['MIN',param]), # right, bottom
            (0., 0.)]
            path = Path(and_verts, codes)
            patch = patches.PathPatch(path, facecolor='orange', lw=.5, zorder=2, alpha=0.7,label='Anderson/Lynker Range')
            ax1.add_patch(patch)
            
            #### rectangle plot for apriori range 
#            if len(data_apri)>0 and apbasin + '_sac_' + param.lower() in data_apri['Max']:
#                and_verts = [(x-ta, data_apri['Min'][apbasin+'_sac_'+param.lower()]), # left, bottom
#                (x-ta, data_apri['Max'][apbasin+'_sac_'+param.lower()]), # left, top
#                (x+ta, data_apri['Max'][apbasin+'_sac_'+param.lower()]), # right, top
#                (x+ta, data_apri['Min'][apbasin+'_sac_'+param.lower()]), # right, bottom
#                (0., 0.)]
#                path = Path(and_verts, codes)
#                patch = patches.PathPatch(path, facecolor='green', lw=.5, zorder=4, alpha=0.7,label='Apriori Range')
#                ax1.add_patch(patch)
                
                    
            #### calculate and plot all tasked basin param limits - max/min (regional limits)
            if group_limits == 'on':
                gmax = data_init[param].max()
                gmin = data_init[param].min()
                and_verts = [(x-tg, gmin), # left, bottom
                (x-tg, gmax), # left, top
                (x+tg, gmax), # right, top
                (x+tg, gmin), # right, bottom
                (0., 0.)]
                path = Path(and_verts, codes)
                patch = patches.PathPatch(path, facecolor='#cc66ff', lw=.5, zorder=3, alpha=0.4,label='FX-Group Range')
                ax1.add_patch(patch)
            
            #### plot initial param value with red bar marker
            ax1.plot(x,data_init.loc[basin,param], color='red', markersize=20, marker='_', mew=1.6, linewidth=2, zorder=5, label = rfc[:5] + ' Initial')
            
            #### plot draft/final calb param value with blue bar marker
            if plot_type == 'draft' or plot_type == 'final':
                ax1.plot(x,data_calb.loc[basin,param], color='blue', markersize=20, marker='_', mew=1.6, linewidth=2, zorder=5, alpha = 0.7, label = 'Lynker ' + 'Calb')
            
            ############## plot settings below #################
            ax1.minorticks_on()
            ax1.grid(which='major', axis='y', color='grey', linestyle='-', zorder=3, alpha=0.3)
            
            ax1.set_ylim([ax1.get_yticks()[0]-(ax1.get_yticks()[1]-ax1.get_yticks()[0])/2,ax1.get_yticks()[-1]+(ax1.get_yticks()[1]-ax1.get_yticks()[0])/2]) # extend y-axis limits 10%
            if float(ax1.get_yticks()[0]) == 0:
                ax1.set_ylim([ax1.get_yticks()[0]-ax1.get_yticks()[1]/2,ax1.get_yticks()[-1]+(ax1.get_yticks()[1]-ax1.get_yticks()[0])/2])
            ax1.set_yticks(ax1.get_yticks()[1:-1]) # trim first and last ylabels to prevent overlap of chart area
            
            #### define pad to move ytick labels inside plot
            if len(str(ax1.get_yticks()[-1]))<=4 and float(ax1.get_yticks()[-1]) > 2.0:
                ax1.tick_params(direction='in', pad=-12)
            elif len(str(ax1.get_yticks()[-1]))<=4:
                ax1.tick_params(direction='in', pad=-17)
            elif len(str(ax1.get_yticks()[-1]))<=5:
                ax1.tick_params(direction='in', pad=-18)
            else:
                ax1.tick_params(direction='in', pad=-19)
            ax1.tick_params(labelsize=5)
            
            ax1.set_xlim([0,2])
            ax1.get_xaxis().set_visible(False)
            
            #### add annotated labels to data points for initial
            ax1.annotate(str(data_init.loc[basin,param]), (x+.35,data_init.loc[basin,param]), fontsize='5',zorder=7, color='red')
            #### add annotated labels to data points for draft/final
            if plot_type == 'draft' or plot_type == 'final': 
                ax1.annotate(str(data_calb.loc[basin,param]), (x-0.25,data_calb.loc[basin,param]), fontsize='4.5', zorder=7, color='blue', path_effects=[
            PathEffects.withStroke(linewidth=2, foreground="w")])
            
            plt.ioff()
            plt.title(param, fontsize='10')
            count +=2; plot_num += 1
            
            #### add a single legend outside the subplots
            if param == 'MFMAX':
                ax1.legend(fontsize=6,bbox_to_anchor=(7.0, 0.00),ncol=5, frameon=False,markerscale=0.5)
                
        ### add Lynker logo watermark in plot corner
        im = image.imread(wm_image)
        newax = fig.add_axes([0.80,1.01, 0.16, 0.16], anchor='NE') # create axis to place image (x,y,scalex,scaley)
        newax.imshow(im, alpha = 0.3, extent=(0,1,1,1.4)) # location of image  (left, right, bottom, top)
        newax.axis('off')
        
        print 'Saving figure...'
        if fx_group == '':
            figname = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'SNOW17' + os.sep + basin + '_snow17_param_' + plot_type + '_analysis.png'
            basin_e19 = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'E19' + os.sep + basin + '_calb'
        else:
            figname = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + fx_group + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'SNOW17' + os.sep + basin + '_snow17_param_' + plot_type + '_analysis.png'
            basin_e19 = maindir + os.sep + 'Extract_Hydro_Params' + os.sep + rfc[:5] + os.sep + rfc + os.sep + fx_group + os.sep + 'param_plots' + os.sep + plot_type + os.sep + 'E19' + os.sep + basin + '_calb'
        
        
        plt.tight_layout()
        subplots_adjust(left=None, bottom=None, right=None, top=0.9, wspace=0.1, hspace=0.2) #adjust white space 
        plt.savefig(figname, bbox_inches='tight', dpi=350)
        ### for E19 chps display basin directories
        if e19 == 'on':
            print 'Saving E19 figure...'
            if os.path.isdir(basin_e19) == False:
                os.mkdir(basin_e19)
            ### for E19 chps display
            plt.savefig(basin_e19 + os.sep + basin + '_snow17_param_' + plot_type + '_analysis.png', bbox_inches='tight', dpi=150)
        plt.close()
        plt.show()

print "End Script"

