from __future__ import print_function
import numpy as np

np.random.seed(100)  

from sklearn import metrics, preprocessing
import pandas as pd
from matplotlib import pyplot as plt

# define sine wave 
def load_data():
    sinewave = np.sin(np.arange(800)/20.0) 
    return sinewave
    
sinewave  = load_data()