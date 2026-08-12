# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import os
import glob
import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re as re
# %load_ext memory_profiler
from datetime import datetime

# +
inflst=glob.glob('../data/era*july 2026.xlsx')
print(inflst)

era_sheets= pd.read_excel(inflst[0], sheet_name=None)
print(era_sheets.keys())
# -



r1_trans=era_sheets['1_transport']
print (r1_trans)

s1_trans=r1_trans[r1_trans['geo'].str[0:2]!='EU']
s1_trans


def selyear(shin):
    s_maxyr=shin.groupby('geo')['time'].agg('max').reset_index()
    s_maxyr.sort_values('time')
    yrus=s_maxyr['time'].min()
    print ('Year use %.0f'%(yrus))
    if( yrus!=s_maxyr['time'].max()):
        print ('Skipping newer data')
        print (s_maxyr[yrus!=s_maxyr['time']])
    return yrus
s1_trans_yrus = selyear(s1_trans)

#noyr BE na fr & pass, PL na pass
p1_trans=pd.pivot(s1_trans[s1_trans_yrus-1==s1_trans['time']],index='geo',values='values',columns='variable')
p1_trans.at['IE','Freight transport tkm'] =0
p1_trans =p1_trans.reset_index()
p1_trans

# +
#data on the lines
# -

r41_lines=era_sheets['4_1_lines']
print (r41_lines)

s41_lines=r41_lines[r41_lines['geo'].str[0:2]!='EU']
s41_lines

s41_lines_yrus = selyear(s41_lines)



p41_lines=pd.pivot(s41_lines[s41_lines_yrus==s41_lines['time']],index='geo',values='values',columns='variable').reset_index()

# +
#performance
# -

r61_perf=era_sheets['6_1_perf']
print (r61_perf)

s61_perf=r61_perf[r61_perf['geo'].str[0:2]!='EU']
s61_perf

s61_perf_yrus = selyear(s61_perf)

p61_perf=pd.pivot(s61_perf[s61_perf_yrus==s61_perf['time']],index='geo',values='values',columns='variable').reset_index()

p61_perf

# +
#market
# -



r63_market=era_sheets['6_3_market']
print (r63_market)

s63_market=r63_market[r63_market['geo'].str[0:2]!='EU']
s63_market

s63_market_yrus = selyear(s63_market)

p63_market=pd.pivot(s63_market[s63_market_yrus==s63_market['time']],index='geo',values='values',columns='variable')
p63_market['Foreign incumbent market share in the rail freight market'].fillna(0,inplace=True)
p63_market['Foreign incumbent market share in the rail passenger market'].fillna(0,inplace=True)
p63_market=p63_market.reset_index()

p63_market['largfr']=p63_market['Domestic incumbent market share in the rail freight market'].where(
   p63_market['Domestic incumbent market share in the rail freight market'] > 
  p63_market['Foreign incumbent market share in the rail freight market'],
   p63_market['Foreign incumbent market share in the rail freight market'])
p63_market['largpass']=p63_market['Domestic incumbent market share in the rail passenger market'].where(
   p63_market['Domestic incumbent market share in the rail passenger market'] > 
  p63_market['Foreign incumbent market share in the rail passenger market'],
   p63_market['Foreign incumbent market share in the rail passenger market'])

p63_market





# +
#combine data of transport and lines to get impression of network
# -

trdens=p1_trans.merge(p41_lines,how='outer')
trdens

trdens['ptsum'] = trdens['Freight transport tkm'] + trdens['Passenger transport pkm']
trdens['pctfr'] = trdens['Freight transport tkm'] /  trdens['ptsum']
trdens['dens'] = trdens['ptsum']  / trdens['Line kilometres']

# +
fig, axi = plt.subplots(figsize=(8, 8))

ax=trdens.sort_values('pctfr').plot.barh(ax=axi,x='geo', y='pctfr',
             title='Fraction of freight traffic of all traffic per country', color='green',legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('freight tkm/ (freight tkm + passenger pkm)')
figname = "../output/fracfreight.svg"
plt.savefig(figname,dpi=300)

# +
fig, axi = plt.subplots(figsize=(8, 8))

ax=trdens.sort_values('dens').plot.barh(ax=axi,x='geo', y='dens',
             title='Density of traffic per country', color='green',legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('million (freight tkm + passenger pkm) / line km')
figname = "../output/usgdens.svg"
plt.savefig(figname,dpi=300)

# +
#now find largest market share
# -

nrgshare=trdens.merge(p63_market,how='outer')
nrgshare


nrgshare['elargfr'] =nrgshare['largfr'] * nrgshare['pctfr']/100
nrgshare['elargpass'] =nrgshare['largpass'] * (1- nrgshare['pctfr'])/100
nrgshare['elargany']=nrgshare['elargfr'].where(
   nrgshare['elargfr'] > nrgshare['elargpass'] ,nrgshare['elargpass']  )
nrgshare['elargwh']='lightblue'
nrgshare['elargwh'] = nrgshare['elargwh'].where(
   nrgshare['elargfr'] > nrgshare['elargpass'] ,'green'  )

nrgshare.to_excel('../output/plotnrs.xlsx')
nrgshare

fig, axi = plt.subplots(figsize=(8, 8))
#nrgshare['elargany'].fillna(0,inplace=True)
nrgshare= nrgshare.sort_values('elargany')
ax=nrgshare.plot.barh(ax=axi,x='geo', y='elargany',
             title='Energy usage of largest operator \n(light blue : freight, green : passenger)', 
                      color=nrgshare['elargwh'],legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('fraction of network use')
figname = "../output/nrglargop.svg"
plt.savefig(figname,dpi=300)


