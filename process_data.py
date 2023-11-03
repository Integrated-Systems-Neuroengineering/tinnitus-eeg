import mne
import matplotlib.pyplot as plt
import pyxdf
import numpy as np
from glob import glob
import os

SUBJECT = 'P001'
DATA_PATH = f'./data/'
XDF_FILES = glob(os.path.join(DATA_PATH + f'/sub-{SUBJECT}/*/*/*.xdf'))
XDF_FILES = sorted(XDF_FILES) # to sort by run#

ALL_EEG = []

# These are unused for the static cars paradigm:
ALL_Z = []
events = []

# Load each XDF file for a given subject
for XDF in XDF_FILES:
    streams, header = pyxdf.load_xdf(XDF)

    # Get the first time stamp across all streams (read from time_stamps)
    first_timestamps = []

    for s in streams:  # loop through remaining streams
        s_name = s['info']['name'][0]
        if 'Tinnitus' not in s_name:
            print(s_name)
            t0 = s['time_stamps'][0]
            print(t0, '\t', s_name)
            first_timestamps.append(t0)

            first_timestamp = min(first_timestamps)
            print(first_timestamp, '\t', '<== earliest')

            # Identify EEG data and impedance streams
    for s in streams:
        s_name = s['info']['name'][0]

        if 'Tinnitus' not in s_name:
            s_type = s['info']['type'][0]
            print(f'Stream Name: {s_name}\tType: {s_type}')

            # Get the EEG data stream for CGX
            if ('CGX' in s_name) and (s_type == 'EEG'):
                eeg_data = s['time_series']
                eeg_t = s['time_stamps'] - first_timestamp  # offset first time stamp to t=0
                eeg_ch_names = [ch['label'][0] for ch in s['info']['desc'][0]['channels'][0]['channel']]
                eeg_ch_units = [ch['unit'][0] for ch in s['info']['desc'][0]['channels'][0]['channel']]
                eeg_sfreq = s['info']['effective_srate']
                # print(f'Channels: {eeg_ch_names}')
                # print(f'Unit: {eeg_ch_units}')
                print(f'Eff. Sampling Rate: {eeg_sfreq} Hz')
                print(eeg_data.shape)

                # Rescale EEG channels to V for importing into MNE
                if 'microvolts' in eeg_ch_units:
                    eeg_data[:, :30] /= 1e6

                ALL_EEG.append(eeg_data)

            # Get the impedance data stream for CGX
            elif ('CGX' in s_name) and (s_type == 'Impeadance'):  # typo in the stream name?
                z_data = s['time_series']
                z_t = s['time_stamps'] - first_timestamp
                z_ch_names = [ch['label'][0] for ch in s['info']['desc'][0]['channels'][0]['channel']]
                z_ch_units = [ch['unit'][0] for ch in s['info']['desc'][0]['channels'][0]['channel']]
                z_sfreq = s['info']['effective_srate']
                # print(f'Channels: {z_ch_names}')
                # print(f'Unit: {z_ch_units}')
                print(f'Eff. Sampling Rate: {z_sfreq} Hz')

                ALL_Z.append(z_data)
    print(streams)