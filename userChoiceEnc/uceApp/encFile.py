import os
import numpy as np
from PIL import Image
from pydub import AudioSegment
from django.conf import settings
from .models import DataStorage
import time

def main(dataId, audiofile):
    data = DataStorage.objects.get(id=dataId)
    imagefile = os.path.join(settings.MEDIA_ROOT, str(data.orgImage))

    # Load audio and ensure proper format
    sound = AudioSegment.from_file(audiofile)
    sound = sound.set_frame_rate(44100).set_channels(2).set_sample_width(2)
    temp_wav = os.path.join(settings.MEDIA_ROOT, "fixed.wav")
    sound.export(temp_wav, format="wav")

    # Read audio
    import scipy.io.wavfile as wave
    samplingRate, audioChannels = wave.read(temp_wav)
    if len(audioChannels.shape) == 1:
        audioChannels = np.column_stack((audioChannels, audioChannels))

    left, right = audioChannels[:, 0], audioChannels[:, 1]
    max_val = np.max(np.abs(audioChannels))  # store for normalization

    # Normalize to 0-255 for storing in image
    left_norm = ((left + max_val) / (2 * max_val) * 255).astype(np.uint8)
    right_norm = ((right + max_val) / (2 * max_val) * 255).astype(np.uint8)

    # Load image and resize
    im = Image.open(imagefile).convert("RGB")
    width, height = im.size
    im = im.resize((max(width, 512), max(height, 512)))
    pixels = im.load()

    total_samples = len(left_norm)
    idx = 0

    # Encode audio into image
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if idx >= total_samples:
                break
            r, g, b = pixels[i, j]
            pixels[i, j] = (left_norm[idx], right_norm[idx], b)
            idx += 1
        if idx >= total_samples:
            break

    # Save processed image
    timestamp = int(time.time())
    output_filename = f"{timestamp}.png"
    output_path = os.path.join(settings.MEDIA_ROOT, "processed_images", output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path)

    # Save to database
    data.file = "processed_images/" + output_filename
    data.save()

    return data.id
