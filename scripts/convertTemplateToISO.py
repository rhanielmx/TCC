import json
import math

def createMaskToGetIntervalBits(start, end):
    """
        from right to left
    """
    mask = 0
    for i in range(start, end): 
        mask |= 1 << i    
    return mask

def quantizeAngle(angle: float) -> int:
    angle = math.degrees(angle) * (256/360)
    angle = round(angle) & ((1<<8)-1)

    return angle



def convertTemplateToISO(template):
    MINCOUNT = len(template['minutiae'])
    SIGNATURE = "FMR"
    VERSION = " 20"
    TOTALBYTES = 30+6*MINCOUNT
    WIDTH = template['width']
    HEIGHT = template['height']
    RESOLUTIONX=197 #for 500dpi images
    RESOLUTIONY=197 #for 500dpi images
    FPCOUNT = 1
    POSITION = 0 #unknown finger
    VIEWOFFSET = 0
    SAMPLETYPE = 0 #Most common one. Should be set if type is unknown
    FPQUALITY = 100
    #MINCOUNT
    EXTBYTES=0

    MINTYPE_MAPPER = {
        'ending': 1,
        'bifurcation': 2
    }

    templateISO = bytearray(TOTALBYTES)

    #HEADER(24bytes) - contains MAGIC, VERSION, TOTALBYTES, DEVSTAMP, DEVID, WIDTH, HEIGHT, RESOLUTIONX, RESOLUTIONY, FPCOUNT
    ##MAGIC(4 bytes) - Contains the file signature: "FMR\0"
    for i, char in enumerate(SIGNATURE):
        templateISO[i] = ord(char)

    ##VERSION(4 bytes) - Contains the version of this format: " 20\0"
    for i, char in enumerate(VERSION):
        templateISO[i+4] = ord(char)

    ##TOTALBYTES(4 bytes) - Contains the template total length
    templateISO[8:12] = TOTALBYTES.to_bytes(4, byteorder='big', signed=False)

    ##DEVSTAMP(4bits) and DEVID(12bits) stay zeroed in this implementation

    ##WIDTH(2 bytes) - Image width
    templateISO[14:16] = WIDTH.to_bytes(2, byteorder='big', signed=False)

    ##HEIGHT(2 bytes) - Image height

    templateISO[16:18] = HEIGHT.to_bytes(2, byteorder='big', signed=False)

    ##RESOLUTIONX(2bytes) - Horizontal pixel density
    templateISO[18:20] = RESOLUTIONX.to_bytes(2, byteorder='big', signed=False)

    ##RESOLUTIONY(2bytes) - Vertical pixel density
    templateISO[20:22] = RESOLUTIONY.to_bytes(2, byteorder='big', signed=False)

    ##FPCOUNT(1byte) - Total number of fingerprints in the template
    templateISO[22:23] = FPCOUNT.to_bytes(1, byteorder='big', signed=False)

    # byte 24 is reserved and remain zeroed

    #FINGERPRINT INFORMATION(6 or more bytes) - contains POSITION, VIEWOFFSET, SAMPLETYPE, FPQUALITY, MINCOUNT, EXTBYTES

    ##POSITION(1byte) - Fingerprint position on hand (i. e. which finger is encoded)
    templateISO[24:25] = POSITION.to_bytes(1, byteorder='big', signed=False)

    ##VIEWOFFSET(4bits)
    templateISO[25] |= VIEWOFFSET << 4 #reverse as templateISO[25] >> 4

    ##SAMPLETYPE(4bits) - Impression Type. Indicates how the fingerprint was captured

    templateISO[25] |= SAMPLETYPE #reverse as templateISO[25] & ((1<<4) - 1)

    ##FPQUALITY(1 byte) - Fingerprint Quality. Indicates overall fingerprint quality
    templateISO[26:27] = FPQUALITY.to_bytes(1, byteorder='big', signed=False)

    ##MINCOUNT(1 byte) = Number of minutia in the fingerprint
    templateISO[27:28] = MINCOUNT.to_bytes(1, byteorder='big', signed=False)

    #MINUTIA INFORMATION(6 bytes per minutia) - contains MINTYPE, MINX, MINY, MINANGLE, MINQUALITY
    for i, minutia in enumerate(template['minutiae']):
        try:
            MINTYPE = MINTYPE_MAPPER[minutia['type']]
        except KeyError:
            MINTYPE = 0

        MINX=minutia['x']
        MINY=minutia['y']
        MINANGLE = quantizeAngle(minutia['direction'])
        MINQUALITY=0
        
        ##MINTYPE(2 bits) - Type of minutia represented - Ending(01), Bifurcation(10), Other(00)

        templateISO[28+6*i] |= MINTYPE << 6

        #TODO - rewrite?
        ##MINX(14 bits) - Location of the minutia on the fingerprint in pixel units along X axis. Pixels are counted left-to-right, starting with zero.
        positionX = MINX.to_bytes(2, byteorder='big', signed=False)

        templateISO[28+6*i] |= positionX[0] & ((1 << 6) - 1)
        templateISO[29+6*i] |= positionX[1]

        ##MINX(14 bits, 2 bytes are alocated but the first 2bits are always 0) - Location of the minutia on the fingerprint in pixel units along Y axis. Pixels are counted left-to-right, starting with zero.
        positionY = MINY.to_bytes(2, byteorder='big', signed=False)

        templateISO[30+6*i] |= positionY[0] & ((1 << 6) - 1)
        templateISO[31+6*i] |= positionY[1]

        ##MINANGLE(1 byte)
        templateISO[32+6*i:33+6*i] = MINANGLE.to_bytes(1, byteorder='big', signed=False)

        ##MINQUALITY(1 byte)
        templateISO[33+6*i:34+6*i] = MINQUALITY.to_bytes(1, byteorder='big', signed=False)

    ##EXTBYTES(2 bytes)
    templateISO[-2:] = EXTBYTES.to_bytes(2, byteorder='big', signed=False)

    return templateISO

if __name__ == '__main__':
    template_name = 'template1'

    with open(f'templates/json/{template_name}.json', 'r') as file:
        template = json.load(file)
        templateISO = convertTemplateToISO(template)
        with open(f'templates/iso/{template_name}.iso', 'wb') as f:
            f.write(templateISO)