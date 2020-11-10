
class FileMessage:
    
    obj_uri = None
    location = { }
    
    def __init__(self, uri, locType, rest, sType, asyncRetr):
        self.obj_uri = uri
        self.location['uri'] = uri
        self.location['type'] = locType
        self.location['restricted'] = rest
        self.location['serviceType'] = sType
        self.location['asynchronous'] = asyncRetr


    

