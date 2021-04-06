from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import ValidDescriptor


class ValidDescriptorFactory(Factory):
    class Meta:
        model = ValidDescriptor

        pass
