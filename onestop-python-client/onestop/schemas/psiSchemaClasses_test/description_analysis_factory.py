from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import DescriptionAnalysis
from psiSchemaClasses_test import fake


class DescriptionAnalysisFactory(Factory):
    class Meta:
        model = DescriptionAnalysis
    descriptionExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    descriptionCharacters = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    descriptionFleschReadingEaseScore = lazy_attribute(lambda x: [fake.pyfloat(), None][randint(0, 1)])
    descriptionFleschKincaidReadingGradeLevel = lazy_attribute(lambda x: [fake.pyfloat(), None][randint(0, 1)])
