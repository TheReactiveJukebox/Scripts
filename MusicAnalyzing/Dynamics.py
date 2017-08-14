#!/usr/bin/env python3
import matplotlib.pyplot as plt  # pip3 install matplotlib
import librosa
import librosa.display as ld
import numpy as np


def dynamics(y, sr):
    # implements mirlowenergy feature
    # https://www.jyu.fi/hytk/fi/laitokset/mutku/en/research/materials/mirtoolbox/MIRtoolbox1.6.1guide  page 83,84
    assert sr == 44100, "Samplerate is not 44.1khz, Change frame values to match the specified times"

    # 512 samples = ~11.6ms
    # 2018 samples =  ~46.4ms
    frame_length = 2048
    hop_length = 512
    boxtime = 2  # in seconds

    rms = librosa.feature.rmse(y=y, frame_length=frame_length, hop_length=hop_length, center=True)[0]
    # testplot(rms,"RMS")

    boxlength = round(boxtime / (hop_length / sr))
    rms = np.convolve(rms, np.ones((boxlength,)) / boxlength, mode='valid')
    rmsmean = np.mean(rms)
    print("Mean RMS=" + str(rmsmean))
    # testplot(rms,"RMS Filtered")

    belowmeancount = 0
    for x in rms:
        if x < rmsmean:
            belowmeancount += 1

    lowenergy = belowmeancount / np.shape(rms)[0]
    print(str(belowmeancount) + " below mean out of " + str(np.shape(rms)[0]) + " samples, lowenergy=" + str(lowenergy))

    return lowenergy


def testplot(data, title):
    plt.figure()
    # plt.semilogy(rms.T, label='RMS Energy')
    plt.title(title)
    # plt.plot(data.T, label=title)
    plt.plot(data.T)
    plt.xticks([])
    plt.xlim([0, data.shape[-1]])
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    # y, sr = librosa.load(librosa.util.example_audio_file())

    # .399
    y, sr = librosa.load(
        "/media/fisch/HDD/Uni/PG/Musik PG/0/1/93c5854e8115b64a82817b2b3013d97061a07e4aa8d2ad2fe6081bbeb64fc8.mp3",
        sr=44100)

    # .6
    # y, sr = librosa.load("/media/fisch/HDD/Uni/PG/Musik PG/0/1/93c5854e8115b64a82817b2b3013d97061a07e4aa8d2ad2fe6081bbeb64fc8.mp3",sr=44100)

    # .42
    # y, sr = librosa.load("/media/fisch/HDD/Uni/PG/Musik PG/0/1/f97dcffdbdf7e52efae73792ad63a335d9bbfcae66e5718aac8eee21485a0d.mp3",sr=44100)

    # .27  kraftklub - zwei dosen sprite
    # y, sr = librosa.load("/media/fisch/HDD/Uni/PG/Musik PG/0/8/ee073fabed3393543b1ce23f3e298ea8286eb2030d8e63083e76f3a265cf6a.mp3",sr=44100)

    # minimum 93c6424646f1b1b1281fc412ee52fadf71aa96aa2706fe5308b7a3e64b73b2d5  0.1350618028
    # y, sr = librosa.load("/media/fisch/HDD/Uni/PG/Musik PG/9/3/c6424646f1b1b1281fc412ee52fadf71aa96aa2706fe5308b7a3e64b73b2d5.mp3",sr=44100)
    # maximum 140a2592c3bdb5fd0458d845355cf3803d1a68fe5428ae8d2d15d6f955d479b7   0.7276209304
    # y, sr = librosa.load("/media/fisch/HDD/Uni/PG/Musik PG/1/4/0a2592c3bdb5fd0458d845355cf3803d1a68fe5428ae8d2d15d6f955d479b7.mp3",sr=44100)



    dynamics(y, sr)
