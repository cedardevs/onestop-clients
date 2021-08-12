from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import AggregatedInput
from psiSchemaClasses_test import fake
from psiSchemaClasses_test.org.cedar.schemas.avro.psi import (
    ErrorEventFactory, FileInformationFactory, FileLocationFactory,
    InputEventFactory, PublishingFactory, RecordTypeFactory,
    RelationshipFactory)


class AggregatedInputFactory(Factory):
    class Meta:
        model = AggregatedInput
    rawJson = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    rawXml = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    initialSource = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    type = lazy_attribute(lambda x: [RecordTypeFactory(), None][randint(0, 1)])
    fileInformation = lazy_attribute(lambda x: [FileInformationFactory(), None][randint(0, 1)])
    fileLocations = lazy_attribute(lambda x: {fake.pystr(): FileLocationFactory() for _ in range(randint(3, 10))})
    publishing = lazy_attribute(lambda x: [PublishingFactory(), None][randint(0, 1)])
    relationships = lazy_attribute(lambda x: [RelationshipFactory() for _ in range(randint(1, 5))])
    deleted = lazy_attribute(lambda x: fake.pybool())
    events = lazy_attribute(lambda x: [InputEventFactory() for _ in range(randint(1, 5))])
    errors = lazy_attribute(lambda x: [ErrorEventFactory() for _ in range(randint(1, 5))])
