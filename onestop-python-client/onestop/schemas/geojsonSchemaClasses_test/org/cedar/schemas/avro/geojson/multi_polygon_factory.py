from random import randint

from factory import Factory, lazy_attribute

from onestop.schemaTest2.org.cedar.schemas.avro.geojson import MultiPolygon
from onestop.schemaTest2_test import fake
from onestop.schemaTest2_test.multi_polygon_type_factory import MultiPolygonTypeFactory


class MultiPolygonFactory(Factory):
    class Meta:
        model = MultiPolygon
    type = lazy_attribute(lambda x: MultiPolygonTypeFactory())
    coordinates = lazy_attribute(lambda x: [[[[[[[fake.pyfloat() for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))])
