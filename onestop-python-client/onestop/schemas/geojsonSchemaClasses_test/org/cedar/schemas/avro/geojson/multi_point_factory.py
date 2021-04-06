from random import randint

from factory import Factory, lazy_attribute

from onestop.schemaTest2.org.cedar.schemas.avro.geojson import MultiPoint
from onestop.schemaTest2_test import fake
from onestop.schemaTest2_test.multi_point_type_factory import MultiPointTypeFactory


class MultiPointFactory(Factory):
    class Meta:
        model = MultiPoint
    type = lazy_attribute(lambda x: MultiPointTypeFactory())
    coordinates = lazy_attribute(lambda x: [[[fake.pyfloat() for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))])
