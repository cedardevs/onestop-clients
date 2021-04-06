from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.geojson import MultiPoint


class MultiPointFactory(Factory):
    class Meta:
        model = MultiPoint

        pass
