from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import DataFormat
from psiSchemaClasses_test import fake


class DataFormatFactory(Factory):
    class Meta:
        model = DataFormat
    name = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    version = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
