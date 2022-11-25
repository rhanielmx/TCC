import sys #nopep8
sys.path.insert(0, 'decode_nfiq/build') #nopep8

from convertTemplateToXYT import convertTemplateToXYT
from convertTemplateToISO import convertTemplateToISO
from convertTemplateToProtocolBuffer import convertTemplateToProtocolBuffer

import json
import wsq
from PIL import Image
from finger_id import *
from base64 import b64encode
import pandas as pd


def loadFileBase64(fn):
    data = open(fn, "rb").read()
    return b64encode(data)


img = loadFileBase64('images/fingerprint.wsq')
tf = decode_extract_wsq(img, qualityThreshold=0, event_id='0')
tf_dict = json.loads(tf)

minutiaCount = len(tf_dict['minutiae'])

# minutiaeValuesToGenerateData = [1, 10, 20, 50, 100, min(150, minutiaCount)]

sizeDataFrame = pd.DataFrame([], columns=['JSON', 'XYT', 'ISO', 'PB'])

for i in range(minutiaCount+1):
    templateJSON = tf_dict.copy()
    templateJSON['minutiae'] = templateJSON['minutiae'][:i]
    templateXYT = convertTemplateToXYT(templateJSON)
    templateISO = convertTemplateToISO(templateJSON)
    templatePB = convertTemplateToProtocolBuffer(templateJSON)

    new_entry = {
        'JSON': len(json.dumps(templateJSON)),
        'XYT': len(templateXYT),
        'ISO': len(templateISO),
        'PB': len(templatePB.SerializeToString())
    }

    sizeDataFrame = sizeDataFrame.append(new_entry,ignore_index=True)

sizeDataFrame.to_csv('data/format_size_comparation.csv',index=False)