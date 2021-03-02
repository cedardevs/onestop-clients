from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import ParsedRecordWithId
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import \
    ParsedRecordFactory


class ParsedRecordWithIdFactory(Factory):
    class Meta:
        model = ParsedRecordWithId
    id = lazy_attribute(lambda x: fake.pystr())
    record = lazy_attribute(lambda x: ParsedRecordFactory())
