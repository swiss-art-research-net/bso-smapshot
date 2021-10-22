import requests

class SmapshotConnector:
    
    API_URL = ""
    OWNER_ID = False
    
    LIMIT = 20
    
    def __init__(self, owner = 3, url = "https://smapshot.heig-vd.ch/api/v1"):
        self.API_URL = url
        self.OWNER_ID = owner
        
    def _listImages(self, limit, offset=0, additionalParams={}):
        url = self.apiPath("/images")
        params = {
            'owner_id': self.OWNER_ID, 
            'limit': limit, 
            'offset': offset
        }
        for key in additionalParams:
            params[key] = additionalParams[key]
        try:
            r = requests.get(url=url, params=params)
        except:
            return False
        return r.json()
        
    def apiPath(self, path):
        return self.API_URL + path
        
    def getImageAttributes(self, imageId):
        """
        Retrieves additional attributes for a given image id
        """
        url = self.apiPath("/images/%d/attributes" % imageId)
        r = requests.get(url=url)
        return r.json()

    def listImages(self,additionalParams = {}):
        """
        Retrieves the images for a given collection owner. Defaults to collection owner 3 (SARI)
        """
        offset = 0

        initialImages = self._listImages(1, 0, additionalParams)
        numberOfImages = initialImages['count']
        
        images = []
        
        while offset < numberOfImages:
            images += self._listImages(self.LIMIT, offset, additionalParams)['rows']
            offset += self.LIMIT
            
        return images

    def listValidatedImages(self, validatedAfterDate=False):
        """
        Retrieves the valitated images for a given collection owner. Defaults to collection owner 3 (SARI)
        """
        additionalParams = {'state[0]': 'validated'}
        if validatedAfterDate:
            additionalParams['date_validated_min'] = str(validatedAfterDate)
        return self.listImages(additionalParams)