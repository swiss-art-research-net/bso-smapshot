import re
import yaml
from datetime import datetime
from dicttoxml import dicttoxml
from os.path import join
from tqdm import tqdm
from xml.dom.minidom import parseString
from SmapshotConnector import SmapshotConnector

configFile = './config.yml'

try:
    with open(configFile, 'r') as f:
        config = yaml.safe_load(f)
except:
    raise Exception("Could not load config file at", configFile)

currentTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
smapshot = SmapshotConnector()

# Retrieve list of images
images = smapshot.listValidatedImages(config['lastUpdate'].strftime("%Y-%m-%dT%H:%M:%SZ"))

# Retrieve details for images
imageDetails = []
for image in tqdm(images):
    imageDetails.append(smapshot.getImageAttributes(image['id']))

# Write image data to individual files
for image in imageDetails:
    filename = join(config['outputFolder'], str(image[config['filenameKey']]) + '.xml')
    xml = dicttoxml(image, attr_type=False)
    dom = parseString(xml)
    with open(filename, 'w') as f:
        f.write(dom.toprettyxml())

# Update the last updated value in the config file
with open(configFile, 'r') as f:
    configRaw = f.read()

pattern = r'(lastUpdate:\s*)(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)'
configRaw = re.sub(pattern, 'lastUpdate: '+ currentTime, configRaw)

with open(configFile, 'w') as f:
    f.write(configRaw)