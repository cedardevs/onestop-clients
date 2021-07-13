import unittest

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord
from onestop.schemas.psiSchemaClasses.keywords_element import KeywordsElement
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.discovery import Discovery
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location import FileLocation
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.temporal_bounding import TemporalBounding
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship import Relationship
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship_type import RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.record_type import RecordType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.link import Link
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.responsible_party import ResponsibleParty
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.reference import Reference
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location_type import FileLocationType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.valid_descriptor import ValidDescriptor
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.analysis import Analysis
from onestop.schemas.psiSchemaClasses.identification_analysis import IdentificationAnalysis
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.operation import Operation
from onestop.schemas.psiSchemaClasses.data_format import DataFormat
from onestop.schemas.psiSchemaClasses.platform import Platform
from onestop.schemas.psiSchemaClasses.time_range_descriptor import TimeRangeDescriptor
from onestop.schemas.psiSchemaClasses.instruments import Instruments
from onestop.schemas.geojsonSchemaClasses.line_string_type import LineStringType
from onestop.schemas.geojsonSchemaClasses.multi_line_string_type import MultiLineStringType
from onestop.schemas.geojsonSchemaClasses.multi_point_type import MultiPointType
from onestop.schemas.geojsonSchemaClasses.multi_polygon_type import MultiPolygonType
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.geojsonSchemaClasses.polygon_type import PolygonType
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.point import Point
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.multi_point import MultiPoint
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.line_string import LineString
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.multi_line_string import MultiLineString
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.polygon import Polygon
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.multi_polygon import MultiPolygon
from onestop.schemas.util.jsonEncoder import EnumEncoder, as_enum, EnumEncoderValue
import json

class test_ParsedRecord(unittest.TestCase):

    fileLocation_dict = {
        "serviceType":"Amazon:AWS:S3",
        "deleted":False,
        "restricted":False,
        "asynchronous":False,
        "locality":"us-east-1",
        "lastModified":1572430074000,
        "type": FileLocationType.INGEST,
        "optionalAttributes":{
        },
        "uri":"s3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc"
    }

    relationship_dict = {
        "id": "5b58de08-afef-49fb-99a1-9c5d5c003bde",
        "type": RelationshipType.COLLECTION
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

    # Discovery Related items
    link_dict = {
        "linkName": "Amazon S3",
        "linkProtocol": "HTTPS",
        "linkUrl": "https://s3.amazonaws.com/nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2",
        "linkDescription": "who knows",
        "linkFunction": "download"
    }
    keywordsElement_dict = {
        'values': ['value1'],
        'type': 'type1',
        'namespace': 'name space'
    }
    temporalBounding_dict = {
        'beginDate': 'begin date',
        'beginIndeterminate': 'begin ind',
        'endDate': 'end date',
        'endIndeterminate': 'end ind',
        'instant': 'instant',
        'instantIndeterminate': 'instant ind',
        'description': 'desc'
    }
    point_dict = {
        'type': PointType.POINT,
        'coordinates': [0.0, 1.1, 2.2, 3.3]
    }
    multiPoint_dict = {
        'type': MultiPointType.MULTIPOINT,
        'coordinates': [[0.0, 1.0], [2.0, 1.0]]
    }
    lineString_dict = {
        'type': LineStringType.LINESTRING,
        'coordinates': [[0.0, 1.0], [2.0, 1.0]]
    }
    multiLineString_dict = {
        'type': MultiLineStringType.MULTILINESTRING,
        'coordinates': [[[0.0, 1.0], [2.0, 1.0]], [[0.0, 2.0], [2.0, 2.0]]]
    }
    polygon_dict = {
        'type': PolygonType.POLYGON,
        'coordinates': [[[0.0, 1.0], [2.0, 1.0]], [[0.0, 2.0], [2.0, 2.0]]]
    }
    multiPolygon_dict = {
        'type': MultiPolygonType.MULTIPOLYGON,
        'coordinates': [[[[0.0, 1.0], [2.0, 1.0]], [[0.0, 2.0], [2.0, 2.0]]], [[[1.0, 1.0], [2.0, 1.0]], [[0.0, 2.0], [2.0, 2.0]]]]
    }
    instruments_dict = {
        'instrumentIdentifier': 'ident',
        'instrumentType': 'type',
        'instrumentDescription': 'desc'
    }
    operation_dict = {
        'operationDescription': 'desc',
        'operationIdentifier': 'iden',
        'operationStatus': 'status',
        'operationType': 'type'
    }
    platform_dict = {
        'platformIdentifier': 'ident',
        'platformDescription': 'desc',
        'platformSponsor': ['sponsor1']
    }
    dateFormat_dict = {
        'name': 'date1',
        'version': 'version1'
    }
    responsibleParty_dict = {
        'individualName': 'person name',
        'organizationName': 'organization',
        'positionName': 'position name',
        'role': 'role',
        'email': 'email addy',
        'phone': 'phone'
    }
    reference_dict = {
        'title': 'a title',
        'date': 'date',
        'links': [link_dict]
    }
    discovery_dict = {
        'fileIdentifier': 'gov.noaa.nodc:NDBC-COOPS',
        'parentIdentifier': 'gov.noaa.nodc:NDBC-COOPS',
        'hierarchyLevelName': '',
        'doi': 'doi',
        'purpose': 'purpose',
        'status': 'status',
        'credit': 'credit',
        'title': 'title',
        'alternateTitle': 'alternate title',
        'description': 'description',
        'keywords': [keywordsElement_dict],
        'topicCategories': ['category1'],
        'temporalBounding': temporalBounding_dict,
        'spatialBounding': None,
        'isGlobal': False,
        'acquisitionInstruments': [instruments_dict],
        'acquisitionOperations': [operation_dict],
        'acquisitionPlatforms': [platform_dict],
        'dataFormats': [dateFormat_dict],
        'links': [link_dict],
        'responsibleParties': [responsibleParty_dict],
        'thumbnail': 'thumbnail',
        'thumbnailDescription': 'thumbnail description',
        'creationDate': 'creation date',
        'revisionDate': 'revision date',
        'publicationDate': 'publicationd date',
        'citeAsStatements': ['cite as statements'],
        'crossReferences': [reference_dict],
        'largerWorks': [reference_dict],
        'useLimitation': 'use limitation',
        'legalConstraints': ['legal constraints'],
        'accessFeeStatement': 'access fee',
        'orderingInstructions': 'no instructions',
        'edition': 'edition1',
        'dsmmAccessibility': -4,
        'dsmmDataIntegrity': -3,
        'dsmmDataQualityAssessment': -2,
        'dsmmDataQualityAssurance': -1,
        'dsmmDataQualityControlMonitoring': 1,
        'dsmmPreservability': 2,
        'dsmmProductionSustainability': 3,
        'dsmmTransparencyTraceability': 4,
        'dsmmUsability': 5,
        'dsmmAverage': 5.0,
        'updateFrequency': 'update freq',
        'presentationForm': 'presentation form'
    }

    identificationAnalysis_dict = {
        'fileIdentifierExists': True,
        'fileIdentifierString': 'file iden',
        'doiExists': False,
        'doiString': 'doi',
        'parentIdentifierExists': True,
        'parentIdentifierString': 'parent iden',
        'hierarchyLevelNameExists': False,
        'isGranule': True
    }
    titleAnalysis_dict = {
        'titleExists': True,
        'titleCharacters': 1,
        'alternateTitleExists': True,
        'alternateTitleCharacters': 2,
        'titleFleschReadingEaseScore': 3.0,
        'alternateTitleFleschReadingEaseScore': 4.0,
        'titleFleschKincaidReadingGradeLevel': 5.0,
        'alternateTitleFleschKincaidReadingGradeLevel': 6.0
    }
    descriptionAnalysis_dict = {
        'descriptionExists': True,
        'descriptionCharacters': 3,
        'descriptionFleschReadingEaseScore': 1.0,
        'descriptionFleschKincaidReadingGradeLevel': 2.0
    }
    dataAccessAnalysis_dict = {
        'dataAccessExists': False
    }
    thumbnail_dict = {
        'thumbnailExists': True
    }
    temporalBoundingAnalysis_dict = {
        'beginDescriptor': ValidDescriptor.VALID,
        'beginPrecision': 'begin prec',
        'beginIndexable': True,
        'beginZoneSpecified': 'begin zone',
        'beginUtcDateTimeString': 'begin utc',
        'beginYear': 2021,
        'beginDayOfYear': 2,
        'beginDayOfMonth': 2,
        'beginMonth': 2,
        'endDescriptor': ValidDescriptor.INVALID,
        'endPrecision': 'end prec',
        'endIndexable': False,
        'endZoneSpecified': 'end zone',
        'endUtcDateTimeString': 'end utc',
        'endYear': 2025,
        'endDayOfYear': 2,
        'endDayOfMonth': 2,
        'endMonth': 2,
        'instantDescriptor': ValidDescriptor.UNDEFINED,
        'instantPrecision': 'instant prec',
        'instantIndexable': False,
        'instantZoneSpecified': 'instant zone',
        'instantUtcDateTimeString': 'instant utc',
        'instantEndUtcDateTimeString': 'instant end utc',
        'instantYear': 2,
        'instantDayOfYear': 2,
        'instantEndDayOfYear': 2,
        'instantDayOfMonth': 2,
        'instantEndDayOfMonth': 2,
        'instantMonth': 2,
        'instantEndMonth': 2,
        'rangeDescriptor': TimeRangeDescriptor.AMBIGUOUS
    }
    spatialBounding_dict = {
        'spatialBoundingExists': False,
        'isValid': True,
        'validationError': 'validation'
    }
    analysis_dict = {
        'identification': identificationAnalysis_dict,
        'titles': titleAnalysis_dict,
        'description': descriptionAnalysis_dict,
        'dataAccess': dataAccessAnalysis_dict,
        'thumbnail': thumbnail_dict,
        'temporalBounding': temporalBoundingAnalysis_dict,
        'spatialBounding': spatialBounding_dict
    }
    checksum_dict = {
        'algorithm': ChecksumAlgorithm.MD5,
        'value': 'value1'
    }
    fileInformation_dict = {
        'name': 'file name',
        'size': 1,
        'checksums': [checksum_dict],
        'format': 'format',
        'headers': 'header',
        'optionalAttributes': {'attr1': 'value1', 'attr2': 'value2'}
    }
    publishing_dict = {
        'isPrivate': True,
        'until': -1
    }
    relationships_dict = {
        'type': RelationshipType.COLLECTION,
        'id': 'id1'
    }
    errorEvent_dict = {
        'title': 'title1',
        'detail': 'detail1',
        'status': 404,
        'code': 500,
        'source': 'source1'
    }
    parsedRecord_dict = {
        'type': RecordType.COLLECTION,
        'discovery': discovery_dict,
        'analysis': analysis_dict,
        'fileInformation': fileInformation_dict,
        'fileLocations': {
            's3://noaa-goes16/ABI-L1b-RadF/2019/303/09/OR_ABI-L1b-RadF-M6C10_G16_s20193030950389_e20193031000109_c20193031000158.nc': {
                **fileLocation_dict
            }
        },
        'publishing': publishing_dict,
        'relationships': [relationships_dict],
        'errors': [errorEvent_dict]
    }

    def test_parsed_record_corner_case(self):
        value = {
            "type": "granule",
            "content": "{"
                       "\"discovery\": {\n            "
                       "\"fileIdentifier\": \"92ade5dc-946d-11ea-abe4-0242ac120004\",\n            "
                       "\"links\": [\n                {\n                    "
                       "\"linkFunction\": \"download\",\n                    "
                       "\"linkName\": \"Amazon S3\",\n                    "
                       "\"linkProtocol\": \"HTTPS\",\n                    "
                       "\"linkUrl\": \"https://s3.amazonaws.com/nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\"\n                "
                       "}\n            ],\n            "
                       "\"parentIdentifier\": \"0fad03df-0805-434a-86a6-7dc42d68480f\",\n            "
                       "\"spatialBounding\": null,\n            "
                       "\"temporalBounding\": {\n                "
                       "\"beginDate\": \"2020-05-12T16:20:15.158Z\", \n                "
                       "\"endDate\": \"2020-05-12T16:21:51.494Z\"\n            "
                       "},\n            "
                       "\"title\": \"HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\"\n        "
                       "},\n        "
                       "\"fileInformation\": {\n  "
                       "\"checksums\": [{"
                       "\"algorithm\": \"MD5\","
                       "\"value\": \"44d2452e8bc2c8013e9c673086fbab7a\""
                       "}]\n, "
                       "\"optionalAttributes\":{},          "
                       "\"format\": \"HSD\",\n            "
                       "\"name\": \"HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\",\n            "
                       "\"size\": 208918\n        "
                       "},\n        "
                       "\"fileLocations\": {\n     "
                       "\"s3://nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\": {\n"
                       "\"optionalAttributes\":{},       "
                       "\"uri\":\"//nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\",   "
                       "\"asynchronous\": false,\n                "
                       "\"deleted\": false,\n                "
                       "\"lastModified\": 1589300890000,\n                "
                       "\"locality\": \"us-east-1\",\n                "
                       "\"restricted\": false,\n                "
                       "\"serviceType\": \"Amazon:AWS:S3\",\n                "
                       "\"type\": {\"__enum__\": \"FileLocationType.INGEST\"},\n                "
                       "\"uri\": \"s3://nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\"\n                   "
                       "}\n        "
                       "},\n        "
                       "\"relationships\": [\n            {\n                "
                       "\"id\": \"0fad03df-0805-434a-86a6-7dc42d68480f\",\n                "
                       "\"type\": {\"__enum__\": \"RelationshipType.COLLECTION\"}           }\n        ]\n    "
                       "}",
            "contentType": "application/json",
            "method": "PUT",
            "source": "unknown",
            "operation": "ADD"
        }

        content_dict = json.loads(value['content'], object_hook=as_enum)

        ParsedRecord(**content_dict)
        ParsedRecord.from_dict(content_dict)

    # Note: Didn't make unit tests for ENUMS since they don't execute any methods.
    def test_parsed_record_all_vars_set(self):
        parsedRecord = ParsedRecord(**self.parsedRecord_dict)

        self.assertEqual(parsedRecord.type, self.parsedRecord_dict['type'])

    def test_discovery_all_vars_set(self):
        discovery = Discovery(**self.discovery_dict)

        self.assertIsNotNone(discovery)

    def test_keywords_all_vars_set(self):
        keywords = KeywordsElement(**self.keywordsElement_dict)

        self.assertEqual(keywords.values, self.keywordsElement_dict['values'])
        self.assertEqual(keywords.type, self.keywordsElement_dict['type'])
        self.assertEqual(keywords.namespace, self.keywordsElement_dict['namespace'])

    def test_temporalBounding_all_vars_set(self):
        temporal = TemporalBounding(**self.temporalBounding_dict)

        self.assertEqual(temporal.beginDate, self.temporalBounding_dict['beginDate'])
        self.assertEqual(temporal.beginIndeterminate, self.temporalBounding_dict['beginIndeterminate'])
        self.assertEqual(temporal.endDate, self.temporalBounding_dict['endDate'])
        self.assertEqual(temporal.endIndeterminate, self.temporalBounding_dict['endIndeterminate'])
        self.assertEqual(temporal.instant, self.temporalBounding_dict['instant'])
        self.assertEqual(temporal.instantIndeterminate, self.temporalBounding_dict['instantIndeterminate'])
        self.assertEqual(temporal.description, self.temporalBounding_dict['description'])

    def test_point_all_vars_set(self):
        point = Point(**self.point_dict)

        self.assertEqual(point.type, self.point_dict['type'])

    def test_multiPoint_all_vars_set(self):
        multi_point = MultiPoint(**self.multiPoint_dict)

        self.assertEqual(multi_point.type, self.multiPoint_dict['type'])
        self.assertEqual(multi_point.coordinates, self.multiPoint_dict['coordinates'])

    def test_lineString_all_vars_set(self):
        line_string = LineString(**self.lineString_dict)

        self.assertEqual(line_string.type, self.lineString_dict['type'])
        self.assertEqual(line_string.coordinates, self.lineString_dict['coordinates'])

    def test_multiLineString_all_vars_set(self):
        multi_line_string = MultiLineString(**self.multiLineString_dict)

        self.assertEqual(multi_line_string.type, self.multiLineString_dict['type'])
        self.assertEqual(multi_line_string.coordinates, self.multiLineString_dict['coordinates'])

    def test_polygon_all_vars_set(self):
        polygon = Polygon(**self.polygon_dict)

        self.assertEqual(polygon.type, self.polygon_dict['type'])
        self.assertEqual(polygon.coordinates, self.polygon_dict['coordinates'])

    def test_multiPolygon_all_vars_set(self):
        multi_polygon = MultiPolygon(**self.multiPolygon_dict)

        self.assertEqual(multi_polygon.type, self.multiPolygon_dict['type'])
        self.assertEqual(multi_polygon.coordinates, self.multiPolygon_dict['coordinates'])

    def test_instruments_all_vars_set(self):
        instruments = Instruments(**self.instruments_dict)

        self.assertEqual(instruments.instrumentIdentifier, self.instruments_dict['instrumentIdentifier'])
        self.assertEqual(instruments.instrumentType, self.instruments_dict['instrumentType'])
        self.assertEqual(instruments.instrumentDescription, self.instruments_dict['instrumentDescription'])

    def test_operation_all_vars_set(self):
        operation = Operation(**self.operation_dict)

        self.assertEqual(operation.operationDescription, self.operation_dict['operationDescription'])
        self.assertEqual(operation.operationIdentifier, self.operation_dict['operationIdentifier'])
        self.assertEqual(operation.operationStatus, self.operation_dict['operationStatus'])
        self.assertEqual(operation.operationType, self.operation_dict['operationType'])

    def test_platform_all_vars_set(self):
        platform = Platform(**self.platform_dict)

        self.assertEqual(platform.platformIdentifier, self.platform_dict['platformIdentifier'])
        self.assertEqual(platform.platformDescription, self.platform_dict['platformDescription'])
        self.assertEqual(platform.platformSponsor, self.platform_dict['platformSponsor'])

    def test_dateFormat_all_vars_set(self):
        dateformat = DataFormat(**self.dateFormat_dict)

        self.assertEqual(dateformat.name, self.dateFormat_dict['name'])
        self.assertEqual(dateformat.version, self.dateFormat_dict['version'])

    def test_link_all_vars_set(self):
        link = Link(**self.link_dict)

        self.assertEqual(link.linkName, self.link_dict['linkName'])
        self.assertEqual(link.linkProtocol, self.link_dict['linkProtocol'])
        self.assertEqual(link.linkUrl, self.link_dict['linkUrl'])
        self.assertEqual(link.linkDescription, self.link_dict['linkDescription'])
        self.assertEqual(link.linkFunction, self.link_dict['linkFunction'])

    def test_responsibleParty_all_vars_set(self):
        responsibleParty = ResponsibleParty(**self.responsibleParty_dict)

        self.assertEqual(responsibleParty.individualName, self.responsibleParty_dict['individualName'])
        self.assertEqual(responsibleParty.organizationName, self.responsibleParty_dict['organizationName'])
        self.assertEqual(responsibleParty.positionName, self.responsibleParty_dict['positionName'])
        self.assertEqual(responsibleParty.role, self.responsibleParty_dict['role'])
        self.assertEqual(responsibleParty.email, self.responsibleParty_dict['email'])
        self.assertEqual(responsibleParty.phone, self.responsibleParty_dict['phone'])

    def test_reference_all_vars_set(self):
        reference = Reference(**self.reference_dict)

        self.assertEqual(reference.title, self.reference_dict['title'])
        self.assertEqual(reference.date, self.reference_dict['date'])
        self.assertEqual(reference.links[0].linkName, self.reference_dict['links'][0]['linkName'])
        self.assertEqual(reference.links[0].linkProtocol, self.reference_dict['links'][0]['linkProtocol'])
        self.assertEqual(reference.links[0].linkUrl, self.reference_dict['links'][0]['linkUrl'])
        self.assertEqual(reference.links[0].linkDescription, self.reference_dict['links'][0]['linkDescription'])
        self.assertEqual(reference.links[0].linkFunction, self.reference_dict['links'][0]['linkFunction'])

    def test_analysis_all_vars_set(self):
        analysis = Analysis(**self.analysis_dict)

        self.assertEqual(analysis.identification, IdentificationAnalysis(**self.identificationAnalysis_dict))

    def test_fileLocation_all_vars_set(self):
        fileLocations = FileLocation(**self.fileLocation_dict)

        self.assertEqual(fileLocations.uri, self.fileLocation_dict['uri'])
        self.assertEqual(fileLocations.type, self.fileLocation_dict['type'])
        self.assertEqual(fileLocations.deleted, self.fileLocation_dict['deleted'])
        self.assertEqual(fileLocations.restricted, self.fileLocation_dict['restricted'])
        self.assertEqual(fileLocations.asynchronous, self.fileLocation_dict['asynchronous'])
        self.assertEqual(fileLocations.locality, self.fileLocation_dict['locality'])
        self.assertEqual(fileLocations.lastModified, self.fileLocation_dict['lastModified'])
        self.assertEqual(fileLocations.serviceType, self.fileLocation_dict['serviceType'])
        self.assertEqual(fileLocations.optionalAttributes, self.fileLocation_dict['optionalAttributes'])

    def test_relationships_all_vars_set(self):
        relationship = Relationship(**self.relationship_dict)

        self.assertEqual(relationship.id, self.relationship_dict['id'])
        self.assertEqual(relationship.type, self.relationship_dict['type'])

    def test_relationships_optionals(self):
        id = '12'
        relationship = Relationship(id=id, type=None)

        self.assertEqual(relationship.id, id)
