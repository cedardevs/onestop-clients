import json

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship_type import RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.record_type import RecordType
from onestop.schemas.psiSchemaClasses.time_range_descriptor import TimeRangeDescriptor
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location_type import FileLocationType
from onestop.schemas.geojsonSchemaClasses.line_string_type import LineStringType
from onestop.schemas.geojsonSchemaClasses.multi_line_string_type import MultiLineStringType
from onestop.schemas.geojsonSchemaClasses.multi_point_type import MultiPointType
from onestop.schemas.geojsonSchemaClasses.multi_polygon_type import MultiPolygonType
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.geojsonSchemaClasses.polygon_type import PolygonType

# Diction of all the Enum Classes
ENUMS = {
    'ChecksumAlgorithm': ChecksumAlgorithm,
    'RELATIONSHIPTYPE': RelationshipType,
    'RecordType': RecordType,
    'TimeRangeDescriptor': TimeRangeDescriptor,
    'LineStringType': LineStringType,
    'MultiLineStringType': MultiLineStringType,
    'MultiPointType': MultiPointType,
    'MultiPolygonType': MultiPolygonType,
    'PointType': PointType,
    'PolygonType': PolygonType,
    'FileLocationType': FileLocationType
}

# Used as an argument in json.dumps, transform Enum instance for later use
# Use this with as_enum
class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in ENUMS.values():
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)

# Used as an argument in json.dumps, returns the actual value of that enum
class EnumEncoderValue(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in ENUMS.values():
            return str(obj.value)
        return json.JSONEncoder.default(self, str)

def as_value(d):
    if type(obj) in ENUMS.values():
        return obj.value
    else:
        return d

# Used in json.loads in object hook field, locates enum instances and produces that specific enum
# Use this with EnumEncoder
def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(ENUMS[name], member)
    else:
        return d