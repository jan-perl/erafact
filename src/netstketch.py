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
import io as io
# %load_ext memory_profiler
from datetime import datetime

some_string="""line,ssiz,sposx,sposy,label
a,30,0,0,a
a,10,1,1
a,10,3,3
a,10,6,5
a,30,8,8,b
b,30,0,0,
b,10,-2,1
b,10,-3,5
b,10,-5,5
b,30,-8,8,c
c,30,0,0
c,10,1,-1
c,10,1.5,-4
c,10,2,-6
c,30,3,-8,d"""
    #read CSV string into pandas DataFrame    
netw_pts= pd.read_csv(io.StringIO(some_string), sep=",")
netw_pts['label'].fillna("",inplace=True)

# +
fig, axi = plt.subplots(figsize=(8, 8))
sns.lineplot(ax=axi,data=netw_pts,x='sposx',y='sposy',hue='line',legend=False,ci=None)
sns.scatterplot(ax=axi,data=netw_pts,x='sposx',y='sposy',size='ssiz',legend=False)
for index, row in netw_pts.iterrows(): 
        (lx,ly,lbl)=(row['sposx'] , row['sposy'], row['label'] )
        if (lbl !=''):
            axi.annotate(lbl,xy=(lx+.5,ly),size=20)

axi.set_axis_off()
figname = "../output/imag_net.svg"
plt.savefig(figname,dpi=300)
# -


