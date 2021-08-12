from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import Service
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import (
    LinkFactory, ResponsiblePartyFactory)


class ServiceFactory(Factory):
    class Meta:
        model = Service
    title = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    alternateTitle = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    description = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    date = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    dateType = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    pointOfContact = lazy_attribute(lambda x: [ResponsiblePartyFactory(), None][randint(0, 1)])
    operations = lazy_attribute(lambda x: [LinkFactory() for _ in range(randint(1, 5))])
