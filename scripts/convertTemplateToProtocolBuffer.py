import proto.template_pb2 as template_pb2
import proto.minutia_pb2 as minutia_pb2
import json
import math

template_name = 'templatefull'

with open(f'templates/json/{template_name}.json', 'r') as j:
    json_data = json.load(j)
    width=json_data['width']
    height=json_data['height']
    minutiae=json_data['minutiae']

def convertTemplateToProtocolBuffer(template):
  templatePB=template_pb2.Template()
  templatePB.width=template['width']
  templatePB.height=template['height']

  i=0
  for minutia in template['minutiae']:
      i+=1
      minutiapb=templatePB.minutiaepb.add()
      minutiapb.x=minutia['x']
      minutiapb.y=minutia['y']
      minutiapb.direction=int(math.degrees(minutia['direction']))

      if minutia['type'] == "ending":
        minutiapb.type = minutia_pb2.Minutiapb.MinutiaType.ENDING
      elif minutia['type'] == "bifurcation":
        minutiapb.type = minutia_pb2.Minutiapb.MinutiaType.BIFURCATION
      else:
        minutiapb.type = minutia_pb2.Minutiapb.MinutiaType.MINUTIA_UNDEFINED

  return templatePB

if __name__ == '__main__':
  template_name = 'template10'

  with open(f'templates/json/{template_name}.json', 'r') as j:
      json_data = json.load(j)
      width=json_data['width']
      height=json_data['height']
      minutiae=json_data['minutiae']

      templatePB = convertTemplateToProtocolBuffer(json_data)
      print(templatePB.SerializeToString())
      with open(f'templates/pb/{template_name}.bin', "wb") as f:
          f.write(templatePB.SerializeToString())
