import pickle
import sys  # nopep8
sys.path.insert(0, '/home/decode_nfiq/build')  # nopep8
from finger_id import *  # nopep8

from typing import Union, Sequence, Tuple
from datetime import datetime
import cv2
import json
import numpy as np
from base64 import b64decode, b64encode
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import segno
import math

def open_image(src: str) -> np.ndarray:
    img = Image.open(src)
    return np.asarray(img).copy()

# TODO - Atualizar pra python3.7 pra poder utilizar @dataclass

# @dataclass


class Minutia:
    x: int
    y: int
    direction: float
    type: str

    def __init__(self, x, y, direction, type) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.type = type

    def __repr__(self) -> str:
        return f"Minutia(x={self.x}, y={self.y}, direction={self.direction}, type={self.type})"

    def __eq__(self, other):
        if not isinstance(other, Minutia):
            return 'NotImplemented'  # Potencial erro

        return self.x == other.x and self.y == other.y and self.direction == other.direction and self.type == other.type

    def as_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "type": self.type
        }


# @dataclass


class Template:
    width: int
    height: int
    minutiae: Sequence[Minutia]

    def __init__(self, width: int, height: int, minutiae: Sequence[Minutia]) -> None:
        self.width = width
        self.height = height
        self.minutiae = minutiae

    def __repr__(self) -> str:
        return f"Template(width={self.width}, height={self.height}, minutiae={[minutia.__repr__() for minutia in self.minutiae]})"

    def __iter__(self):
        yield from self.minutiae

    def __eq__(self, other):
        if not isinstance(other, Template):
            return 'NotImplemented'  # Potencial erro
        return self.width == other.width and self.height == other.height and self.minutiae == other.minutiae

    def as_json(self):
        return {
            "width": self.width,
            "height": self.height,
            "minutiae": [minutia.as_json() for minutia in self.minutiae]
        }


class QRCodeData:
    name: str
    expiration: datetime.timestamp
    template: Template


class TBD:
    def __init__(self, public_key:str, private_key:str) -> None:
        self.public_key = RSA.import_key(open(public_key).read())        
        self.private_key = RSA.import_key(open(private_key).read())        

    def isBase64(string_to_check: str) -> bool:
        try:
            if isinstance(string_to_check, str):
                string_to_check_as_bytes = bytes(string_to_check, 'ascii')
            elif isinstance(string_to_check, bytes):
                string_to_check_as_bytes = string_to_check
            else:
                raise ValueError(
                    "O formato do argumento deve ser string ou bytes!")
            return b64encode(b64decode(string_to_check_as_bytes)) == string_to_check_as_bytes
        except Exception:
            return False

    def read_image(source: str) -> np.ndarray:
        if source.endswith('.wsq'):
            image = read_wsq_file(source)
        elif TBD.isBase64(source):
            image = read_wsq_base64(source)
        else:
            image = open_image(source)

        return image

    def extract_minutiae(self, source: str, extractor: str, filter: str = '') -> Template:
        img = open_image(source)
        enhanced = enhance_function(img, filter=filter)
        template_as_json = extractor(enhanced, qualityThreshold=0)
        template_as_dict = json.loads(template_as_json)
        minutiae = template_as_dict['minutiae']
        template = Template(width=template_as_dict['width'], height=template_as_dict['height'], minutiae=[Minutia(
            minutia['x'], minutia['y'], minutia['direction'], minutia['type']) for minutia in minutiae])
        return template

    def match_minutiae(self, matcher, reference_template: bytes, input_template: bytes) -> bool:
        
        score = matcher(reference_template, input_template)
        is_valid = score > 50
        print(score)

        return is_valid

    def convert_template(self, template: dict) -> str:
        """
        Convert Template from JSON format to str representation with fixed minutia length
        size = 6 + num_minutiae * 14
        """
        minutiae = template['minutiae']

        width = str(template['width'])
        height = str(template['height'])

        stringRepresentation = width.rjust(3, '0') + height.rjust(3, '0')

        for minutia in minutiae:
            x = str(minutia['x'])
            y = str(minutia['y'])
            type = minutia['type']
            direction = int(math.degrees(minutia['direction']))
            direction = str(direction)

            stringRepresentation += x.rjust(3, '0') + y.rjust(
                3, '0') + type[0] + direction.rjust(3, '0')

        return stringRepresentation

    def trunc_template(self, template: Template, maxMinutia=100) -> str:
        truncated_template = template.as_json()
        truncated_template['minutiae'] = truncated_template['minutiae'][:maxMinutia]
        return truncated_template

    def encrypt_data(self, data):
        aes_key = get_random_bytes(32)
        cipherAES = AES.new(aes_key, AES.MODE_CBC)
        ciphertext = cipherAES.encrypt(pad(data, AES.block_size))

        cipherRSA = PKCS1_OAEP.new(self.public_key)
        encrypted_symmetric_key = cipherRSA.encrypt(aes_key)   

        return ciphertext, encrypted_symmetric_key, cipherAES.iv

    def decrypt_data(self, data, encrypted_key, iv) -> bytes:
        cipherRSA = PKCS1_OAEP.new(self.private_key)
        symmetric_key = cipherRSA.decrypt(encrypted_key)

        cipherAES = AES.new(symmetric_key, AES.MODE_CBC, iv)
        decrypted_data = cipherAES.decrypt(data)
        original_data = unpad(decrypted_data, AES.block_size)

        return original_data


    def generate_qrcode(self, name: str, template: Union[str,bytes], template_type: str) -> bytes:
        timestamp = datetime.utcnow().timestamp()
        timestamp_as_string = str(timestamp).encode("utf-8")

        if template_type == 'ISO':
            from utils.template_conversor import convertTemplateToISO
            converted_template = convertTemplateToISO(template)
        if template_type == 'XYT':
            from utils.template_conversor import convertTemplateToXYT
            converted_template = convertTemplateToXYT(template).encode('utf-8')
        if template_type == 'PB':
            from utils.template_conversor import convertTemplateToProtocolBuffer
            converted_template = convertTemplateToProtocolBuffer(template).SerializeToString()
        if template_type == 'JSON':
            converted_template = json.dumps(template).encode('utf-8')
            
        encrypted_template , encrypted_key, iv = self.encrypt_data(converted_template)
        data_block = encrypted_key + iv + encrypted_template

        data_to_encode = b64encode(name.encode(
            "utf-8")) + b' ' + b64encode(data_block) + b' ' + b64encode(timestamp_as_string)

        qrcode = segno.make(data_to_encode)
       
        return qrcode

    def read_qrcode(self, qrcode: str) -> Tuple[str, bytes, bytes, bytes, str]:
        if TBD.isBase64(qrcode):
            img = Image.open(BytesIO(b64decode(qrcode)))
        else:
            img = Image.open(qrcode)
        
        qrcode_payload = decode(img)[0].data
        user_data, data_block, timestamp = qrcode_payload.split(b' ')
        
        user_data = b64decode(user_data).decode('utf-8')
        data_block = b64decode(data_block)
        encrypted_key = data_block[:128]
        iv = data_block[128:144]
        encrypted_template = data_block[144:]
        timestamp = b64decode(timestamp).decode()

        return user_data, encrypted_template, encrypted_key, iv, timestamp


    def validate_qrcode(self, qrcode: str, input_template: bytes) -> bool:
        user_data, encrypted_template, encrypted_key, iv, timestamp = self.read_qrcode(qrcode)
        templateISO = self.decrypt_data(encrypted_template, encrypted_key, iv)
            
        identity_is_valid = self.match_minutiae(         
             m3gl_match_iso, templateISO, input_template)
        return identity_is_valid


if __name__ == '__main__':
    fingerlink = TBD(public_key='assets/public_key.pem', private_key='assets/private_key.pem')

    image_name = 'NIST4_F0001_01'
    template = fingerlink.extract_minutiae(
        f'images/fingerprints/{image_name}.bmp', extractor=mindtct_numpy)
    template = fingerlink.trunc_template(template, maxMinutia=100)
    template_type = 'ISO'

    qrcode = fingerlink.generate_qrcode(
        name='Rhaniel Magalhães Xavier', template=template, template_type=template_type)

    qrcode.save(f'images/qrcodes/{image_name}_{template_type}_qrcode_v{qrcode.version}.png', scale=5)
    user_data, encrypted_template, encrypted_key, iv, timestamp = fingerlink.read_qrcode(f'images/qrcodes/{image_name}_{template_type}_qrcode_v{qrcode.version}.png')
    
    from utils.template_conversor import convertTemplateToISO
    is_valid = fingerlink.validate_qrcode(f'images/qrcodes/{image_name}_{template_type}_qrcode_v{qrcode.version}.png', input_template=convertTemplateToISO(template))
    print(f'is_valid: {is_valid}')
    # import copy

    # template2 = copy.deepcopy(template)

    # for i, minutia in enumerate(template2['minutiae']):
    #     disturbed = {
    #         'x': minutia['x'] + np.random.normal(0,5,1)[0],
    #         'y': minutia['y'] + np.random.normal(0,5,1)[0],
    #         'direction': minutia['direction'] +np.random.normal(0,0.01,1)[0],
    #         'type': minutia['type']
    #     }
    #     for key, value in disturbed.items():
    #         if key !='type' and value < 0: disturbed[key] = 0
        
    #     template2['minutiae'][i] = disturbed
    
    # print(template['minutiae'][10])
    # print(template2['minutiae'][10])
