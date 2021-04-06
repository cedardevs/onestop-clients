from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Relationship
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import \
    RelationshipTypeFactory


class RelationshipFactory(Factory):
    class Meta:
        model = Relationship
    type = lazy_attribute(lambda x: [RelationshipTypeFactory(), None][randint(0, 1)])
    id = lazy_attribute(lambda x: fake.pystr())
