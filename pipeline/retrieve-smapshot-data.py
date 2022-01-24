import csv
import re
import yaml
from datetime import datetime
from dicttoxml import dicttoxml
from os.path import join
from string import Template
from tqdm import tqdm
from xml.dom.minidom import parseString
from lib.SmapshotConnector import SmapshotConnector

config = {
    'outputFolderImages': '../data/xml/images',
    'outputFolderObservations': '../data/xml/observations',
    'filenameKeyImages': 'original_id',
    'filenameKeyObservations': 'id',
    'imageMetaDataFile': '../data/meta/images.csv'
}
lastUpdatedFile = './lastUpdated.log'

try: 
    with open(lastUpdatedFile, 'r') as f:
        lastUpdate = datetime.strptime(f.read(), "%Y-%m-%dT%H:%M:%SZ")
except:
    lastUpdate = datetime.fromtimestamp(0)

currentTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
smapshot = SmapshotConnector()

# Retrieve list of images
images = smapshot.listValidatedImages(lastUpdate.strftime("%Y-%m-%dT%H:%M:%SZ"))

# Retrieve details for images
imageDetails = []
for image in tqdm(images):
    imageDetails.append(smapshot.getImageAttributes(image['id']))

# Write image data to individual files
for image in imageDetails:
    filename = join(config['outputFolderImages'], str(image[config['filenameKeyImages']]) + '.xml')
    xml = dicttoxml([image], attr_type=False)
    dom = parseString(xml)
    with open(filename, 'w') as f:
        f.write(dom.toprettyxml())

# Retrieve list of observations
observations = smapshot.listValidatedObservations(lastUpdate.strftime("%Y-%m-%dT%H:%M:%SZ"))

# Read image metadata
imageMetaData = []
imageMetaDataKeys = {}
with open(config['imageMetaDataFile'], 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        imageMetaDataKeys[row['image']] = len(imageMetaData)
        row['width'] = int(row['width'])
        row['height'] = int(row['height'])
        imageMetaData.append(row)

# Add coordinates in pixels to observations
svgTemplate = Template("""<svg xmlns='http://www.w3.org/2000/svg'><path xmlns="http://www.w3.org/2000/svg" d="M${x0},${y0}l${halfW},0l0,0l${halfW},0l 0,${halfH}l 0,${halfH}l -${halfW},0l -${halfW},0l 0,-${halfH}z" data-paper-data="{&quot;defaultStrokeValue&quot;:1,&quot;editStrokeValue&quot;:5,&quot;currentStrokeValue&quot;:1,&quot;rotation&quot;:0,&quot;deleteIcon&quot;:null,&quot;rotationIcon&quot;:null,&quot;group&quot;:null,&quot;editable&quot;:true,&quot;annotation&quot;:null}" id="rectangle_e880ad36-1fef-4ce3-835d-716ba7db628a" fill-opacity="0" fill="#00bfff" fill-rule="nonzero" stroke="#00bfff" stroke-width="4.04992" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"/></svg>""")

for observation in observations:
    iiifUrl = observation['image']['media']['tiles']['url'][:-10]
    observation['iiifUrl'] = iiifUrl
    if observation['coord_x']:
        imageData = imageMetaData[imageMetaDataKeys[iiifUrl]]
        multiplierX = imageData['width']
        multiplierY = imageData['width'] # OpenSeaDragen returns y coordinates in relation to ratio of image, therefore the multiplier for vertical coordinates is the same as for horizontal coordinates
        coordinates_pixel = {
            'x': int(float(observation['coord_x']) * multiplierX),
            'y': int(float(observation['coord_y']) * multiplierY),
            'width': int(float(observation['width']) * multiplierX),
            'height': int(float(observation['height']) * multiplierY),
        }
        observation['coordinates_pixel'] = coordinates_pixel
        observation['svg_path'] = svgTemplate.substitute(x0=coordinates_pixel['x'], y0=coordinates_pixel['y'], halfW=coordinates_pixel['width']/2, halfH=coordinates_pixel['height']/1)
        
# Write observation data to individual files
for observation in observations:
    filename = join(config['outputFolderObservations'], str(observation[config['filenameKeyObservations']]) + '.xml')
    xml = dicttoxml(observation, attr_type=False)
    dom = parseString(xml)
    
    if 'svg_path' in observation:
        svgElement = dom.createElement("svg_raw")
        cdata = dom.createCDATASection(observation['svg_path'])
        svgElement.appendChild(cdata)
        dom.documentElement.appendChild(svgElement)

    with open(filename, 'w') as f:
        f.write(dom.toprettyxml())

# Update the last updated value
with open(lastUpdatedFile, 'w') as f:
    f.write(currentTime)