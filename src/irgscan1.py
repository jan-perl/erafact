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
inflst=glob.glob('../data/2026__3__IRG-Rail_14th_MM_Report_-_Selection.xlsx')
print(inflst)

#era_sheets= pd.read_excel(inflst[0], sheet_name=None)
#print(era_sheets.keys())
# -
irg_df= pd.read_excel(inflst[0], sheet_name="Summary_1",skiprows=[1,2])
irg_df['geo'] = irg_df['Country'].str[0:2]
#irg_df


irg_df.columns

p63_market = irg_df
p63_market['Market share of foreign incumbent in the rail freight market'].fillna(0,inplace=True)
p63_market['Market share of foreign incumbent in the rail passenger market'].fillna(0,inplace=True)
p63_market=p63_market.reset_index()

p63_market['largfr']=p63_market['Market share of domestic incumbent in the rail freight market'].where(
   p63_market['Market share of domestic incumbent in the rail freight market'] > 
  p63_market['Market share of foreign incumbent in the rail freight market'],
   p63_market['Market share of foreign incumbent in the rail freight market'])
p63_market['largpass']=p63_market['Market share of domestic incumbent in the rail passenger market'].where(
   p63_market['Market share of domestic incumbent in the rail passenger market'] > 
  p63_market['Market share of foreign incumbent in the rail passenger market'],
   p63_market['Market share of foreign incumbent in the rail passenger market'])

# +
#p63_market
# -





# +
#combine data of transport and lines to get impression of network
# -

trdens=p63_market
#trdens['ptsum'] = trdens['Freight transport tkm'] + trdens['Passenger transport pkm']
trdens['pctfr'] = trdens['Share of freight services']
trdens['dens'] = trdens['Network usage intensity for total services']

fig, axi = plt.subplots(figsize=(8, 8))
trdens['domp']='lightblue'
frlim=.30
trdens['domp'].where(   trdens['pctfr'] >frlim ,'green' ,inplace=True )
trdensff=trdens.sort_values('pctfr')
ax=trdensff.plot.barh(ax=axi,x='geo', y='pctfr',
             title='Fraction of freight traffic of all traffic per country', color=trdensff['domp'],legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('% of train kilometers')
ax.annotate("",xytext=(frlim,0),xy=(frlim, 30), 
                    arrowprops=dict(arrowstyle="-"))
ax.annotate("%.0f %% freight"%(frlim*100),xytext=(frlim+.01,0),xy=(frlim+.01, 0))
figname = "../output/fracfreight.svg"
plt.savefig(figname,dpi=300)

# +
fig, axi = plt.subplots(figsize=(8, 8))
trdensds=trdens.sort_values('dens')
ax=trdensds.plot.barh(ax=axi,x='geo', y='dens',
             title='Density of traffic per country', color=trdensds['domp'],legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('train km per day / line km')
denslim=60
ax.annotate("",xytext=(denslim,0),xy=(denslim, 30), 
                    arrowprops=dict(arrowstyle="-"))
ax.annotate("density < 60",xytext=(denslim+1,0),xy=(denslim+1, 0))

figname = "../output/usgdens.svg"
plt.savefig(figname,dpi=300)

# +
fig, axi = plt.subplots(figsize=(8, 8))
trdensds=trdens.sort_values('dens')
sns.scatterplot(ax=axi,data=trdens,y='pctfr', x='dens',
             legend=False)
ax=axi
ax.set_ylabel('freight as % of train kilometers')
ax.set_xlabel('train km per day / line km')
ax.set_title('Freight Fraction and Density of traffic per country')
denslim=60
ax.annotate("",xytext=(denslim,0),xy=(denslim, 0.5),  arrowprops=dict(arrowstyle="-"),color='grey')
ax.annotate("density = "+str(denslim),xytext=(denslim+1,0.5),xy=(denslim+1, 0.5))
ax.annotate("",xytext=(0,frlim),xy=(130,frlim),   arrowprops=dict(arrowstyle="-"),color='grey')
ax.annotate("%.0f %% freight"%(frlim*100),xytext=(100,frlim+.01),xy=(100,frlim+.01))
for index, row in trdens.iterrows():
    # ax.annotate(row['geo'],xy=(row['dens']-3,row['pctfr']))   
    ax.text(row['dens']-.7,row['pctfr'],row['geo'], ha='right', va='top',alpha=0.5,size =16,
                    bbox=dict(boxstyle="Square,pad=0.0",
                      fc="white", ec="white", alpha=.5) )
ax.text( -3,0.42,"low traffic density\nhigh freight", ha='left', va='bottom',alpha=0.5,size =12,
                    bbox=dict(boxstyle="Square,pad=0.2",   fc="pink", ec="red", alpha=.5) )
ax.text( 90,0.42,"high traffic density\nhigh freight\nNO COUNTRY", ha='left', va='bottom',alpha=0.5,size =12,
                    bbox=dict(boxstyle="Square,pad=0.2",   fc="pink", ec="red", alpha=.5) )
ax.text( -3,0.17,"low traffic density\nlow freight", ha='left', va='bottom',alpha=0.5,size =12,
                    bbox=dict(boxstyle="Square,pad=0.2",   fc="pink", ec="red", alpha=.5) )
ax.text( 90,0.17,"high traffic density\nlow freight", ha='left', va='bottom',alpha=0.5,size =12,
                    bbox=dict(boxstyle="Square,pad=0.2",   fc="pink", ec="red", alpha=.5) )

    
figname = "../output/usgdensandfr.svg"
fig.savefig(figname,dpi=300, bbox_inches="tight")

# +
#now find largest market share
# -

nrgshare=trdens


nrgshare['elargfr'] =nrgshare['largfr'] * nrgshare['pctfr']
nrgshare['elargpass'] =nrgshare['largpass'] * (1- nrgshare['pctfr'])
nrgshare['elargany']=nrgshare['elargfr'].where(
   nrgshare['elargfr'] > nrgshare['elargpass'] ,nrgshare['elargpass']  )
nrgshare['elargwh']='lightblue'
nrgshare['elargwh'] = nrgshare['elargwh'].where(
   nrgshare['elargfr'] > nrgshare['elargpass'] ,'green'  )

nrgshare.to_excel('../output/plotnrs.xlsx')
#nrgshare

fig, axi = plt.subplots(figsize=(8, 8))
#nrgshare['elargany'].fillna(0,inplace=True)
nrgshare= nrgshare.sort_values('elargany')
ax=nrgshare.plot.barh(ax=axi,x='geo', y='elargany',
             title='Train kms of largest operator', 
                      color=nrgshare['elargwh'],legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('fraction of all train kms on network')
pbnorm=.55
ax.annotate("",xytext=(pbnorm,0),xy=(pbnorm, 30), 
                    arrowprops=dict(arrowstyle="-"))
ax.annotate("%.0f %% of all train kms"%(pbnorm*100),xytext=(pbnorm+.01,0),xy=(pbnorm+.01, 0))
figname = "../output/nrglargop.svg"
plt.savefig(figname,dpi=300)

# +
#performance join
# -

perfcmbi=nrgshare
perfcmbi['Passenger - punctuality' ] = perfcmbi['Passenger train punctuality; percent of passenger trains arriving on time']
perfcmbi['Freight - punctuality' ] = perfcmbi['Share of freight trains arriving on time']

fig, axi = plt.subplots(figsize=(8, 8))
#nrgshare['elargany'].fillna(0,inplace=True)
perfcmbi['domp']='lightblue'
perfcmbi['domp'] =perfcmbi['domp'].where(  perfcmbi['pctfr'] >0.2 ,'green'  )
perfcmbi= perfcmbi.sort_values('Passenger - punctuality')
ax=perfcmbi.plot.barh(ax=axi,x='geo', y='Passenger - punctuality',
             title='Passenger punctuality \n( network type: light blue : freight, green : passenger)', 
                      color=perfcmbi['domp'],legend=False)
ax.set_ylabel('Country')
ax.set_xlabel('Passenger punctuality')
ax.set_xlim(left=60)
figname = "../output/passpunct.svg"
plt.savefig(figname,dpi=300)

#now read operational rules
RNE_prioin=pd.read_excel("../data/trafrctry_table_with_headings_v15.xls")
#RNE_prioin

RNE_prioin.columns

RNE_prio = RNE_prioin[RNE_prioin['geo'].isna()==False]

perfwprio=perfcmbi.merge(RNE_prio,how='outer')
perfwprio

perfwprio[['geo','COUNTRY']]

sns.scatterplot(data=perfwprio,x='dens',y='Passenger - punctuality',hue='domp')

fig, axi = plt.subplots(figsize=(8, 8))
perfwprioc= perfwprio.copy()
perfwprioc['Passenger - punctuality'].fillna(50,inplace=True)
perfwprioc['First prio'].fillna('Unknown',inplace=True)
perfwprioc['First prio'].where(perfwprioc['First prio'] !='Other',"Bespoke",inplace=True)
perfwprioc= perfwprioc.sort_values('First prio',ascending=[1])
sns.scatterplot(ax=axi,data=perfwprioc,x='dens',y='Passenger - punctuality',hue='First prio',
                style='First prio',s=120,alpha=.6)
ax=axi
ax.set_ylabel('Passenger punctuality (%)')
ax.set_xlabel('train km per day / line km')
ax.set_title('Passenger punctuality versus density and dispatching rules')
nalim=55
ax.annotate("",xytext=(10,nalim),xy=(130,nalim),   arrowprops=dict(arrowstyle="-"),color='grey')
ax.annotate("below this line: punctuality not in IRG report",xytext=(50,nalim-2),xy=(50,nalim-2))
for index, row in perfwprioc.iterrows():
    # ax.annotate(row['geo'],xy=(row['dens']-3,row['pctfr']))   
    ax.text(row['dens']-.7,row['Passenger - punctuality'],row['geo'], ha='right', va='top',alpha=0.5,size =16,
                    bbox=dict(boxstyle="Square,pad=0.0",
                      fc="white", ec="white", alpha=.5) )
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
figname = "../output/denspunctdisp.svg"
fig.savefig(figname,dpi=300, bbox_inches="tight")        

sns.scatterplot(data=perfwprio,x='dens',y='Passenger - punctuality',hue='threshold for passenger trains arriving on time')

sns.scatterplot(data=perfwprio,x='Freight - punctuality',y='Passenger - punctuality',hue='First prio')

eressctry=['DK', 'BE', 'NO', 'SE', 'FI', 'CH','NL','ES','LU','PT' ]
othboth=['IT' , 'UK', 'FR' ,'SI', 'DE' ,'AT' ]
less20elec=['IE','KS' ,'EE','LT','LV' ]
print(len(eressctry+othboth))
print(len(less20elec))
print(", ".join(less20elec))
print(", ".join(eressctry))

enam=perfwprio[True==perfwprio['geo'].isin(eressctry +othboth)][['geo','COUNTRY']]
print (len(enam))
emiss = set (eressctry+othboth+less20elec)- set(perfwprio['geo']) 
print (", ".join(emiss))
enam

nomet=perfwprio[False==perfwprio['geo'].isin(eressctry +othboth+less20elec)][['geo','COUNTRY']].sort_values('geo')
print (", ".join(list (nomet['geo'])) )
nomet


