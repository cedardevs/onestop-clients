from random import randint

from factory import Factory, lazy_attribute

from psiSchemaClasses.org.cedar.schemas.avro.psi import ResponsibleParty
from psiSchemaClasses_test import fake


class ResponsiblePartyFactory(Factory):
    class Meta:
        model = ResponsibleParty
    individualName = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    organizationName = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    positionName = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    role = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    email = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
    phone = lazy_attribute(lambda x: [fake.pystr(), None][randint(0, 1)])
