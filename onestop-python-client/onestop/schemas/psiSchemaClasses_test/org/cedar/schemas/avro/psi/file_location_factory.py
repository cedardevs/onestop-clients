from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import FileLocation
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import \
    FileLocationTypeFactory


class FileLocationFactory(Factory):
    class Meta:
        model = FileLocation
    uri = lazy_attribute(lambda x: fake.pystr())
    type = lazy_attribute(lambda x: [FileLocationTypeFactory(), None][randint(0, 1)])
    deleted = lazy_attribute(lambda x: fake.pybool())
    restricted = lazy_attribute(lambda x: fake.pybool())
    asynchronous = lazy_attribute(lambda x: fake.pybool())
    locality = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    lastModified = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    serviceType = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    optionalAttributes = lazy_attribute(lambda x: {fake.pystr(): fake.pystr() for _ in range(randint(3, 10))})
