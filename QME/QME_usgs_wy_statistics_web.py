# QME_water_year_statistics_fill.py
# 4/22/2021
# Ryan Spies (rspies@lynker.com)
# Description: uses the USGS REST service to get the water streamflow statistics
# https://waterservices.usgs.gov/rest/Statistics-Service.html

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

out_csv = r'D:\projects\2021_twdb_wgrfc_calb\data\QME'

# https://waterservices.usgs.gov/rest/Statistics-Service.html
urla = 'https://waterservices.usgs.gov/nwis/stat/?format=rdb&sites='
urlb = '&parameterCd=00060&statReportType=annual&statYearType=water'

sites_list = pd.read_csv(r'G:\Shared drives\TWDB-WGRFC Hydro Calb\hydromet_data\usgs_POR_by_basin.csv')
sites_list = sites_list[['CH5_ID...1','site_no']]
sites_list = sites_list.drop_duplicates(ignore_index=True)

for i, site in enumerate(sites_list['site_no']):
    ch5 = sites_list['CH5_ID...1'][i]
    print (i)
    print(site)

    res = requests.get(urla + '0' + str(site) + urlb)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)[0]
    text_spl = text.split('\n')
    if len(text_spl) > 10:
        text_split_filtered = [] # list to append with filtered data
        text_spl = text_spl
        for line in text_spl:
            if len(line) > 0: # need to remove blank lines (footer?)
                if line[0] != '#': # need to remove lines that start with # to remove header content
                    text_split_filtered.append(line)
        df = pd.DataFrame([x.split('\t') for x in text_split_filtered])
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        df = df[df['agency_cd'] == 'USGS']
        df = df[['year_nu','mean_va','count_nu']]
        df = df.rename(columns={'mean_va':'QME_WY_cfs', 'count_nu':'QME_WY_cnt'})
        df.columns = pd.MultiIndex.from_tuples(zip(['year',ch5,ch5],df.columns)) # add the ch5id as a multi index header
        if i == 0:
            df_merge = df
        else:
            df_merge = df_merge.merge(df,how='outer',on=[('year','year_nu')])
    else:
        print('Data not found for site: ' + str(site))
        print('Check here: ' + urla + '0' + str(site) + urlb)
        
df_merge = df_merge.sort_values([('year','year_nu')])
df_merge.to_csv(out_csv + os.sep + 'usgs_wy_qme_statistics.csv', index=False)

print('Completed!!')
