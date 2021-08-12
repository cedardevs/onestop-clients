from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Link
from psiSchemaClasses_test import fake


class LinkFactory(Factory):
    class Meta:
        model = Link
    linkName = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    linkProtocol = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    linkUrl = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    linkDescription = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    linkFunction = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
