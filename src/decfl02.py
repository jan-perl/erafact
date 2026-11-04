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
#try make a decision flw
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
#os.system("pip install schemdraw[matplotlib]")
#os.system("pip install schemdraw[svgmath]")
#os.system("pip install schemdraw==0.14")

# +
#os.system("pip install ziamath")

# +
# %matplotlib inline
# %config InlineBackend.figure_format = 'svg'


import matplotlib
matplotlib.use('Agg') # Set Matplotlib's backend here


# -

import matplotlib
matplotlib.rcParams['svg.fonttype'] = 'none'

import schemdraw as schemdraw
from schemdraw import flow
import schemdraw.elements as elm

# +
#from IPython.display import Image,display

# +
#schemdraw.use('svg')
#schemdraw.svgconfig.svg2 = False

# +
txtqprio ="4.5 b\n Prio train type or\nno conflict ?"
txtqebenf='4.2 (with flow), 6.2\nBenefits from\nenergy saving ?'
dwi=7

def addpartnott(d,d1,d2m,fast,ttpo,bslo,coastin,sep): 
    d += flow.Arrow().right(d.unit*0.5).at(d1.E)
    nttd = flow.Box(w=5, h=3).anchor('W').label('Many countries:\n freight \nshunting').drop('E')
    d += nttd
    d += flow.Arrow().right(d.unit*0.5)
    dgt = flow.Decision(w=dwi, h=3.9, S='YES', E='NO').anchor('W').label('4.1.1\nCan Guess\na Timetable ?').drop('E')
    d += dgt
    d += flow.Arrow().right(d.unit*2.0)
#    d += flow.Arrow().tox(fast.E)
#    d3 = flow.Decision(w=5, h=3.9, N='YES', S='NO').anchor('W').label(txtqprio ).drop('S')
    d3 = flow.Decision(w=dwi, h=3.9,  S='either').anchor('W').label(txtqprio ).drop('S')
    d += d3
    #d += flow.Arrow().down(d.unit*2.5)
    d += flow.Arrow().toy(d2m.N)
    d2 = flow.Decision(w=dwi, h=3.9, S='YES', W='NO').anchor('N').label(txtqebenf).drop('S')
    d += d2
    d += flow.Arrow().toy(bslo.N)
    bot = flow.Box(w=5, h=3).label('5.3.1\nrun slowly\naim  40 km/h\nend speed')
    d += bot
    d += flow.Arrow().toy(sep.N)
#    d += flow.Arrow().to(coastal.N)
    coastal= flow.Start().label('Coast\na lot')
    d += coastal
    
    d += flow.Arrow().at(dgt.S).down(d.unit*0.5)
    d += flow.Box(w=8, h=2).label('own timetable\nas low prio').drop('S')
#    d += flow.Arrow().to(ttpo.N) 
    d += flow.Wire("|-", arrow='->').to(ttpo.N)

    d += flow.Arrow().at(d2.W).to(fast.E)
    
    #d += flow.StateEnd().label('Coastalot')
#    d += flow.Arrow().up(d.unit*0.5).at(d3.N)
#    d += flow.Start().anchor('S').label('Unlikely')
    return(coastal,fast) 



# +
def addpartnosav(d,d1,sep):
#,coastal,fast    
    d += flow.Arrow().right(d.unit*2.0).at(d1.E)
#    nttd = flow.Box(w=2, h=1).anchor('W').label('Some countries\n freight \nshunting').drop('E')
#    d += nttd    
    d3 = flow.Decision(w=dwi, h=3.9, S='YES', E='NO').anchor('W').label(txtqprio).drop('S')
    d += d3

    d += flow.Arrow().down(d.unit*1.5).at(d3.S)
    d += flow.Box(w=5, h=3).anchor('N').label('5.2.1\nawait connections\nrun quickly').drop('S')
    d += flow.Arrow().toy(sep.N)
    d += flow.Start().label('Wait and\nMake up')

#    d += flow.Arrow().at(d3.E).to(fast.W)

    d += flow.Arrow().at(d3.E).right(d.unit*0.5)
    fast = flow.Box(w=5, h=3).anchor('W').label('5.2.2\nget ahead\nof others').drop('S')
    d += fast
    d += flow.Arrow().toy(sep.N)
    d += flow.Start().label('Full\nspeed')

    return (fast)
# -



# +
d2=  schemdraw.Drawing() 

def addpart1(d):
    d.config(fontsize=22)
    b = flow.Start().label('START')
    d += b 
    d += flow.Arrow().down(d.unit/2)
    d1 = flow.Decision(w=dwi, h=3.9, S='YES', E='NO').label('4.1, 6.1\nMinute-level\ntimetable ?')
    d += d1
    d += flow.Arrow().length(d.unit/2)
    d3 = flow.Decision(w=dwi, h=3.9, W='OTP', S='TTP').label('4.5 a\nDispatching\nStrategy')
    d += d3
    d += flow.Arrow().length(d.unit/2)
    d2 = flow.Decision(w=dwi, h=3.9, S='YES', E='NO').label(txtqebenf)    
    d += d2
    d += flow.Arrow().length(d.unit/2)
    dpr = flow.Decision(w=dwi, h=3.9, E='YES', S='NO').label(txtqprio )
    d += dpr
    d += flow.Arrow().length(d.unit/2)
    bot = flow.Box(w=5, h=3).label('5.1.3\nrun on time-ish\naim + 1 min')
    d += bot
    d += flow.Arrow().down(d.unit/2)
    
    sep= flow.Start().label('ECO\ndrive')    
    d += sep
    
    d += flow.Arrow().left(d.unit/2).at(d3.W)
    bot = flow.Box(w=5, h=3).label('5.1.1\nbe on-time\n< +/-30 secs.').drop('S')
    d += bot
    d += flow.Arrow().toy(sep.N)
    d+= flow.Start().label('ECO\ndrive')

    (fast) = addpartnosav(d,d2,sep) 
    
    d += flow.Arrow().right(d.unit*0.5).at(dpr.E)
#    d += flow.Line().at(dpr.E).tox(fast.E)
#    d += flow.Arrow().right(d.unit/2)
    bslo = flow.Box(w=5, h=3).label('5.1.2\naim half\npunct. min').drop('S')
    d += bslo
    d += flow.Arrow().toy(sep.N)
#    d += flow.Arrow().to(coastal.N)
    coastal= flow.Start().label('ECO\ndrive')
    d += coastal    
#    d += flow.Arrow().right(d.unit*1)
#    coastal=flow.StateEnd().label('Coast\na lot')
#    d += coastal

    (coastal,fast)  = addpartnott(d,d1,d2,fast,d2,bslo,coastal,sep)            
#    d += flow.Arrow().at(bot.E).to(coastal.W)
        
addpart1(d2)
d2.save("../output/ecoflow02.svg",dpi=300)
d2.draw()

# +
d2e=  schemdraw.Drawing() 
heart="\u2764"
mok="\u2714"
mnok="\u2718"

def addebenf1(d):
    d.config(fontsize=22)
    b = flow.Start().label('START')
    d += b 
    d += flow.Arrow().down(d.unit/2)
    d1 = flow.Decision(w=8, h=5, S='Electric', E='Diesel').label('Traction type')
    d += d1
    d += flow.Arrow().length(d.unit/2)
    d3 = flow.Decision(w=8, h=5, E='> 55 %', S='< 55 %').label('operator > 55 %\nof E-Energy\nin network')
    d += d3
    d += flow.Arrow().length(d.unit/2)
    d2 = flow.Decision(w=8, h=5, E='YES', S='NO').label("Have meter ?").drop('E')
    d += d2
    
    d += flow.Arrow().length(d.unit/2)
    dvch = flow.Decision(w=8, h=5, E='NO', S='YES').label("Virtual meter\ncheaper ?" ).drop('S')
    d += dvch
    d += flow.Arrow().down(d.unit/2)
    d += flow.Box(w=8, h=2).label("Avoid\nusing meter").drop('S')
    d += flow.Arrow().down(d.unit/2)
    sep= flow.Start(w=8,h=2).label(mnok+' No profits\nby ECO-driving')    
    d += sep

    d += flow.Arrow().at(d3.E).right(d.unit*2.5)
    benf= flow.Start(w=8,h=2).anchor('W').label(mok+' Profits\nby ECO-driving')
    d += benf
    d += flow.Wire("-|", arrow='->').at(dvch.E).to(benf.S)
#    d += flow.Arrow().at(d1.E).to(benf.N)
    d += flow.Wire("-|", arrow='->').at(d1.E).to(benf.N)
    #d += flow.Arrow().at(d2.S).to(sep.W)
    d += flow.Wire("|-", arrow='->').at(d2.S).to(sep.W)
        
addebenf1(d2e)
d2e.save("../output/ebenf.svg",dpi=300)
d2e.draw()
# -


