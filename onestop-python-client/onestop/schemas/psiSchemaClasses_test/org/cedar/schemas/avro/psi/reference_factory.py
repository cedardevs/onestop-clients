from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Reference
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import LinkFactory


class ReferenceFactory(Factory):
    class Meta:
        model = Reference
    title = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    date = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    links = lazy_attribute(lambda x: [LinkFactory() for _ in range(randint(1, 5))])
