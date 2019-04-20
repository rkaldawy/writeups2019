import scipy.io.wavfile
from pydub import AudioSegment
import numpy as np
from numpy import fft as fft
import matplotlib.pyplot as plt
from scipy import signal
from PIL import Image, ImageDraw


def constructFFT(rate, audData, period):
    channel1 = audData[int(period[0] * rate):int(period[1] * rate), 0]  # left
    channel2 = audData[int(period[0] * rate):int(period[1] * rate), 1]  # right

    fourier1, fourier2 = fft.fft(channel1), fft.fft(channel2)
    n = len(channel1)
    fourier1 = fourier1[0:int(n / 2)]
    fourier1 = fourier1 / float(n)

    fourier2 = fourier2[0:int(n / 2)]
    fourier2 = fourier2 / float(n)

    return fourier1

def findCorrellation(static, source):
    static_fft = constructFFT(rate, audData, static)
    sample_fft = constructFFT(rate, audData, source)

    result = signal.correlate(static_fft, sample_fft, mode='full')
    result = result.real / 1000000
    return result.max()

def reconstructQRCode():
    output = ""
    staticIdx = 0
    sourceIdx = 3

    while sourceIdx < songLen:
        corellation = findCorrellation((staticIdx, staticIdx + 0.25), (sourceIdx, sourceIdx + 0.25))
        if corellation > 25:
            output += "B"
            sourceIdx += 0.25
            staticIdx += 0.25
        else:
            output += "W"
            sourceIdx += 1
            staticIdx = 0

    #remove the ending song from the construction
    while output[-1] == "W":
        output = output[:-1]

    return output

def drawQRImage(code, path="solution/output.bmp"):
    im = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    for i in range(0, len(code), 25):
        strip = code[i:i + 25]
        ypos = int((i * 20) / 25)
        for j in range(0, len(strip)):
            xpos = j * 20
            val = strip[j]
            print(strip[j], xpos, ypos)
            if val == "B":
                draw.rectangle([(xpos, ypos), (xpos + 20, ypos + 20)], outline=(0, 0, 0, 0), fill=(0, 0, 0, 0))

    im.show()
    im.save("solution/output.bmp")

solution_folder = "solution/"

mp3 = AudioSegment.from_mp3("challenge.mp3")
mp3.export("solution/temp.wav", format="wav")

rate, audData = scipy.io.wavfile.read("solution/temp.wav")
songLen = audData.shape[0]/rate

code = reconstructQRCode()

print(code)

drawQRImage(code)


#print(output)
#print(len(output))

#freqArray = np.arange(0, int(n/2), 1.0) * (rate*1.0/n)

# plt.figure(1)
# plt.subplot(211)
# plt.plot(freqArray/1000, 10*np.log10(fft1), color='#ff7f00', linewidth=0.2)
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Power (dB)')
# plt.subplot(212)
# plt.plot(freqArray, result, color='#ff7f00', linewidth=0.2)
# plt.xlabel('Frequency (kHz)')
# # plt.ylabel('Power (dB)')
# plt.show()

