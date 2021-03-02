from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import RelationshipType


class RelationshipTypeFactory(Factory):
    class Meta:
        model = RelationshipType

        pass
