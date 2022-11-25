import sys  # nopep8
sys.path.insert(0, '/home/decode_nfiq/build')  # nopep8
from finger_id import *  # nopep8

import json
import numpy as np
from base64 import b64decode, b64encode
from PIL import Image
import wsq

from io import BytesIO

def open_image(src: str) -> np.ndarray:
    img = Image.open(src)
    return np.asarray(img).copy()

def encode_template(template:str) -> str:
    template = json.loads(template)
    encoded_string = f"w{template['width']}h{template['height']}m"
    for minutia in template['minutiae']:
        encoded_string += f"x{minutia['x']}y{minutia['y']}d{minutia['direction']}t{'e' if minutia['type']=='ending' else 'b'}"
    return encoded_string

def trunc_template(template: str) -> str:
    template = json.loads(template)
    template['minutiae'] = template['minutiae'][:120]
    return json.dumps(template)

def trunc_template2(template: str) -> str:
    template = json.loads(template)
    template['minutiae'] = template['minutiae'][:-120]
    return json.dumps(template)

def loadFileBase64( fn ):
	data = open( fn, "rb").read()
	return b64encode(data)

def crop_roi(filename):
    img_base64 = loadFileBase64(filename)
    img_np = np.asarray(Image.open(filename))

    roi = json.loads(crop_roi_wsq(img_base64))
    x = roi['x']
    y = roi['y']
    width = roi['width']
    height = roi['height']

    cropped_img = img_np[y:y+height,x:x+width]
    Image.fromarray(cropped_img).save(filename.replace('wsq','png'))

    return cropped_img

# import wsq
# img = Image.open('DB1_B/101_3.tif')
# img.save('101_3.wsq')
# img = Image.open('DB1_B/101_4.tif')
# img.save('101_4.wsq')

# cropped1 = crop_roi('101_3.wsq')
# cropped2 = crop_roi('101_4.wsq')
# enhanced1 = enhance_function(img1, filter='CARTOON')

# for filter in ['CLAHE','CARTOON','NORMALIZATION','LCLAHE','WIENER']:
#     enhanced = enhance_function(cropped1,filter=filter)
#     Image.fromarray(enhanced).save(f'enhanced_101_3_{filter}.png')


# t1 = fingerjet_numpy(cropped1, qualityThreshold=0, event_id='1', maxMinutia=100)

# img2 = loadFileBase64('101_4.wsq')
# t2 = fingerjet_numpy(cropped2, qualityThreshold=0, event_id='1', maxMinutia=100)

img1 = open_image('bin.png')
img2 = open_image('101_3.png')

t1 = fingerjet_numpy(np.asarray(img1), qualityThreshold=0, event_id='1')
t2 = fingerjet_numpy(np.asarray(img2), qualityThreshold=0, event_id='1')

print(len(json.loads(t1)['minutiae']))
print(len(json.loads(t2)['minutiae']))

print(f"t1xt1={m3gl_match_json(t1,t1)}")
print(f"t2xt2={m3gl_match_json(t2,t2)}")
print(f"t1xt2={m3gl_match_json(t1,t2)}")