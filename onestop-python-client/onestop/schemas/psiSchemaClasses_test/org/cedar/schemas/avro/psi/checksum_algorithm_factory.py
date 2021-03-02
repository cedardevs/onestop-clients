from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import ChecksumAlgorithm
from psiSchemaClasses_test import fake


class ChecksumAlgorithmFactory(Factory):
    class Meta:
        model = ChecksumAlgorithm
    value = lazy_attribute(lambda x: fake.enum_with_schema(ChecksumAlgorithm))
