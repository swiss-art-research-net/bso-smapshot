import os
import xml.etree.ElementTree
# assign directory
directory = '/data/temp/images'
output_directory = '/data/temp/images'
from tqdm import tqdm

# iterate over files in xml data directory
for filename in tqdm(os.listdir(directory)):
    if '.xml' in filename:
        f = os.path.join(directory, filename)
    
        # open original XML file
        et = xml.etree.ElementTree.parse(f)

        # add new tag for geolatlong (child of pose)
        new_tag = xml.etree.ElementTree.SubElement(et.findall("item/pose")[0], 'geolatlong')
        new_tag.text = '{0}#{1}'.format(et.findall("item/pose/latitude")[0].text, et.findall("item/pose/longitude")[0].text)

        # write back to file
        et.write(output_directory + '/' + f.split('/')[-1], encoding='utf-8')
            

