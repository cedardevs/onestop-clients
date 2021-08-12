from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import TitleAnalysis
from psiSchemaClasses_test import fake


class TitleAnalysisFactory(Factory):
    class Meta:
        model = TitleAnalysis
    titleExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    titleCharacters = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    alternateTitleExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    alternateTitleCharacters = lazy_attribute(lambda x: [fake.pyint(), None][randint(0, 1)])
    titleFleschReadingEaseScore = lazy_attribute(lambda x: [fake.pyfloat(), None][randint(0, 1)])
    alternateTitleFleschReadingEaseScore = lazy_attribute(lambda x: [fake.pyfloat(), None][randint(0, 1)])
    titleFleschKincaidReadingGradeLevel = lazy_attribute(lambda x: [fake.pyfloat(), None][randint(0, 1)])
    alternateTitleFleschKincaidReadingGradeLevel = lazy_attribute(lambda x: [fake.pyfloat(), None][randint(0, 1)])
