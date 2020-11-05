
class Link:

    #   Example
    #   {
    #     "linkFunction": "download",
    #     "linkName": "Amazon S3",
    #     "linkProtocol": "HTTPS",
    #     "linkUrl": "<object_store_url>"
    #   }

    
    attributes = { }
    
    # parameterized constructor
    def __init__(self, func, name, proto, url):
        self.attributes['linkFunction'] = func
        self.attributes['linkName'] = name
        self.attributes['linkProtocol'] = proto
        self.attributes['linkUrl'] = url

    


      
    

