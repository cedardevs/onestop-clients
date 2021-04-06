from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import FileLocationType


class FileLocationTypeFactory(Factory):
    class Meta:
        model = FileLocationType

        pass
