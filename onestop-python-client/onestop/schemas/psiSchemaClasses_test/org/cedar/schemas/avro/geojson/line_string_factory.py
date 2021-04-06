from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.geojson import LineString


class LineStringFactory(Factory):
    class Meta:
        model = LineString

        pass
