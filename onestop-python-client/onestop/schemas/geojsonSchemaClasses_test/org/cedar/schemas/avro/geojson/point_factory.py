from random import randint

from factory import Factory, lazy_attribute

from onestop.schemaTest2.org.cedar.schemas.avro.geojson import Point
from onestop.schemaTest2_test import fake
from onestop.schemaTest2_test.point_type_factory import PointTypeFactory


class PointFactory(Factory):
    class Meta:
        model = Point
    type = lazy_attribute(lambda x: PointTypeFactory())
    coordinates = lazy_attribute(lambda x: [fake.pyfloat() for _ in range(randint(1, 5))])
