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
import seaborn as sns
import re as re
import io as io
# %load_ext memory_profiler
from datetime import datetime

os.system("pip install pyflowchart")

from pyflowchart import *

# +
st = StartNode('a_pyflow_test')
op = OperationNode('do something')
cond = ConditionNode('Yes or No?')
io = InputOutputNode(InputOutputNode.OUTPUT, 'something...')
sub = SubroutineNode('A Subroutine')
e = EndNode('a_pyflow_test')

st.connect(op)
op.connect(cond)
cond.connect_yes(io)
cond.connect_no(sub)
sub.connect(op, "right")  # sub->op line starts from the right of sub
io.connect(e)

fc = Flowchart(st)
rint(fc.flowchart())
# -

fc = Flowchart(st)
print(fc.flowchart())

# +

help(fc)
# -

fc = Flowchart(st)
print(fc)

fc = Flowchart(st)
print(fc.output_html())

output_html('output.html', 'a_pyflow_test', fc.flowchart())



