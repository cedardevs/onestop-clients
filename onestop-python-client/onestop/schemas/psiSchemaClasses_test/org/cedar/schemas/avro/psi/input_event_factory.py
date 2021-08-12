from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import InputEvent
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import (
    MethodFactory, OperationTypeFactory)


class InputEventFactory(Factory):
    class Meta:
        model = InputEvent
    timestamp = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    method = lazy_attribute(lambda x: [MethodFactory(), None][randint(0, 1)])
    source = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    operation = lazy_attribute(lambda x: [OperationTypeFactory(), None][randint(0, 1)])
    failedState = lazy_attribute(lambda x: fake.pybool())
