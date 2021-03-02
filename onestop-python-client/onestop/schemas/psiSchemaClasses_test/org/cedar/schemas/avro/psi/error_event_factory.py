from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import ErrorEvent
from psiSchemaClasses_test import fake


class ErrorEventFactory(Factory):
    class Meta:
        model = ErrorEvent
    title = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    detail = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    status = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    code = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    source = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
