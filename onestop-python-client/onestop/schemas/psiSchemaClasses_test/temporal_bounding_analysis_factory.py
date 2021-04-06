from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import TemporalBoundingAnalysis
from psiSchemaClasses_test import fake
from psiSchemaClasses_test. import TimeRangeDescriptorFactory
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import \
    ValidDescriptorFactory


class TemporalBoundingAnalysisFactory(Factory):
    class Meta:
        model = TemporalBoundingAnalysis
    beginDescriptor = lazy_attribute(lambda x: [ValidDescriptorFactory(), None][randint(0, 1)])
    beginPrecision = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    beginIndexable = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    beginZoneSpecified = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    beginUtcDateTimeString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    beginYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    beginDayOfYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    beginDayOfMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    beginMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    endDescriptor = lazy_attribute(lambda x: [ValidDescriptorFactory(), None][randint(0, 1)])
    endPrecision = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    endIndexable = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    endZoneSpecified = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    endUtcDateTimeString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    endYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    endDayOfYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    endDayOfMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    endMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantDescriptor = lazy_attribute(lambda x: [ValidDescriptorFactory(), None][randint(0, 1)])
    instantPrecision = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instantIndexable = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    instantZoneSpecified = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instantUtcDateTimeString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instantEndUtcDateTimeString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    instantYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantDayOfYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantEndDayOfYear = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantDayOfMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantEndDayOfMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    instantEndMonth = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    rangeDescriptor = lazy_attribute(lambda x: [TimeRangeDescriptorFactory(), None][randint(0, 1)])
