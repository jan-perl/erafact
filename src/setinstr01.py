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

# +
#illustration of set of operator choices
# -

import os
import glob
import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import re as re
import io as io
# %load_ext memory_profiler
from datetime import datetime

# +
# #%matplotlib inline
# %config InlineBackend.figure_format = 'svg'


import matplotlib
#matplotlib.use('Agg') # Set Matplotlib's backend here
# -

import matplotlib
#matplotlib.rcParams['svg.fonttype'] = 'none'



#all axes in seconds
#illustrative punctuality limit
plimill = 180
depx0 = 0
arrx0 = 3*plimill
disty=0.05
maxyfigval=0


# +
#draw distribution 
def drawdis(ax,dis0, wi, zeroxind,zeroyind, pind,dirind,prstat=False):
    global maxyfigval
    hwhmfact =  np.sqrt(2*np.log(2)) 
    mu, sigma = dis0, wi/hwhmfact
    if (dirind==0):
        sigma=wi/hwhmfact/2
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 400)
    y0=(1 / (sigma * np.sqrt(2*np.pi)))
    y = y0 * np.exp(-0.5 * ((x - mu)/sigma)**2)
    if (dirind==1):
        y=y*2*(x>mu)
        y0*=2
    elif (dirind==-1):
        y=y*2*(x<mu)
        y0*=2
    if (prstat):
        print ("area %g mean %g"%(y.sum()*(x[1]-x[0]) ,(x*y).sum() /y.sum() ))
    ax.plot(x+zeroxind, y+zeroyind,color="blue")    
    maxyfigval=max(y0,maxyfigval)
    y1=np.array([0+zeroyind,maxyfigval+zeroyind])
    x1=np.array([zeroxind,zeroxind])
    ax.plot(x1, y1,color="orange")
    x1=np.array([zeroxind+pind,zeroxind+pind])
    ax.plot(x1, y1,color="orange")
    ap=dict(arrowstyle="<->",shrinkA=0,shrinkB=0)
    if (dirind==1):
        ax.annotate(" %.0f @ %0.f"%(wi,dis0), xytext=(zeroxind+dis0+wi,y0/2+zeroyind),xy=(zeroxind+dis0, y0/2+zeroyind), 
                    arrowprops=ap,va="center")
    elif (dirind==-1):
        ax.annotate(" %.0f @ %0.f"%(wi,dis0), xytext=(zeroxind+dis0,y0/2+zeroyind),xy=(zeroxind+dis0-wi, y0/2+zeroyind), 
                    arrowprops=ap,va="center")
    else:
        ax.annotate(" %.0f @ %0.f"%(wi,dis0), xytext=(zeroxind+dis0+wi/2,y0/2+zeroyind),xy=(zeroxind+dis0-wi/2, y0/2+zeroyind), 
                    arrowprops=ap,va="center")

fig, axi = plt.subplots(figsize=(8, 8))    
drawdis(axi,plimill/2,plimill/2,arrx0,0.05,plimill,1,prstat=True)
fig.show()

# +
rtmarg=60
def addochoi(ax,nr,label, vpos, dep0, depwi,depind,arr0, arrwi,arrind,showlim=1):
    drawdis(axi,dep0,depwi,arrx0*0,-disty*vpos,0,depind)
    drawdis(axi,arr0,arrwi,arrx0*1,-disty*vpos,plimill*showlim,arrind)
    axi.annotate(nr+"\n", xy=(-arrx0*0.45,-disty*vpos) )
    axi.annotate(label+"\n", xy=(-arrx0*0.35,-disty*vpos) )
    rtsup= arr0-dep0 - (2*depwi * depind /3) + (2*arrwi * arrind /3)       
    axi.annotate("Mean runtime\nPlanT %+.0f s\nMinT %+.0f s\n"%(rtsup,rtsup+rtmarg), xy=(arrx0*0.45,-disty*vpos) )
    
fig, axi = plt.subplots(figsize=(12, 8))
axi.annotate("departing", xy=(0,-disty*0.15) )
axi.annotate("arriving", xy=(arrx0,-disty*0.15) )
axi.set_ylim(top=0,bottom=-7*disty)
axi.set_xlim(left=-arrx0/2,right=arrx0+2*plimill)
maxyfigval=0
addochoi(axi,"5.1.1","be on-time",1,0,30,1,0,30,0 )    
addochoi(axi,"5.1.2","aim punctual",2,0,30,1,plimill/2,plimill/3,0 ) 
addochoi(axi,"5.1.3","on-timish",3,0,30,1,plimill/6,plimill/3,0 )
addochoi(axi,"5.2.1","wait connect",4,rtmarg,rtmarg/1.5,0,0,plimill/2,0 )
addochoi(axi,"5.2.2","try get ahead",5,0,30,1,-rtmarg,plimill/6,1 )
addochoi(axi,"5.3.1","coastalot",6,0,30,1,plimill,plimill,0 ,showlim=0)

ylpos=-disty*6.5
axi.annotate("planned\ndeparture", xy=(0,ylpos) )
axi.annotate("planned\narrival", xy=(arrx0,ylpos) )
axi.annotate("p.limit\nill=%0.f"%(plimill), xy=(arrx0+plimill,ylpos) )
axi.set_axis_off()
fig.show()
figname = "../output/opchill.svg"
fig.savefig(figname,dpi=600)
# -


