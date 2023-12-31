#Import libraries
import matplotlib.pyplot as plt
import wave
import pyaudio
from keras.models import load_model
import os
import glob
import librosa
import numpy as np


CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

model=load_model("model/model_final.h5")

#Extract features
def extract_features(file_name):
    X, sample_rate = librosa.load(file_name)
    #Short time fourier transformation
    stft = np.abs(librosa.stft(X))
    #Mel Frequency Cepstra coeff (40 vectors)
    mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
    #Chromogram or power spectrum (12 vectors)
    chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    #mel scaled spectogram (128 vectors)
    mel=np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
    # Spectral contrast (7 vectors)
    contrast=np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    #tonal centroid features (6 vectors)
    tonnetz=np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),sr=sample_rate).T, axis=0)
    return mfccs, chroma, mel, contrast, tonnetz

#generating predictions
def speech_to_emotion(filename):
    mfccs, chroma, mel, contrast, tonnetz= extract_features(filename)

    features=np.empty((0,193))
    f=np.hstack([mfccs, chroma, mel, contrast, tonnetz])
    features=np.vstack([features, f])

    his=model.predict(features)

    emotions = ['airplane', 'breathing', 'brushing_teeth', 'can_opening', 'car_horn', 'cat', 'chainsaw',
                'chirping_birds',
                'church_bells', 'clapping', 'clock_alarm', 'clock_tick', 'coughing', 'crackling_fire', 'crickets',
                'dog']
    y_pred=np.argmax(his, axis=1)
    pred_prob=np.max(his,axis=1)
    pred_emo=(emotions[y_pred[0]],pred_prob[0])

    return pred_emo

def record_audio(record=True, file_loc=None):
    if record:
        p=pyaudio.PyAudio()
        stream=p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

        # create matplotlib figure and axes
        fig, ax = plt.subplots(1, figsize=(7, 4))
        # variable for plotting
        x = np.arange(0, 2 * CHUNK, 2)
        # create a line object with random data
        line = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)[0]
        # basic formatting for the axes
        ax.set_title('AUDIO WAVEFORM')
        ax.set_xlabel('Samples')
        ax.set_ylabel('Volume')
        ax.set_xlim(0, 2 * CHUNK)
        plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-1000, 1000])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        # show the plot
        plt.show(block=False)
        wm = plt.get_current_fig_manager()
        wm.window.attributes('-topmost', 1)
        #wm.window.attributes('-topmost', 0)

        frames = []
        for i in range(0, int(RATE / CHUNK * 5)):
            data = stream.read(CHUNK)
            frames.append(data)
            result = np.frombuffer(data, dtype=np.int16)
            line.set_ydata(result)
            fig.canvas.draw()
            fig.canvas.flush_events()
            prog=round((i*100)/(int(RATE/CHUNK*5)))
            plt.suptitle('Progress: '+str(prog)+"%")

        filename = "output.wav"

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        main_dir = r'D:\DL\Speaker Recongition\CODE\output.wav'
        pred = speech_to_emotion(main_dir)
        #fig.suptitle(pred[0])
        fig.texts=[]
        plt.title('AUDIO WAVEFORM\nPredicted Emotion: '+str(pred[0].capitalize()))

        rec=wave.open(filename, 'r')
        return rec
    else:
        if file_loc:
            emo=speech_to_emotion(file_loc)[0]
            #print("The predicted emotion is: "+emo.capitalize())
            return emo.capitalize()


#Trial of the  program
#rec=record_audio(record=True)

#dir=r'C:\Users\YMTS0297\PycharmProjects\Emotion Recognition using speech\Datasets\AudioData'
#s_dir=[d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir,d))]
#fn=glob.glob(os.path.join(dir, s_dir[1],"*.wav"))[35]

#record_audio(record=False, file_loc=fn)

#main_dir = r'C:\Users\YMTS0297\PycharmProjects\Emotion Recognition using speech\output.wav'
#pred=speech_to_emotion(main_dir)
#fig.suptitle(pred[0])


