import os
import pickle
DEVICE_DATA_FILE = 'device_data.pkl'
def save_device_data(device_data, snr):
    dict = None
    if os.path.isfile(DEVICE_DATA_FILE):
        with open(DEVICE_DATA_FILE, 'rb') as file:
            dict = pickle.load(file)
            dict[snr] = device_data
    else:
        dict = {snr: device_data}
    with open(DEVICE_DATA_FILE, 'wb') as file:
        pickle.dump(dict, file)

def get_device_data(snr):
    if os.path.isfile(DEVICE_DATA_FILE):
        with open(DEVICE_DATA_FILE, 'rb') as file:
            dict = pickle.load(file)
            if snr in dict:
                return dict[snr]
    return None