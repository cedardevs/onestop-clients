from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.geojson import MultiPolygon


class MultiPolygonFactory(Factory):
    class Meta:
        model = MultiPolygon

        pass
