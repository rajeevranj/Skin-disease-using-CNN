# #Import libraries
# import glob
# import os
# import librosa
# import numpy as np
# import tensorflow as tf
# from keras.models import Sequential
# from keras.layers import Dense, Activation
# from keras.layers import Dropout
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix, accuracy_score
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
#
#
# CSV_FILE_PATH = "D:\DL\Speaker Recongition\CODE\Vox50.csv"  # path of csv file
# DATA_PATH = r"D:\DL\Speaker Recongition\CODE\VOX/" # path to folder containing audio files
#
# df = pd.read_csv(CSV_FILE_PATH)
# df.head()
# print("shape of df: ", df.shape)
#
# df=df.drop(["fold","esc10","src_file","take"],axis=1)
#
# classes = df['category'].unique()
# print("Classes are: ",classes)
# print("# of Classes are: ",classes.shape[0])
#
# X = []
# y = []
# from tqdm import tqdm
#
# for data in tqdm(df.iterrows(),  desc='Progress'):
#     sig , sr = librosa.load(DATA_PATH+data[1][0])
#     mfcc_ = librosa.feature.mfcc(sig , sr=sr, n_mfcc=40)
#     X.append(mfcc_)
#     y.append(data[1][1])
#
# X = np.array(X)
# y = np.array(y)
#
# X.shape
#
# import tensorflow as tf
# y = tf.keras.utils.to_categorical(y , num_classes=50)
# X = X.reshape(X.shape[0], X.shape[1], X.shape[2], 1)
#
# print("X Shape is: ", X.shape)
# print("y Shape is: ", y.shape)
#
# from numpy import save
# X= np.asarray(X)
# save("X.npy",X)
#
# y= np.asarray(y)
# save("y.npy",y)
#
# print(X.shape)
# print(y.shape)
#
#
