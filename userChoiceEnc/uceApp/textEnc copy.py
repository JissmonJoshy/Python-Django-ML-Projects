
from pathlib import Path
from django.core.files import File
from .models import EncodedText
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
        pix = [value for value in imdata.__next__()[:3] +
                imdata.__next__()[:3] +
                imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

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

def enc_fun(id,text_area):
    data = EncodedText.objects.get(id=id)
    myimg = Image.open(data.inputImage.path)
    newimg = myimg.copy()
    encode_enc(newimg, text_area)

    proj = Path.cwd() / "media"
    output_file = proj / "encoded_image.png"  # Adjust the name/format as needed
    newimg.save(output_file)

    with open(output_file, 'rb') as f:  # Open the image in binary mode
        django_file = File(f)
        data.encodeImage.save(output_file.name, django_file)
        data.save()

def decode(image):
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                    imgdata.__next__()[:3] +
                    imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data