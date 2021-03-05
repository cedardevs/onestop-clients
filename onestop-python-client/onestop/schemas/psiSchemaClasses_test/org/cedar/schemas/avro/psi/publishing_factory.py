from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Publishing
from psiSchemaClasses_test import fake


class PublishingFactory(Factory):
    class Meta:
        model = Publishing
    isPrivate = lazy_attribute(lambda x: fake.pybool())
    until = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
