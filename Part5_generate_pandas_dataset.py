import pandas as pd
from scipy import stats
import numpy as np
import os

def findocean(coord):
    # coord will be buoydata['name'][0]
    dgns = float(coord[0])
    ns = coord[1]
    dgew = float(coord[2])
    ew = coord[3]
    # Ocean classification:
    #ARTC: between 66N - 90N
    #ANTC: between 66S - 90S
    #ATLN: between 0W - 78W and 10N - 66N
    #ATLS: <23E an <55W and 10N - 66S
    #PACN: >23E an >90W and 5N - 66N
    #PACS: >23E an >70W and 5N - 66S
    #INDC: between 23E - 117E and 10N - 66S
    #REST: rest
    if dgns>=66.0:
        if ns == 'N':
            loclbl = 'ARTC'
        else:
            loclbl = 'ANTC'
    else:
        loclbl = 'REST'
        if (dgew<78.0) and (ew == 'W') and (dgns < 66.0 and dgns > 10.0) and (ns == 'N'):
            loclbl = 'ATLN'
        if ((dgew<55.0 and ew=='W') or (dgew<23.0 and ew == 'E')) and ((dgns < 66.0 and ns == 'S') or (dgns < 10.0 and ns == 'N')):
            loclbl = 'ATLS'
        if ((dgew>90.0 and ew=='W') or (dgew>23.0 and ew == 'E')) and (dgns < 66.0 and dgns > 5.0) and (ns == 'N'):
            loclbl = 'PACN'
        if ((dgew>70.0 and ew=='W') or (dgew>23.0 and ew == 'E')) and ((dgns < 66.0 and ns == 'S') or (dgns < 5.0 and ns == 'N')):
            loclbl = 'PACS'
        if (dgew<117.0 and dgew>23.0) and (ew == 'E') and ((dgns < 66.0 and ns == 'S') or (dgns < 10.0 and ns == 'N')):
            loclbl = 'INDC'
    return(loclbl)



# MAIN funtion:
bdt = np.load('CLEANED_DATA/buoyprops_dictionary.npy').item()
counter = 0
frstflag = True
for root, dirs, files in os.walk("datasetsatt1", topdown=False):
    for name in files:
        print("Seen " + str(counter) + " files. Opening now: " + name[0:5].upper())
        xfl = pd.read_csv("datasetsatt1/" + name,sep=' ',skiprows=[1], dtype=np.float, error_bad_lines=False)
        bynmn = name[0:5].upper()
        counter += 1
        try:
            depth = bdt[bynmn][1]
            oceaname = findocean(bdt[bynmn][0])
        except KeyError:
            print('KeyErr exception with ' + bynmn)
            depth = -1
            oceaname = 'REST'
        if (counter == 1):
            # create datasets: one with energy and one only wvht and period
            # we want in general: #YY BUOYNAME WVHT DPD ENERGY WSPD LOCATION DEPTH 
            xfl['ENERGY'] = xfl.apply(lambda row: (0.5*row.WVHT*row.WVHT*row.DPD) if (float(row.WVHT<99.00) and float(row.DPD<99.00)) else np.nan, axis=1)
            xfl['BUOYNAME'] = xfl.apply(lambda row:bynmn, axis=1)
            xfl['DEPTH'] = xfl.apply(lambda row:depth, axis=1)
            xfl['OCEANNAME'] = xfl.apply(lambda row:oceaname, axis=1)
            if (list(xfl.columns.values)[0] != 'YY'):
                xfl = xfl.rename(index=str, columns={list(xfl.columns.values)[0]: 'YY'})
            dtset_all = xfl.ix[:, ['YY', 'BUOYNAME', 'WVHT', 'DPD', 'ENERGY', 'WSPD', 'OCEANNAME', 'DEPTH']]
        else:
            # then dtset_all exists and has some data (or empty), so I just need to append the new data...
            xfl['ENERGY'] = xfl.apply(lambda row: (0.5*row.WVHT*row.WVHT*row.DPD) if (float(row.WVHT<99.00) and float(row.DPD<99.00)) else np.nan, axis=1)
            xfl['BUOYNAME'] = xfl.apply(lambda row:bynmn, axis=1)
            xfl['DEPTH'] = xfl.apply(lambda row:depth, axis=1)
            xfl['OCEANNAME'] = xfl.apply(lambda row:oceaname, axis=1)
            # rename '#YY' to 'YY' if needed
            if (list(xfl.columns.values)[0] != 'YY'):
                xfl = xfl.rename(index=str, columns={list(xfl.columns.values)[0]: 'YY'})
            xfl = xfl.ix[:, ['YY', 'BUOYNAME', 'WVHT', 'DPD', 'ENERGY', 'WSPD', 'OCEANNAME', 'DEPTH']]
            #dtset_all = pd.concat([dtset_all, xfl])
            dtset_all = dtset_all.append(xfl)

dtset_all.to_csv('Pandas_all_Energy_data.csv')

#xfl = pd.read_csv("datasetsatt1/0y2w3_ALL.txt",sep=' ',skiprows=[1], dtype=np.float)
#xfl['ENERGY'] = xfl.apply(lambda row: (row.WVHT * row.DPD * row.DPD)*float(row.WVHT<99.00)*float(row.DPD<99.00), axis=1)
#xfl['BUOY'] = xfl.apply(lambda row:"0y2w3", axis=1)
#xfl = xfl.ix[:, ['#YY', 'BUOY', 'WVHT', 'DPD', 'ENERGY', 'WSPD']]
#xfl










