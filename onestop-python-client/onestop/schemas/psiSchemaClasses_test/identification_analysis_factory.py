from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import IdentificationAnalysis
from psiSchemaClasses_test import fake


class IdentificationAnalysisFactory(Factory):
    class Meta:
        model = IdentificationAnalysis
    fileIdentifierExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    fileIdentifierString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    doiExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    doiString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    parentIdentifierExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    parentIdentifierString = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    hierarchyLevelNameExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    isGranule = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
