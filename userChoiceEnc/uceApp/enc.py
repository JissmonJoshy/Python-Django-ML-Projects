from PIL import Image
import scipy.io.wavfile as wave
import numpy
from pydub import AudioSegment

audiofile = 'sampleTest.wav'
imagefile = '123.jpg'  # Specify the input image

# Convert audio to proper WAV format
sound = AudioSegment.from_file(audiofile)
sound = sound.set_frame_rate(44100).set_channels(2).set_sample_width(2)
sound.export("fixed.wav", format="wav")

audiofile = 'fixed.wav'
samplingRate, audioChannels = wave.read(audiofile)

left = list(audioChannels[:, 0])
right = list(audioChannels[:, 1])

mleft = max(map(abs, left))
mright = max(map(abs, right))

def divide(a, max_value):
    return (a / float(max_value)) * 255

left = list(map(lambda a: divide(a, mleft), left))
right = list(map(lambda a: divide(a, mright), right))

# Load existing image instead of creating a new one
im = Image.open(imagefile)
im = im.convert("RGB")  # Ensure it's in RGB mode
im = im.resize((670, 670))  # Resize to match expected dimensions

ai = 0
done = False
pixels = im.load()  # Load pixel data for modification

for i in range(670):
    if done:
        break
    for j in range(670):
        if ai >= len(left):
            done = True
            break
        r, g, b = pixels[i, j]  # Get original pixel color
        r = int(left[ai])  # Modify red channel with audio data
        g = int(right[ai])  # Modify green channel with audio data
        pixels[i, j] = (r, g, b)  # Update pixel
        ai += 1

im.save('output_image.jpg')  # Save modified image
