import os
from glob import glob

for fn in glob('text/p*'):
    new_fn = fn+'.txt'
    os.rename(fn,new_fn)
