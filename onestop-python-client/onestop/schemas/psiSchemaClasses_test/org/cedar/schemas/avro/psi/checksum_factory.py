from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Checksum
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import \
    ChecksumAlgorithmFactory


class ChecksumFactory(Factory):
    class Meta:
        model = Checksum
    algorithm = lazy_attribute(lambda x: ChecksumAlgorithmFactory())
    value = lazy_attribute(lambda x: fake.pystr())
