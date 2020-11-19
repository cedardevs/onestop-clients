
class FileMessage:

    def __init__(self, uri, loc_type, rest, s_type, async_retr):
        self.obj_uri = uri
        self.uri = uri
        self.type = loc_type
        self.restricted = rest
        self.service_type = s_type
        self.asynchronous = async_retr
