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
# -

with schemdraw.Drawing() as drw:
    drw.config(fontsize=10, unit=.5)
    flow.Terminal().label('Start')
    flow.Arrow()
    flow.Process().label('Do something').drop('E')
    flow.Arrow().right()
    flow.Process().label('Do something\nelse')
#print(d)
    drw.draw()
    e=drw.get_segments()
    drw.save("../intermediate/test.svg",dpi=300)
    image_bytes = drw.get_imagedata('svg')
image_bytes
#plt.imshow(image_bytes)
#display(Image(image_bytes))


with schemdraw.Drawing():
    elm.Resistor()
    elm.Capacitor()
    elm.Diode()

d07= schemdraw.Drawing()
#.config(fontsize=10, unit=.5)
d07+= flow.Terminal().label('Start')
d07+=flow.Arrow()
d07+=    flow.Process().label('Do something').drop('E')
d07+=flow.Arrow().right()
d07+= flow.Process().label('Do something\nelse')
#print(d)
d07.draw()
#e=d.get_segments()
#    drw.save("../intermediate/test.svg",dpi=300)
#    image_bytes = d.get_imagedata('svg')
#image_bytes

d07.save("../intermediate/test.svg",dpi=300)



with schemdraw.Drawing() as d:
    d.config(fontsize=10, unit=.5)
    d += flow.Terminal().label('Start')
    d += flow.Arrow()
    d += flow.Process().label('Step 1')
    d += flow.Arrow()
    d += flow.Process().label('Step 2').drop('E')
    d += flow.Arrow().right()
    d += flow.Connect().label('Next')

    d += flow.Terminal().label('Start').at((4, 0))
    d += flow.Arrow().theta(-45)
    d += flow.Process().label('Step 1')
    d += flow.Arrow()
    d += flow.Process().label('Step 2').drop('E')
    d += flow.Arrow().right()
    d += flow.Connect().label('Next')

with schemdraw.Drawing() as d:
    d += flow.Start().label('START')
    d += flow.Arrow().down(d.unit/3)
    h = flow.Decision(w=5.5, h=4, S='YES').label('Hey, wait,\nthis flowchart\nis a trap!')
    d += (h)
    d += flow.Line().down(d.unit/4)
    d += flow.Wire('c', k=3.5, arrow='->').to(h.E)

# +
#Recreation of XKCD 518.
# -

with schemdraw.Drawing() as d:
    d.config(fontsize=11)
    b = flow.Start().label('START')
    d += b 
    d += flow.Arrow().down(d.unit/2)
    d1 = flow.Decision(w=5, h=3.9, E='YES', S='NO').label('DO YOU\nUNDERSTAND\nFLOW CHARTS?')
    d += d1
    d += flow.Arrow().length(d.unit/2)
    d2 = flow.Decision(w=5, h=3.9, E='YES', S='NO').label('OKAY,\nYOU SEE THE\nLINE LABELED\n"YES"?')
    d += d2
    d += flow.Arrow().length(d.unit/2)
    d3 = flow.Decision(w=5.2, h=3.9, E='YES', S='NO').label('BUT YOU\nSEE THE ONES\nLABELED "NO".')
    d += d3

    d += flow.Arrow().right(d.unit/2).at(d3.E)
    d += flow.Box(w=2, h=1.25).anchor('W').label('WAIT,\nWHAT?')
    d += flow.Arrow().down(d.unit/2).at(d3.S)
    listen = flow.Box(w=2, h=1).label('LISTEN.')
    d += listen
    d += flow.Arrow().right(d.unit/2).at(listen.E)
    hate = flow.Box(w=2, h=1.25).anchor('W').label('I HATE\nYOU.')
    d += hate
    
    d += flow.Arrow().right(d.unit*3.5).at(d1.E)
    good = flow.Box(w=2, h=1).anchor('W').label('GOOD')
    d += good
    d += flow.Arrow().right(d.unit*1.5).at(d2.E)
    d4 = flow.Decision(w=5.3, h=4.0, E='YES', S='NO').anchor('W').label('...AND YOU CAN\nSEE THE ONES\nLABELED "NO"?')
    d += d4

    d += flow.Wire('-|', arrow='->').at(d4.E).to(good.S)
    d += flow.Arrow().down(d.unit/2).at(d4.S)
    d5 = flow.Decision(w=5, h=3.6, E='YES', S='NO').label('BUT YOU\nJUST FOLLOWED\nTHEM TWICE!')
    d += d5
    d += flow.Arrow().right().at(d5.E)
    question = flow.Box(w=3.5, h=1.75).anchor('W').label("(THAT WASN'T\nA QUESTION.)")
    d += question
    d += flow.Wire('n', k=-1, arrow='->').at(d5.S).to(question.S)
    
    d += flow.Line().at(good.E).tox(question.S)
    d += flow.Arrow().down()
    drink = flow.Box(w=2.5, h=1.5).label("LET'S GO\nDRINK.")
    d+= drink
    d += flow.Arrow().right().at(drink.E).label('6 DRINKS')
    d += flow.Box(w=3.7, h=2).anchor('W').label('HEY, I SHOULD\nTRY INSTALLING\nFREEBSD!')
    d += flow.Arrow().up(d.unit*.75).at(question.N)
    screw = flow.Box(w=2.5, h=1).anchor('S').label('SCREW IT.')
    d+= screw
    d += flow.Arrow().at(screw.N).toy(drink.S)


