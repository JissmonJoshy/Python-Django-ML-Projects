from pathlib import Path
from django.core.files import File
from .models import EncodedText, EncodedTextDec
from PIL import Image


def genData(data):
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                imdata.__next__()[:3] +
                imdata.__next__()[:3]]
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1
        # Eigh^th pixel of every set tells
        # whether to stop or read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def enc_fun(id, text_area):
    data = EncodedText.objects.get(id=id)
    myimg = Image.open(data.inputImage.path).convert("RGB")  # Ensure RGB mode
    newimg = myimg.copy()

    encode_enc(newimg, text_area)

    output_path = Path("media") / f"encoded_image_{id}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure media folder exists
    newimg.save(output_path)

    with open(output_path, 'rb') as f:
        django_file = File(f)
        data.encodeImage.save(output_path.name, django_file, save=True)
        data.save()

def decode(id):
    try:
        dataEn = EncodedTextDec.objects.get(id=id)
        image = Image.open(dataEn.file.path).convert("RGB")
        imgdata = iter(image.getdata())

        data = ''
        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                                   imgdata.__next__()[:3] +
                                   imgdata.__next__()[:3]]

            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            char = chr(int(binstr, 2))

            # safety check: only allow readable ASCII
            if not (32 <= ord(char) <= 126):  
                return "Invalid format"

            data += char

            if pixels[-1] % 2 != 0:  # message end marker
                break

        return data.strip()

    except Exception:
        return "Invalid format"
