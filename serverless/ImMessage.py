import json
from FileMessage import FileMessage
from Link import Link

class ImMessage:
    
    #File Information
    file_information = { }
    file_name = { "name": None }
    file_size = { "size": None}
    alg = { "algorithm": None }
    alg_value = { "value": None}
    chk_sums = { "checksums": [ alg, alg_value ] }
    file_format = { "format": None } 
    headers = { "headers": None } 

    #Relationships
    relationships = [ ] 
    
    #Discovery
    discovery = { }
    links = [ ]
    parentIdentifier = { "parentIdentifier": None }
        
    #Record
    file_information = [ file_name, file_size, chk_sums, file_format, headers ] 
    file_locations = { }
    
    def set_file_locations(self, file_message):
        self.file_locations[file_message.obj_uri] = file_message.location
    
    def append_link_attributes(self, link):
        self.links.append(link.attributes)
        
    def append_relationship(self, relationship):
        self.relationships.append(relationship)
    
    discovery = { }
    discovery['links'] = links

        
    def serialize(self):
        payload = { }
        payload['file_information'] = self.file_information
        payload['relationships'] = self.relationships
        payload['fileLocations'] = self.file_locations 
        payload['discovery'] = self.discovery 
        json_payload = json.dumps(payload, indent = 4)   
        
        
        print ("IM Message:")
        print(json_payload)  
        
        #Return the dictionary or json???
        return json_payload
        



