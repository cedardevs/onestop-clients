from random import randint

from factory import Factory, lazy_attribute

from onestop.schemaTest2.org.cedar.schemas.avro.geojson import MultiLineString
from onestop.schemaTest2_test import fake
from onestop.schemaTest2_test.multi_line_string_type_factory import MultiLineStringTypeFactory


class MultiLineStringFactory(Factory):
    class Meta:
        model = MultiLineString
    type = lazy_attribute(lambda x: MultiLineStringTypeFactory())
    coordinates = lazy_attribute(lambda x: [[[[[fake.pyfloat() for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))])
