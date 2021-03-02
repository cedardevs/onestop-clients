from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import KeywordsElement
from psiSchemaClasses_test import fake


class KeywordsElementFactory(Factory):
    class Meta:
        model = KeywordsElement
    values = lazy_attribute(lambda x: [fake.pystr() for _ in range(randint(1, 5))])
    type = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    namespace = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
