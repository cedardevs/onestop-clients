from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Analysis
from psiSchemaClasses_test. import (DataAccessAnalysisFactory,
                                    DescriptionAnalysisFactory,
                                    IdentificationAnalysisFactory,
                                    SpatialBoundingAnalysisFactory,
                                    TemporalBoundingAnalysisFactory,
                                    ThumbnailAnalysisFactory,
                                    TitleAnalysisFactory)


class AnalysisFactory(Factory):
    class Meta:
        model = Analysis
    identification = lazy_attribute(lambda x: [IdentificationAnalysisFactory(), None][randint(0, 1)])
    titles = lazy_attribute(lambda x: [TitleAnalysisFactory(), None][randint(0, 1)])
    description = lazy_attribute(lambda x: [DescriptionAnalysisFactory(), None][randint(0, 1)])
    dataAccess = lazy_attribute(lambda x: [DataAccessAnalysisFactory(), None][randint(0, 1)])
    thumbnail = lazy_attribute(lambda x: [ThumbnailAnalysisFactory(), None][randint(0, 1)])
    temporalBounding = lazy_attribute(lambda x: [TemporalBoundingAnalysisFactory(), None][randint(0, 1)])
    spatialBounding = lazy_attribute(lambda x: [SpatialBoundingAnalysisFactory(), None][randint(0, 1)])
