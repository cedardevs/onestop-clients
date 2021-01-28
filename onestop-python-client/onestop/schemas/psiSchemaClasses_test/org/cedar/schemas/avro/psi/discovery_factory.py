from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import Discovery
from psiSchemaClasses_test import fake
from psiSchemaClasses_test. import (DataFormatFactory, InstrumentsFactory,
                                    KeywordsElementFactory, OperationFactory,
                                    PlatformFactory, ServiceFactory)
from psiSchemaClasses_test.org.cedar.schemas.avro.geojson import (
    LineStringFactory, MultiLineStringFactory, MultiPointFactory,
    MultiPolygonFactory, PointFactory, PolygonFactory)
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import (
    LinkFactory, ReferenceFactory, ResponsiblePartyFactory,
    TemporalBoundingFactory)


class DiscoveryFactory(Factory):
    class Meta:
        model = Discovery
    fileIdentifier = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    parentIdentifier = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    hierarchyLevelName = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    doi = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    purpose = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    status = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    credit = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    title = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    alternateTitle = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    description = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    keywords = lazy_attribute(lambda x: [KeywordsElementFactory() for _ in range(randint(1, 5))])
    topicCategories = lazy_attribute(lambda x: [fake.pystr() for _ in range(randint(1, 5))])
    temporalBounding = lazy_attribute(lambda x: [TemporalBoundingFactory(), None][randint(0, 1)])
    spatialBounding = lazy_attribute(lambda x: [None, PointFactory(), MultiPointFactory(), LineStringFactory(), MultiLineStringFactory(), PolygonFactory(), MultiPolygonFactory()][randint(0, 6)])
    isGlobal = lazy_attribute(lambda x: [fake.pybool(), None][randint(0, 1)])
    acquisitionInstruments = lazy_attribute(lambda x: [InstrumentsFactory() for _ in range(randint(1, 5))])
    acquisitionOperations = lazy_attribute(lambda x: [OperationFactory() for _ in range(randint(1, 5))])
    acquisitionPlatforms = lazy_attribute(lambda x: [PlatformFactory() for _ in range(randint(1, 5))])
    dataFormats = lazy_attribute(lambda x: [DataFormatFactory() for _ in range(randint(1, 5))])
    links = lazy_attribute(lambda x: [LinkFactory() for _ in range(randint(1, 5))])
    responsibleParties = lazy_attribute(lambda x: [ResponsiblePartyFactory() for _ in range(randint(1, 5))])
    thumbnail = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    thumbnailDescription = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    creationDate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    revisionDate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    publicationDate = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    citeAsStatements = lazy_attribute(lambda x: [fake.pystr() for _ in range(randint(1, 5))])
    crossReferences = lazy_attribute(lambda x: [ReferenceFactory() for _ in range(randint(1, 5))])
    largerWorks = lazy_attribute(lambda x: [ReferenceFactory() for _ in range(randint(1, 5))])
    useLimitation = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    legalConstraints = lazy_attribute(lambda x: [fake.pystr() for _ in range(randint(1, 5))])
    accessFeeStatement = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    orderingInstructions = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    edition = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    dsmmAccessibility = lazy_attribute(lambda x: fake.pyint())
    dsmmDataIntegrity = lazy_attribute(lambda x: fake.pyint())
    dsmmDataQualityAssessment = lazy_attribute(lambda x: fake.pyint())
    dsmmDataQualityAssurance = lazy_attribute(lambda x: fake.pyint())
    dsmmDataQualityControlMonitoring = lazy_attribute(lambda x: fake.pyint())
    dsmmPreservability = lazy_attribute(lambda x: fake.pyint())
    dsmmProductionSustainability = lazy_attribute(lambda x: fake.pyint())
    dsmmTransparencyTraceability = lazy_attribute(lambda x: fake.pyint())
    dsmmUsability = lazy_attribute(lambda x: fake.pyint())
    dsmmAverage = lazy_attribute(lambda x: fake.pyfloat())
    updateFrequency = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    presentationForm = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    services = lazy_attribute(lambda x: [ServiceFactory() for _ in range(randint(1, 5))])
