from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import Instruments
from psiSchemaClasses_test import fake


class InstrumentsFactory(Factory):
    class Meta:
        model = Instruments
    instrumentIdentifier = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instrumentType = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instrumentDescription = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
