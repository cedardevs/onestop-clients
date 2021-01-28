from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.geojson import Polygon


class PolygonFactory(Factory):
    class Meta:
        model = Polygon

        pass
