import pickle
import sys  # nopep8
sys.path.insert(0, '/home/decode_nfiq/build')  # nopep8
from finger_id import *  # nopep8

from typing import Union, Sequence
from datetime import datetime
import cv2
import json
import numpy as np
from base64 import b64decode, b64encode
from PIL import Image

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad


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
    def __init__(self, public_key:str, aes_key:str) -> None:
        self.public_key = RSA.import_key(open(public_key).read())        
        self.aes_key = open(aes_key, 'rb').read()

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

    def match_minutiae(self, matcher: str, reference_minutiae: Template, input_minutiae: Template) -> bool:
        pass

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
        cipherRSA = PKCS1_OAEP.new(self.public_key)
        encrypted_symmetric_key = cipherRSA.encrypt(self.aes_key)

        cipherAES = AES.new(self.aes_key, AES.MODE_CBC)
        ciphertext = cipherAES.encrypt(pad(data, AES.block_size))

        return ciphertext, encrypted_symmetric_key

    def generate_qrcode(self, name: str, template: Union[str,bytes], template_type: str) -> bytes:
        timestamp = datetime.utcnow().timestamp()
        timestamp_as_string = str(timestamp).encode("utf-8")

        if template_type == 'ISO':
            from convertTemplateToISO import convertTemplateToISO
            converted_template = convertTemplateToISO(template)
        if template_type == 'XYT':
            from convertTemplateToXYT import convertTemplateToXYT
            converted_template = convertTemplateToXYT(template).encode('utf-8')
        if template_type == 'PB':
            from convertTemplateToProtocolBuffer import convertTemplateToProtocolBuffer
            converted_template = convertTemplateToProtocolBuffer(template).SerializeToString()
        if template_type == 'JSON':
            converted_template = json.dumps(template).encode('utf-8')
            
        encrypted_data , encrypted_key = self.encrypt_data(converted_template)


        data_to_encode = b64encode(name.encode(
            "utf-8")) + b' ' + b64encode(encrypted_data) + b64encode(encrypted_key) + b' ' + b64encode(timestamp_as_string)

        qrcode = segno.make(data_to_encode)
        return qrcode

    def read_qrcode(self, qrcode: str) -> QRCodeData:
        pass

    def validate_qrcode(self, qrcode: str, input_minutiae: Template, matcher: str = 'm3gl') -> bool:
        input_qrcode = self.read_qrcode(qrcode)
        identity_is_valid = self.match_minutiae(
            matcher, input_qrcode.minutiae, input_minutiae)
        return identity_is_valid


if __name__ == '__main__':
    fingerlink = TBD(public_key='assets/public_key.pem', aes_key='assets/aes_key.bin')

    image_name = 'NIST4_F0001_01'
    template = fingerlink.extract_minutiae(
        f'images/fingerprints/{image_name}.bmp', extractor=mindtct_numpy)
    template = fingerlink.trunc_template(template, maxMinutia=100)

    template_type = 'JSON'

    qrcode = fingerlink.generate_qrcode(
        name='Rhaniel Magalhães Xavier', template=template, template_type=template_type)

    qrcode.save(f'images/qrcodes/{image_name}_{template_type}_qrcode_v{qrcode.version}.png', scale=5)
  


