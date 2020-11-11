
class FileMessage:
    
    obj_uri = None
    location = {}
    
    def __init__(self, uri, loc_type, rest, s_type, async_retr):
        self.obj_uri = uri
        self.location['uri'] = uri
        self.location['type'] = loc_type
        self.location['restricted'] = rest
        self.location['serviceType'] = s_type
        self.location['asynchronous'] = async_retr


    

