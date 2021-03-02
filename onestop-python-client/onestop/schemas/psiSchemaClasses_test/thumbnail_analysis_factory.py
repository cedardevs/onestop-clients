from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses. import ThumbnailAnalysis
from psiSchemaClasses_test import fake


class ThumbnailAnalysisFactory(Factory):
    class Meta:
        model = ThumbnailAnalysis
    thumbnailExists = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
