from random import randint
from biosppy.signals import ecg
from filtering_methods import bandpass_filter
from scipy.signal import resample
import numpy as np
from matplotlib.figure import Figure


def sampler_randomizer(data_dict):
  '''
  Takes the raw signals from the 12 leads
  and extracts a sample from them
  '''
  length = (len(data_dict['leads'][0]['samples']))
  frequency = data_dict['fs']

  if frequency == 500:
    if length > 3000:
      n0 = randint(0,(length-3000))
      process = 1

    elif length == 3000 :
      n0 = 0
      process = 2
    else:
      n0 = randint(0, 3000-length)
      process = 3

  if frequency == 1000:
    if length > 6000:
      n0 = randint(0,(length-6000))
      n_end = n0+6000
      process = 4
    elif length == 6000:
      n0 = 0
      process = 5
    else:
      n0 = randint(0, 6000-length)
      process = 6 

  return process, n0

def random_sampling(filtered, process, n0, resample_freq):

    '''
    Given the method from above (sampler_randomizer) it applies the partition 
    in every lead
    '''

    if process == 1:
      signal = resample(filtered[n0:n0+3000],resample_freq)
      return signal 

    elif process == 2 :
      signal = resample(filtered,resample_freq)
      return signal

    elif process == 3:
        background = np.zeros(3000)
        counter = 0

        for x in range(n0, n0+len(filtered)):
          background[x] = filtered[counter]
          counter += 1
        
        signal = resample(background, resample_freq)
        return signal

    elif process == 4:
      signal = resample(filtered[n0:n0+6000],resample_freq)
      return signal 

    elif process == 5:
      signal = resample(filtered,resample_freq)
      return signal

    else:
      background = np.zeros(6000)
      counter = 0

      for x in range(n0, n0+len(filtered)):
        background[x] = filtered[counter]
        counter += 1 
      signal = resample(background, resample_freq)
      
      return signal

def filter_single_ECG(data_dict):
  '''
  Filters each signal by correcting the baseline and applying a bandpass filter
  '''
  process, n0 = sampler_randomizer(data_dict)
  for x in range(12):
    signal = ecg.ecg(signal=data_dict['leads'][x]['samples'], sampling_rate=data_dict['fs'], show=False)['filtered']
    filtered = bandpass_filter(signal, 0.001, 15, data_dict['fs'],1)
    filtered = random_sampling(filtered, process, n0, 3000)
    data_dict['leads'][x]['samples'] = filtered

  return data_dict

def y_range_ecg(data_dict):
  '''
  This method extracts the total range of the ECG strips
  E.g. range(I+V1)+range(II+V2)+range(III+V3)
  '''
  range_list=[]
  for x in range(6):
    y = x+6
    signal = data_dict['leads'][x]['samples']
    signal2 = data_dict['leads'][y]['samples']
    strip = np.concatenate((signal,signal2))
    rango = max(strip) - min(strip)

    range_list.append(rango)

  return int(sum(range_list)), range_list

def create_grid(ecg_duration, freq, total_range):
    '''
    Creates a grid based in the signal's frequency
    it has to be created as a Figure object otherwise 
    Flask will not allow it
    '''

    fig = Figure(figsize=(20,15), dpi=200)
    ax = fig.add_subplot(1, 1, 1)
    
    
    ax.set_xticks(np.arange(-300, (ecg_duration*freq*2)+300, freq*0.2))
    ax.set_yticks(np.arange(-1000, total_range+1000, freq*0.2))

    # And a corresponding grid
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.grid(which='both', axis='both')
    # Or if you want different settings for the grids:
    ax.set_aspect("equal")

    return fig, ax

def get_ecg_duration(signal, freq):
    '''
    Gets the duration of the complete ECG signal
    '''
    ecg_duration = len(signal)/freq
    return ecg_duration

def oneshot_plot_12ECG(data_dict):
    '''
    Final method that gathers all the helper methods from above to plot the final ecg strip
    '''

    leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    total_range, range_list = y_range_ecg(data_dict)
    print(range_list)
    signal = data_dict['leads'][0]['samples']
    freq = data_dict['fs']
    duration = get_ecg_duration(signal, freq)
    print(duration)
    fig, ax = create_grid(duration, freq, total_range)
    counter = range_list[0]
    lead_delimiter = ax.axvline(len(signal), color='g', linestyle='--')

    for x in range(6): 
        y = x+6
        signal = ecg.ecg(signal=data_dict['leads'][x]['samples'], sampling_rate=freq, show=False)['filtered']
        signal2 = ecg.ecg(signal=data_dict['leads'][y]['samples'], sampling_rate=freq, show=False)['filtered']
        strip = np.concatenate((signal,signal2))

        if x == 0:
            displacement = int(total_range) - (counter)
        elif x == 5:
            displacement = int(total_range) - (counter)
        else:
            displacement = int(total_range) - (counter)

        ax.text(0,displacement+200,leads[x])
        ax.text(duration*freq, displacement+200, leads[y])


        counter += range_list[x]
        x_axis = range(len(strip))
        y_axis = np.add(strip,displacement)

        lead_delimiter
        ax.plot(x_axis,y_axis)

    #try:
    fig.savefig('./preprint_ECG/ECG_for_NN.png')
    #    print('Image successfully saved')
    #except:
    #    print('Error saving the image')

    return


def upload_image_print(data_dict):
    '''
    Final method that will be called in the parent class 
    to get the image uploaded in the preprint_ECG folder
    '''

    signal_plot = filter_single_ECG(data_dict)
    oneshot_plot_12ECG(signal_plot)

    return 