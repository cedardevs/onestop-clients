from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import ParsedRecord
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import (
    AnalysisFactory, DiscoveryFactory, ErrorEventFactory,
    FileInformationFactory, FileLocationFactory, PublishingFactory,
    RecordTypeFactory, RelationshipFactory)


class ParsedRecordFactory(Factory):
    class Meta:
        model = ParsedRecord
    type = lazy_attribute(lambda x: [RecordTypeFactory(), None][randint(0, 1)])
    discovery = lazy_attribute(lambda x: [DiscoveryFactory(), None][randint(0, 1)])
    analysis = lazy_attribute(lambda x: [AnalysisFactory(), None][randint(0, 1)])
    fileInformation = lazy_attribute(lambda x: [FileInformationFactory(), None][randint(0, 1)])
    fileLocations = lazy_attribute(lambda x: {fake.pystr(): FileLocationFactory() for _ in range(randint(3, 10))})
    publishing = lazy_attribute(lambda x: PublishingFactory())
    relationships = lazy_attribute(lambda x: [RelationshipFactory() for _ in range(randint(1, 5))])
    errors = lazy_attribute(lambda x: [ErrorEventFactory() for _ in range(randint(1, 5))])
