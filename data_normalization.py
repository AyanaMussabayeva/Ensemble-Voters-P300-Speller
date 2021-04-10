#script for multi-channel EEG data cleaning and normalization 

import data_filtering #file with lowpass filter
import numpy as np


def prepare_data(file):
  allX = []
  allY = []
  allT = []
  allF = []
  raw_data = loadmat(file)
  useful_data = raw_data['data'].copy()
  X = useful_data['X']
  Y = useful_data['y']
  T = useful_data['trial']
  F = useful_data['flash']
  # X_mean = np.mean(X, axis=1)
  X_filtered = data_filtering.butter_lowpass_filter(X, cutoff, fs, order)
  
  return X_filtered, Y, T, F


def normalized(vec):
  norm_vec = (vec - vec.min(axis=1, keepdims=True))/vec.ptp(axis=1, keepdims=True)
  return norm_vec

def clean_data(X, Y, flash):
  
  X_samples = np.array([np.array(X[i[0]:i[0]+351]) for i in flash] )
  column    = [i[2] for i in flash]
  label     = [i[3] - 1 for i in flash]
  
  LIMIT = 4080 #the last trial is incomplete
  X_selected = np.array(X_samples[:LIMIT])
  col_selected = np.array(column[:LIMIT])
  label_selected = np.array(label[:LIMIT])

  y = np.array(to_categorical(label_selected))

  false_idx = [k for k, i in enumerate(y) if i[0] == 1]
  true_idx  = [k for k, i in enumerate(y) if i[0] == 0]

  falseX = X_selected[false_idx]
  falsey = y[false_idx]

  trueX  = X_selected[true_idx]  
  truey  = y[true_idx]
  # proportional data to avoid greedy cost funtion

  proportionalX = falseX[:int(len(trueX))]
  proportionaly = falsey[:int(len(truey))]

  finalX = np.concatenate((trueX, proportionalX))
  finaly = np.concatenate((truey, proportionaly))

  X_timeseries = np.vstack(finalX)
  X_letters = X_timeseries.reshape(34,40,351,8)
  y_letters = finaly.reshape(34,40,2)
  cleaned_X = np.vstack(X_letters)
  cleaned_Y = np.vstack(y_letters)
  
  return cleaned_X, cleaned_Y