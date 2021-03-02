from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import Operation
from psiSchemaClasses_test import fake


class OperationFactory(Factory):
    class Meta:
        model = Operation
    operationDescription = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    operationIdentifier = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    operationStatus = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    operationType = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
