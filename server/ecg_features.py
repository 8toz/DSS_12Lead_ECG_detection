from statistics import mean
from biosppy.signals import ecg
import neurokit2 as nk
import numpy as np

'''
To extract ECG features we are going to use biosppy and neurokit2 
they will be of great utility for filtering and signal analysis purposes
'''

def get_averaged_heartbeat(signal, frequency):
  '''
  With this method we can get the averaged bpm from the patient 
  with the desired decimals 
  '''
  out = ecg.ecg(signal=signal, sampling_rate=frequency, show=False)
  
  return round(mean(out['heart_rate']),2)

def get_R_peaks(signal, frequency):
  '''
  This method detects the R peaks in the signal
  '''
  _, rpeaks = nk.ecg_peaks(signal, frequency)
  return rpeaks

def get_other_peaks(signal, frequency):
  '''
  Based on the Rpeaks, this method extracts if possible the remaining peaks
  '''
  rpeaks = get_R_peaks(signal, frequency)
  _, waves_peak = nk.ecg_delineate(signal, rpeaks, sampling_rate=500)
  return waves_peak['ECG_T_Peaks'], waves_peak['ECG_P_Peaks']

def distance_between_same_peaks(list_of_samples, freq):
  '''
  measures the distance between same peaks RR, TT, PP...
  '''
  time = np.multiply(np.divide(np.array(list_of_samples),freq),1000)

  shifted = np.roll(time, 1)
  result = np.subtract(time, shifted)
  result = np.delete(result, 0)
  mean_RR = np.mean(result)

  return result, mean_RR

def transform_to_time(signal, freq):
  '''
  method that converts the number of samples into the time axis
  '''
  time_list = np.multiply(np.divide(np.array(signal),freq),1000)
  return time_list


def dist_betweenWaves(wave1, wave2):
  '''
  method that measures the distance within two waves and
  returns the average and a list with all the values in case
  of an error in the calculation
  '''
  if len(wave1) != len(wave2):
    print(len(wave1),len(wave2))
    print('The number of peaks must match')

  wave1,  wave2 = np.array(wave1), np.array(wave2)
  result = np.subtract(wave2, wave1)
  mean_W1_W2 = np.mean(result)

  return result, mean_W1_W2


def get_ECG_features(data_dict):

  '''
  Final method that wraps up all the methods described above to gather the information
  which will be the one to be finally used in the frontend
  '''

  # We extract the signal that we desire
  signal = data_dict['leads'][1]['samples']
  freq = data_dict['fs']
  signal = ecg.ecg(signal=signal, sampling_rate=data_dict['fs'], show=False)['filtered']
  # Extract the information of the R peaks
  R_peaks = get_R_peaks(signal, freq)['ECG_R_Peaks']
  t_R_peaks, mean_RR = distance_between_same_peaks(R_peaks, freq)
  # Extract the information of the rest of the peaks
  T_peaks, P_peaks = get_other_peaks(signal, freq)
  # T wave
  t_T_peaks, mean_TT = distance_between_same_peaks(T_peaks, freq)
  # P wave
  t_P_peaks, mean_PP = distance_between_same_peaks(P_peaks, freq)
  # PR interval
  t_PR_interval, mean_PR = dist_betweenWaves(P_peaks, R_peaks)
  #RT interval
  t_RT_interval, mean_RT = dist_betweenWaves(R_peaks, T_peaks)

  # Upload the data into a dictionary
  ecg_features = {}
  ecg_features['average_RR_distance'] = int(np.round(mean_RR,0).astype(int))
  ecg_features['RR_distance'] = str(t_R_peaks.astype(int))
  ecg_features['average_TT_distance'] = int(np.round(mean_TT,0).astype(int))
  ecg_features['TT_distance'] = str(t_T_peaks.astype(int))
  ecg_features['average_PP_distance'] = int(np.round(mean_PP,0).astype(int))
  ecg_features['PP_distance'] = str(t_P_peaks.astype(int))
  ecg_features['average_PR_distance'] = int(np.round(mean_PR,0).astype(int))
  ecg_features['PR_distance'] = str(t_PR_interval.astype(int))
  ecg_features['average_RT_distance'] = int(np.round(mean_RT,0).astype(int))
  ecg_features['RT_distance'] = str(t_RT_interval.astype(int))
  ecg_features['average_bpm'] = int(np.round(get_averaged_heartbeat(signal, freq),0).astype(int))

  return ecg_features