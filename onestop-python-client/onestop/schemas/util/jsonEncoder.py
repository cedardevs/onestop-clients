import json

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm

# Diction of all the Enum Classes
ENUMS = {
    'ChecksumAlgorithm': ChecksumAlgorithm,

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