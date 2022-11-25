import json
import math

template_name='templatefull'

def convertTemplateToXYT(template):
    # with open(f'templates/json/{template_name}.json', 'r') as json_file:
        # template = json.load(json_file)
    minutiae = template['minutiae']

    templateXYT = ''

    for minutia in minutiae:
        templateXYT += f"{minutia['x']}\t{minutia['y']}\t{int(math.degrees(minutia['direction']))}\n"

    return templateXYT.rstrip()
        
        # with open(f'{template_name}.xyt','w') as xyt_file:
        #     for minutia in minutiae:
        #         xyt_file.write(f"{minutia['x']}\t{minutia['y']}\t{int(math.degrees(minutia['direction']))}\n")


if __name__ == '__main__':
    with open(f'templates/json/template1.json', 'r') as json_file:
        template = json.load(json_file)
        templateXYT = convertTemplateToXYT(template)
        print(templateXYT)
        with open('testefile.xyt', 'w') as out_file:
            out_file.write(templateXYT)
    