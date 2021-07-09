import unittest

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship_type import RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship import Relationship


class test_ParsedRecord(unittest.TestCase):
    fileLocation_dict = {
        "fileLocations":{
            "s3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc":{
                "serviceType":"Amazon:AWS:S3",
                "deleted":False,
                "restricted":False,
                "asynchronous":False,
                "locality":"us-east-1",
                "lastModified":1572430074000,
                #Todo: change this type.
                "type": {"type":"ACCESS"},
                "optionalAttributes":{
                },
                "uri":"s3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc"
            }
        }
    }

    relationship_dict = {
        "id": "5b58de08-afef-49fb-99a1-9c5d5c003bde",
        "type": RelationshipType.collection
    }
    relationships_dict = {
        "relationships":[
            relationship_dict,
            {
                "id":"6668de08-afef-49fb-99a1-9c5d5c003bde",
                "type":{"type":"collection"}
            }
        ]
    }

    @unittest.skip
    def test_type(self):
        content_dict = {
            "fileInformation":{
                "checksums":[
                    {
                        "value":"4809084627a18d54db59659819f8a4b5d2c76367",
                        "algorithm":"SHA1"
                    }
                ],
                "headers":"NetCDF file reader",
                "size":22876986,
                "name":"OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc",
                "format":"NetCDF",
                "optionalAttributes":{
                }
            }
        }

        parsed_record = ParsedRecord.from_dict(content_dict)

        self.assertIsNotNone(parsed_record)

    @unittest.skip
    def test_discovery(self):
        content_dict = {
            "discovery":{
                "fileIdentifier":"1034194888",
                "temporalBounding":{
                    "beginDate":"2019-10-30T05:50:39Z",
                    "endDate":"2019-10-30T06:00:11Z"
                },
                "parentIdentifier":"5b58de08-afef-49fb-99a1-9c5d5c003bde",
                "links":[
                    {
                        "linkFunction":"download",
                        "linkUrl":"s3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc",
                        "linkName":"Amazon S3",
                        "linkProtocol":"HTTPS"
                    }
                ],
                "spatialBounding":{
                    "coordinates":[
                        [
                            [
                                -156.2995,
                                -81.3282
                            ],
                            [
                                6.2995,
                                -81.3282
                            ],
                            [
                                6.2995,
                                81.3282
                            ],
                            [
                                -156.2995,
                                81.3282
                            ],
                            [
                                -156.2995,
                                -81.3282
                            ]
                        ]
                    ],
                    "type":"Polygon"
                },
                "title":"OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc"
            }
        }

        parsed_record = ParsedRecord.from_dict(content_dict)

        self.assertIsNotNone(parsed_record)

# TODO
#    def test_analysis(self):

    @unittest.skip
    def test_fileInformation(self):
        content_dict = {
            "fileInformation":{
                "checksums":[
                    {
                        "value":"4809084627a18d54db59659819f8a4b5d2c76367",
                        "algorithm":"SHA1"
                    }
                ],
                "headers":"NetCDF file reader",
                "size":22876986,
                "name":"OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc",
                "format":"NetCDF",
                "optionalAttributes":{
                }
            }
        }

        parsed_record = ParsedRecord.from_dict(content_dict)

        self.assertIsNotNone(parsed_record)

    @unittest.skip
    def test_fileLocations(self):
        content_dict = {
            "fileLocations":{
                "s3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc":{
                    "serviceType":"Amazon:AWS:S3",
                    "deleted":False,
                    "restricted":False,
                    "asynchronous":False,
                    "locality":"us-east-1",
                    "lastModified":1572430074000,
                    "type":"ACCESS",
                    "optionalAttributes":{
                    },
                    "uri":"s3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc"
                }
            }
        }

        parsed_record = ParsedRecord.from_dict(content_dict)
        print("parsed_record:%s"%parsed_record)
        self.assertIsNotNone(parsed_record)

# TODO
#    def test_publishing(self):

    def test_relationships_all_vars_set(self):
        relationship = Relationship(**self.relationship_dict)

        self.assertEqual(relationship.id, self.relationship_dict['id'])
        self.assertEqual(relationship.type, self.relationship_dict['type'])

    def test_relationships_optionals(self):
        id = '12'
        relationship = Relationship(id=id, type=None)

        self.assertEqual(relationship.id, id)
