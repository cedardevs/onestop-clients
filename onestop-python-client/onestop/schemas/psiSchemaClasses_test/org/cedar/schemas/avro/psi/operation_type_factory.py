from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import OperationType


class OperationTypeFactory(Factory):
    class Meta:
        model = OperationType

        pass
