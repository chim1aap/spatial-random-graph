import igraph as ig
import numpy as np
from classes.TriangleFinder import TriangleFinder
from classes.Generator import Generator
import logging, sys, os
from tqdm import tqdm # progressbar
from joblib import Parallel, delayed # Parallel processing.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)  # set to debug for printing debug messages

## Simulation Values


graphSizesToTry = [100, 250, 500, 1000, 2500]  # , 5000, 10000]
gammasToTry = [(0.5 + 2 / 3) / 2, (1.0 + 2 / 3) / 2]
betasToTry = [1]
numberOfRepeats = 10

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

for beta0 in betasToTry:
    for gamma0 in gammasToTry:
        Parallel(n_jobs=10,prefer="threads")
        for n0 in graphSizesToTry:
            blockPrint()
            TriangleFinder.simulate()
