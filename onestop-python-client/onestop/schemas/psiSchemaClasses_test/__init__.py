import faker

from pyavro_gen.enum_with_schema_provider import EnumWithSchemaProvider
from .testing_classes import test_classes

fake = faker.Faker()
fake.add_provider(EnumWithSchemaProvider)
