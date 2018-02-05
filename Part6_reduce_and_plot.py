import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

ed=pd.read_csv('Pandas_all_Energy_data.csv')
ed = ed.ix[:,['YY','ENERGY','DEPTH','OCEANNAME']]
ed = ed[ed['DEPTH']>0]
ed['DTH2'] = ed.apply(lambda row: 100.0*round(row.DEPTH/100.0), axis=1)

# all energies vs depth
# ax = ed.plot(x='DTH2', y='ENERGY', kind='kde', figsize=(10, 6))
# arr = ax.get_children()[0]._x
# plt.xticks(np.linspace(arr[0], arr[-1]), rotation=90)
# plt.show()

print('Max Energy for each depth:')
gurade = ed.groupby('DEPTH').max()
gurade.to_csv('MaxEnergyAll.csv')
print('Mean Energy for each depth:')
gurade = ed.groupby('DEPTH').mean()
gurade.to_csv('MeanEnergyAll.csv')

olst = ['ARTC','ATLN','ATLS','PACN','PACS', 'INDC','ANTC']
for ocean in olst:
    dfc = ed[ed['OCEANNAME']==ocean]
    print('Max Energy for each depth:')
    gurade = dfc.groupby('DEPTH').max()
    gurade.to_csv('MaxEnergy'+ocean+'.csv')
    print('Mean Energy for each depth:')
    gurade = dfc.groupby('DEPTH').mean()
    gurade.to_csv('MeanEnergy'+ocean+'.csv')
    #dfc.to_csv('energies_' + ocean +'.csv')

# ax = ed.plot(x='DTH2', y='ENERGY', kind='kde', figsize=(10, 6))
# arr = ax.get_children()[0]._x
# plt.xticks(np.linspace(arr[0], arr[-1]), rotation=90)
# plt.show()

evsdmx = ed.groupby('DEPTH').max()
evsdmx.ENERGY.plot.density()

evsdme = ed.groupby('DEPTH').mean()
evsdme.ENERGY.plot.density()

olst = ['ARTC','ATLN','ATLS','PACN','PACS']
for ocean in olst:
    dfc = ed[ed['OCEANNAME']==ocean]
    dfc.ENERGY.plot.density()
    plt.show()

ed.ENERGY.plot.density()
plt.show()


