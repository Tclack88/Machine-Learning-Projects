import numpy as np
import pandas as pd
import wave
from scipy.io import wavfile
import os
import librosa
from librosa.feature import melspectrogram
import warnings
from sklearn.utils import shuffle
from sklearn.utils import class_weight
from PIL import Image
from uuid import uuid4
import sklearn
from tqdm import tqdm

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout, Activation
from tensorflow.keras.layers import BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Flatten, Dropout, Activation, LSTM, SimpleRNN, Conv1D, Input, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


train_df = pd.read_csv('train.csv')
train_df = train_df[train_df.rating >= 4]

birds_count = {}
for bird_species, count in zip(train_df.ebird_code.unique(), train_df.groupby("ebird_code")["ebird_code"].count().values):
    birds_count[bird_species] = count
most_represented_birds = [key for key,value in birds_count.items() if value == 100]

train_df = train_df.query("ebird_code in @most_represented_birds")

birds_to_recognise = sorted(shuffle(most_represented_birds)[:20])
train_df = shuffle(train_df)

print(len(train_df))

def get_sample(filename, bird, output_folder):
    wave_data, wave_rate = librosa.load(filename)
    wave_data, _ = librosa.effects.trim(wave_data)
    #only take 5s samples and add them to the dataframe
    song_sample = []
    sample_length = 5*wave_rate
    samples_from_file = []
    #The variable below is chosen mainly to create a 216x216 image
    N_mels=216
    for idx in range(0,len(wave_data),sample_length):
        song_sample = wave_data[idx:idx+sample_length]
        if len(song_sample)>=sample_length:
            mel = melspectrogram(song_sample, n_mels=N_mels)
            db = librosa.power_to_db(mel)
            normalised_db = sklearn.preprocessing.minmax_scale(db)
            filename = str(uuid4())+".tif"
            db_array = (np.asarray(normalised_db)*255).astype(np.uint8)
            db_image =  Image.fromarray(np.array([db_array, db_array, db_array]).T)
            db_image.save(f"{output_folder}{filename}")

            samples_from_file.append({"song_sample":f"{output_folder}{filename}",
                                            "bird":bird})
    return samples_from_file

warnings.filterwarnings("ignore")
samples_df = pd.DataFrame(columns=["song_sample","bird"])

sample_limit = 1000
sample_list = []


output_folder = "./melspectrogram_dataset/"
os.mkdir(output_folder)
with tqdm(total=sample_limit) as pbar:
    for idx, row in train_df[:sample_limit].iterrows():
        pbar.update(1)
        try:
            audio_file_path = f"./data/{row.ebird_code}"
            #print(f'working on {audio_file_path}')
            
            if row.ebird_code in birds_to_recognise:
                sample_list += get_sample(f'{audio_file_path}/{row.filename}', row.ebird_code, output_folder)
            else:
                sample_list += get_sample(f'{audio_file_path}/{row.filename}', "nocall", output_folder)
        except:
            raise
            print(f"{audio_file_path} is corrupted")
            
        #print(sample_list)
samples_df = pd.DataFrame(sample_list)
samples_df.to_csv('samples_df.csv',index=False)
print('DONE')
