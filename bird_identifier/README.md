# Bird call classification 

1. Download the sample data from [kaggle](https://www.kaggle.com/c/birdsong-recognition/data) (train\_audio and train.csv) 

(It's about 25 Gb). Place the train\_audio samples in a dir called `data`

ex.

data/
├── aldfly
│   ├── XC134874.mp3
│   ├── XC135454.mp3
│   ├── XC135455.mp3
│   ├── XC135456.mp3
│   ├── XC135457.mp3
│   ├── XC135459.mp3
│   ├── XC135460.mp3
│   ├── XC135883.mp3


2. run make\_bird\_data.py

creates a folder (melspectrogram\_dataset) of .tif files and samples\_df.csv which tie the tif file to the bird (NOTE: each audio file is broken into 5 second sample chunks for the spectrogram, ie there's not a one-to-one correlation to a specific mp3 file for each .tif)

3. run keras\_make\_model.py

takes in samples\_df.csv created from `birds.py` creates weights saved as a .h5 file
