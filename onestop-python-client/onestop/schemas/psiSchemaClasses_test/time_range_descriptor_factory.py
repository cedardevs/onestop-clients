from factory import Factory, lazy_attribute

from psiSchemaClasses. import TimeRangeDescriptor
from psiSchemaClasses_test import fake


class TimeRangeDescriptorFactory(Factory):
    class Meta:
        model = TimeRangeDescriptor
    value = lazy_attribute(lambda x: fake.enum_with_schema(TimeRangeDescriptor))
