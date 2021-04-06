from pyavro_gen.codewriters.namespace import ClassItem

test_classes = [
    ClassItem('schemaTest2.org.cedar.schemas.avro.geojson', 'LineString', 'schemaTest2_test.org.cedar.schemas.avro.geojson', 'LineStringFactory'),
    ClassItem('schemaTest2.org.cedar.schemas.avro.geojson', 'Polygon', 'schemaTest2_test.org.cedar.schemas.avro.geojson', 'PolygonFactory'),
    ClassItem('schemaTest2.org.cedar.schemas.avro.geojson', 'MultiLineString', 'schemaTest2_test.org.cedar.schemas.avro.geojson', 'MultiLineStringFactory'),
    ClassItem('schemaTest2.org.cedar.schemas.avro.geojson', 'Point', 'schemaTest2_test.org.cedar.schemas.avro.geojson', 'PointFactory'),
    ClassItem('schemaTest2.org.cedar.schemas.avro.geojson', 'MultiPoint', 'schemaTest2_test.org.cedar.schemas.avro.geojson', 'MultiPointFactory'),
    ClassItem('schemaTest2.org.cedar.schemas.avro.geojson', 'MultiPolygon', 'schemaTest2_test.org.cedar.schemas.avro.geojson', 'MultiPolygonFactory'),
    ClassItem('schemaTest2.', 'LineStringType', 'schemaTest2_test.', 'LineStringTypeFactory'),
    ClassItem('schemaTest2.', 'PolygonType', 'schemaTest2_test.', 'PolygonTypeFactory'),
    ClassItem('schemaTest2.', 'MultiLineStringType', 'schemaTest2_test.', 'MultiLineStringTypeFactory'),
    ClassItem('schemaTest2.', 'PointType', 'schemaTest2_test.', 'PointTypeFactory'),
    ClassItem('schemaTest2.', 'MultiPointType', 'schemaTest2_test.', 'MultiPointTypeFactory'),
    ClassItem('schemaTest2.', 'MultiPolygonType', 'schemaTest2_test.', 'MultiPolygonTypeFactory'),
]
