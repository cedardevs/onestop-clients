from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import TemporalBounding
from psiSchemaClasses_test import fake


class TemporalBoundingFactory(Factory):
    class Meta:
        model = TemporalBounding
    beginDate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    beginIndeterminate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    endDate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    endIndeterminate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instant = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instantIndeterminate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    description = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
