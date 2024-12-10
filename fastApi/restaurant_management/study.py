import pandas as pd
import numpy as np

from scipy import loadtxt

from sklearn.datasets import load_iris

#data = pd.read_csv('ml.csv')
#data = np.genfromtxt('ml.csv', delimiter=',')
#data = loadtxt('ml.csv',delimeter=',')
data = load_iris().data