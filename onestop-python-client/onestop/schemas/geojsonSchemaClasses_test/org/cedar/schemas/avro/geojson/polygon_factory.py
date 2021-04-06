from random import randint

from factory import Factory, lazy_attribute

from onestop.schemaTest2.org.cedar.schemas.avro.geojson import Polygon
from onestop.schemaTest2_test import fake
from onestop.schemaTest2_test.polygon_type_factory import PolygonTypeFactory


class PolygonFactory(Factory):
    class Meta:
        model = Polygon
    type = lazy_attribute(lambda x: PolygonTypeFactory())
    coordinates = lazy_attribute(lambda x: [[[[[fake.pyfloat() for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))]][randint(0, 0)] for _ in range(randint(1, 5))])
