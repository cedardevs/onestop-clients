from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import Platform
from psiSchemaClasses_test import fake


class PlatformFactory(Factory):
    class Meta:
        model = Platform
    platformIdentifier = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    platformDescription = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    platformSponsor = lazy_attribute(lambda x: [fake.pystr() for _ in range(randint(1, 5))])
