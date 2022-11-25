import sys  # nopep8
sys.path.insert(0, '/home/decode_nfiq/build')  # nopep8
from finger_id import *  # nopep8

import json
import numpy as np
from base64 import b64decode, b64encode
from PIL import Image

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

img = loadFileBase64('teste.wsq')
img1 = open_image('NIST4_F0001_01.bmp')
enhanced1 = enhance_function(img1, filter='CARTOON')
t1 = decode_extract_wsq(img, qualityThreshold=0, event_id='1', maxMinutia=60)

img2 = open_image('FVC2002DB2A_1_1.bmp')
enhanced2 = enhance_function(img2, filter='CARTOON')
t2 = decode_extract_wsq(img.decode('utf-8'), qualityThreshold=0, event_id='1', maxMinutia=120)

print(len(t1),len(t2))


print(f"t1xt1={m3gl_match_json(t1,t1)}")
print(f"t2xt2={m3gl_match_json(t2,t2)}")
print(f"t1xt2={m3gl_match_json(t1,t2)}")