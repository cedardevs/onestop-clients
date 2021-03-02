from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.geojson import Point


class PointFactory(Factory):
    class Meta:
        model = Point

        pass
