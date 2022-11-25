from PIL import Image
import wsq

import os

root = 'dataset'
output = 'output'

if not os.path.isdir(output):
    os.makedirs(output)

for path, subdirs, file in os.walk(root):
    for name in file:
        output_path = path.replace('dataset','output')
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        

        img_path = os.path.join(path,name)
        img = Image.open(img_path)
        
        output_path = os.path.join(output_path,name.replace('wsq','png'))
        img.save(output_path)