from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Input
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import (
    MethodFactory, OperationTypeFactory, RecordTypeFactory)


class InputFactory(Factory):
    class Meta:
        model = Input
    type = lazy_attribute(lambda x: [RecordTypeFactory(), None][randint(0, 1)])
    content = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    contentType = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    method = lazy_attribute(lambda x: [MethodFactory(), None][randint(0, 1)])
    source = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    operation = lazy_attribute(lambda x: [OperationTypeFactory(), None][randint(0, 1)])
