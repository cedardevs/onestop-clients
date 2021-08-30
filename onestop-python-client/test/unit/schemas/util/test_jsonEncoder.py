import json
import unittest

from onestop.schemas.util.jsonEncoder import EnumEncoder, as_enum
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship_type import RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.record_type import RecordType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.valid_descriptor import ValidDescriptor
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.operation_type import OperationType
from onestop.schemas.psiSchemaClasses.time_range_descriptor import TimeRangeDescriptor
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location_type import FileLocationType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.method import Method
from onestop.schemas.geojsonSchemaClasses.line_string_type import LineStringType
from onestop.schemas.geojsonSchemaClasses.multi_line_string_type import MultiLineStringType
from onestop.schemas.geojsonSchemaClasses.multi_point_type import MultiPointType
from onestop.schemas.geojsonSchemaClasses.multi_polygon_type import MultiPolygonType
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.geojsonSchemaClasses.polygon_type import PolygonType

class jsonEncoderTest(unittest.TestCase):

    def test_checksumalgorithm_enum_class_encodes(self):
        type = ChecksumAlgorithm.MD5
        obj = ChecksumAlgorithm(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_checksumalgorithm_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"ChecksumAlgorithm.MD5\"}}"
        json.loads(content, object_hook=as_enum)

    def test_relationshiptype_enum_class_encodes(self):
        type = RelationshipType.COLLECTION
        obj = RelationshipType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)
        print("jsonStr:%s"%jsonStr)
        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_relationshiptype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"RelationshipType.COLLECTION\"}}"
        json.loads(content, object_hook=as_enum)

    def test_recordtype_enum_class_encodes(self):
        type = RecordType.GRANULE
        obj = RecordType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_recordtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"RecordType.COLLECTION\"}}"
        json.loads(content, object_hook=as_enum)

    def test_timerangedescriptor_enum_class_encodes(self):
        type = TimeRangeDescriptor.AMBIGUOUS
        obj = TimeRangeDescriptor(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_timerangedescriptor_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"TimeRangeDescriptor.AMBIGUOUS\"}}"
        json.loads(content, object_hook=as_enum)

    def test_linestringtype_enum_class_encodes(self):
        type = LineStringType.LINESTRING
        obj = LineStringType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_linestringtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"LineStringType.LINESTRING\"}}"
        json.loads(content, object_hook=as_enum)

    def test_method_enum_class_encodes(self):
        type = Method.CONNECT
        obj = Method(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_method_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"Method.POST\"}}"
        json.loads(content, object_hook=as_enum)

    def test_multilinestringtype_enum_class_encodes(self):
        type = MultiLineStringType.MULTILINESTRING
        obj = MultiLineStringType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_mutilinestringtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"MultiLineStringType.MULTILINESTRING\"}}"
        json.loads(content, object_hook=as_enum)

    def test_multipointtype_enum_class_encodes(self):
        type = MultiPointType.MULTIPOINT
        obj = MultiPointType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_multipointtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"MultiPointType.MULTIPOINT\"}}"
        json.loads(content, object_hook=as_enum)

    def test_multipolygontype_enum_class_encodes(self):
        type = MultiPolygonType.MULTIPOLYGON
        obj = MultiPolygonType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_multipolygontype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"MultiPolygonType.MULTIPOLYGON\"}}"
        json.loads(content, object_hook=as_enum)

    def test_operationtype_enum_class_encodes(self):
        type = OperationType.ADD
        obj = OperationType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_operationtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"OperationType.ADD\"}}"
        json.loads(content, object_hook=as_enum)

    def test_pointtype_enum_class_encodes(self):
        type = PointType.POINT
        obj = PointType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_pointtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"PointType.POINT\"}}"
        json.loads(content, object_hook=as_enum)

    def test_polygontype_enum_class_encodes(self):
        type = PolygonType.POLYGON
        obj = PolygonType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_polygontype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"PolygonType.POLYGON\"}}"
        json.loads(content, object_hook=as_enum)

    def test_filelocationtype_enum_class_encodes(self):
        type = FileLocationType.INGEST
        obj = FileLocationType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_filelocationtype_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"FileLocationType.INGEST\"}}"
        json.loads(content, object_hook=as_enum)

    def test_validdescriptor_enum_class_encodes(self):
        type = ValidDescriptor.INVALID
        obj = ValidDescriptor(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "%s"}'%type)

    def test_validdescriptor_json_decode_enum(self):
        content = "{\"type\": {\"__enum__\": \"ValidDescriptor.VALID\"}}"
        json.loads(content, object_hook=as_enum)
