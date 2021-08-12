from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import DataAccessAnalysis
from psiSchemaClasses_test import fake


class DataAccessAnalysisFactory(Factory):
    class Meta:
        model = DataAccessAnalysis
    dataAccessExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
