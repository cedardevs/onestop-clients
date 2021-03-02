from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import SpatialBoundingAnalysis
from psiSchemaClasses_test import fake


class SpatialBoundingAnalysisFactory(Factory):
    class Meta:
        model = SpatialBoundingAnalysis
    spatialBoundingExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    isValid = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    validationError = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
