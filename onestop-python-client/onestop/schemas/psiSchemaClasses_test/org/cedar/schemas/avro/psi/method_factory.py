from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Method


class MethodFactory(Factory):
    class Meta:
        model = Method

        pass
