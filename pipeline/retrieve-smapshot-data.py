import re
import yaml
from datetime import datetime
from dicttoxml import dicttoxml
from os.path import join
from tqdm import tqdm
from xml.dom.minidom import parseString
from lib.SmapshotConnector import SmapshotConnector

configFile = './config.yml'
lastUpdatedFile = './lastUpdated.log'

try:
    with open(configFile, 'r') as f:
        config = yaml.safe_load(f)
except:
    raise Exception("Could not load config file at", configFile)

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
    filename = join(config['vars']['outputFolder'], str(image[config['vars']['filenameKey']]) + '.xml')
    xml = dicttoxml([image], attr_type=False)
    dom = parseString(xml)
    with open(filename, 'w') as f:
        f.write(dom.toprettyxml())

# Update the last updated value in the config file
with open(lastUpdatedFile, 'w') as f:
    f.write(currentTime)