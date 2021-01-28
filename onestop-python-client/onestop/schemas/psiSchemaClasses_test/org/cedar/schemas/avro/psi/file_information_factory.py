from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import FileInformation
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import ChecksumFactory


class FileInformationFactory(Factory):
    class Meta:
        model = FileInformation
    name = lazy_attribute(lambda x: fake.pystr())
    size = lazy_attribute(lambda x: fake.pyint())
    checksums = lazy_attribute(lambda x: [ChecksumFactory() for _ in range(randint(1, 5))])
    format = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    headers = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    optionalAttributes = lazy_attribute(lambda x: {fake.pystr(): fake.pystr() for _ in range(randint(3, 10))})
