from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import RecordType
from psiSchemaClasses_test import fake


class RecordTypeFactory(Factory):
    class Meta:
        model = RecordType
    value = lazy_attribute(lambda x: fake.enum_with_schema(RecordType))
