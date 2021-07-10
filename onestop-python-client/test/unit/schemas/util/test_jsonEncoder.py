import json
import unittest

from onestop.schemas.util.jsonEncoder import EnumEncoder
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship_type import RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.record_type import RecordType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.valid_descriptor import ValidDescriptor
from onestop.schemas.psiSchemaClasses.time_range_descriptor import TimeRangeDescriptor
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location_type import FileLocationType
from onestop.schemas.geojsonSchemaClasses.line_string_type import LineStringType
from onestop.schemas.geojsonSchemaClasses.multi_line_string_type import MultiLineStringType
from onestop.schemas.geojsonSchemaClasses.multi_point_type import MultiPointType
from onestop.schemas.geojsonSchemaClasses.multi_polygon_type import MultiPolygonType
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.geojsonSchemaClasses.polygon_type import PolygonType

class jsonEncoderTest(unittest.TestCase):

    def test_checksumalgorithm_enum_class_encodes(self):
        type = ChecksumAlgorithm.MD5.value
        obj = ChecksumAlgorithm(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "ChecksumAlgorithm.%s"}'%type)

    def test_relationshiptype_enum_class_encodes(self):
        type = RelationshipType.collection.value
        obj = RelationshipType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "RelationshipType.%s"}'%type.lower())

    def test_recordtype_enum_class_encodes(self):
        type = RecordType.granule.value
        obj = RecordType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "RecordType.%s"}'%type.lower())

    def test_timerangedescriptor_enum_class_encodes(self):
        type = TimeRangeDescriptor.AMBIGUOUS.value
        obj = TimeRangeDescriptor(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "TimeRangeDescriptor.%s"}'%type)

    def test_linestring_enum_class_encodes(self):
        type = LineStringType.LineString.value
        obj = LineStringType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "LineStringType.%s"}'%type)

    def test_multilinestringtype_enum_class_encodes(self):
        type = MultiLineStringType.MultiLineString.value
        obj = MultiLineStringType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "MultiLineStringType.%s"}'%type)

    def test_multipointtype_enum_class_encodes(self):
        type = MultiPointType.MultiPoint.value
        obj = MultiPointType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "MultiPointType.%s"}'%type)

    def test_multipolygontype_enum_class_encodes(self):
        type = MultiPolygonType.MultiPolygon.value
        obj = MultiPolygonType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "MultiPolygonType.%s"}'%type)

    def test_pointtype_enum_class_encodes(self):
        type = PointType.Point.value
        obj = PointType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "PointType.%s"}'%type)

    def test_polygontype_enum_class_encodes(self):
        type = PolygonType.Polygon.value
        obj = PolygonType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "PolygonType.%s"}'%type)

    def test_filelocationtype_enum_class_encodes(self):
        type = FileLocationType.INGEST.value
        obj = FileLocationType(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "FileLocationType.%s"}'%type)

    def test_validdescriptor_enum_class_encodes(self):
        type = ValidDescriptor.INVALID.value
        obj = ValidDescriptor(type)

        jsonStr = json.dumps(obj,
                             cls=EnumEncoder)

        self.assertEqual(jsonStr, '{"__enum__": "ValidDescriptor.%s"}'%type)
