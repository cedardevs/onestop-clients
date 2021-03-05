from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.geojson import MultiLineString


class MultiLineStringFactory(Factory):
    class Meta:
        model = MultiLineString

        pass
