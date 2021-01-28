from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional, Union

from undictify import type_checked_constructor

from onestop.schemas.psiSchemaClasses import KeywordsElement,Instruments,Operation, Platform, DataFormat, Service


from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.line_string import LineString
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.multi_line_string import MultiLineString
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.multi_point import MultiPoint
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.multi_polygon import MultiPolygon
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.point import Point
from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.polygon import Polygon

from .link import Link
from .reference import Reference
from .responsible_party import ResponsibleParty
from .temporal_bounding import TemporalBounding



@type_checked_constructor()
@dataclass
class Discovery:
    """
    The shape of the discovery object generated within Inventory Manager for a successfully parsed metadata document. This is the internal metadata format used within the system and ultimately sent downstream to OneStop.
    """
    fileIdentifier: Optional[str]
    parentIdentifier: Optional[str]
    hierarchyLevelName: Optional[str]
    doi: Optional[str]
    purpose: Optional[str]
    status: Optional[str]
    credit: Optional[str]
    title: Optional[str]
    alternateTitle: Optional[str]
    description: Optional[str]
    keywords: Optional[List[KeywordsElement]]
    topicCategories: Optional[List[str]]
    temporalBounding: Optional[TemporalBounding]
    spatialBounding: Union[None, Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon]
    isGlobal: Optional[bool]
    acquisitionInstruments: Optional[List[Instruments]]
    acquisitionOperations: Optional[List[Operation]]
    acquisitionPlatforms: Optional[List[Platform]]
    dataFormats: Optional[List[DataFormat]]
    links: List[Link]
    responsibleParties: Optional[List[ResponsibleParty]]
    thumbnail: Optional[str]
    thumbnailDescription: Optional[str]
    creationDate: Optional[str]
    revisionDate: Optional[str]
    publicationDate: Optional[str]
    citeAsStatements: Optional[List[str]]
    crossReferences: Optional[List[Reference]]
    largerWorks: Optional[List[Reference]]
    useLimitation: Optional[str]
    legalConstraints: Optional[List[str]]
    accessFeeStatement: Optional[str]
    orderingInstructions: Optional[str]
    edition: Optional[str]
    dsmmAccessibility: Optional[int]
    dsmmDataIntegrity: Optional[int]
    dsmmDataQualityAssessment: Optional[int]
    dsmmDataQualityAssurance: Optional[int]
    dsmmDataQualityControlMonitoring: Optional[int]
    dsmmPreservability: Optional[int]
    dsmmProductionSustainability: Optional[int]
    dsmmTransparencyTraceability: Optional[int]
    dsmmUsability: Optional[int]

    #: Calculated mean average of individual DSMM scores for Accessibility, Data Integrity, Data Quality Assessment, Data Quality Assurance, Data Quality Control Monitoring, Preservability, Production Sustainability, Transparency Traceability, and Usability.
    dsmmAverage: Optional[float]
    updateFrequency: Optional[str]
    presentationForm: Optional[str]

    #: List of objects that represent an SV_ServiceIdentification section, if any, of ISO 19115 XML metadata document. Empty if not present.
    services: Optional[List[Service]]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "Discovery",
        "doc": "The shape of the discovery object generated within Inventory Manager for a successfully parsed metadata document. This is the internal metadata format used within the system and ultimately sent downstream to OneStop.",
        "fields": [
            {
                "name": "fileIdentifier",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "parentIdentifier",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "hierarchyLevelName",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "doi",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "purpose",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "status",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "credit",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "title",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "alternateTitle",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "description",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "keywords",
                "type": {
                    "type": "array",
                    "items": {
                        "name": "KeywordsElement",
                        "type": "record",
                        "fields": [
                            {
                                "name": "values",
                                "type": {
                                    "type": "array",
                                    "items": "string"
                                },
                                "default": []
                            },
                            {
                                "name": "type",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "namespace",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            }
                        ]
                    }
                },
                "default": []
            },
            {
                "name": "topicCategories",
                "type": {
                    "type": "array",
                    "items": "string"
                },
                "default": []
            },
            {
                "name": "temporalBounding",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.TemporalBounding"
                ],
                "default": null
            },
            {
                "name": "spatialBounding",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.geojson.Point",
                    "org.cedar.schemas.avro.geojson.MultiPoint",
                    "org.cedar.schemas.avro.geojson.LineString",
                    "org.cedar.schemas.avro.geojson.MultiLineString",
                    "org.cedar.schemas.avro.geojson.Polygon",
                    "org.cedar.schemas.avro.geojson.MultiPolygon"
                ],
                "default": null
            },
            {
                "name": "isGlobal",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null
            },
            {
                "name": "acquisitionInstruments",
                "type": {
                    "type": "array",
                    "items": {
                        "name": "Instruments",
                        "type": "record",
                        "fields": [
                            {
                                "name": "instrumentIdentifier",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "instrumentType",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "instrumentDescription",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            }
                        ]
                    }
                },
                "default": []
            },
            {
                "name": "acquisitionOperations",
                "type": {
                    "type": "array",
                    "items": {
                        "name": "Operation",
                        "type": "record",
                        "fields": [
                            {
                                "name": "operationDescription",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "operationIdentifier",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "operationStatus",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "operationType",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            }
                        ]
                    }
                },
                "default": []
            },
            {
                "name": "acquisitionPlatforms",
                "type": {
                    "type": "array",
                    "items": {
                        "name": "Platform",
                        "type": "record",
                        "fields": [
                            {
                                "name": "platformIdentifier",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "platformDescription",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "platformSponsor",
                                "type": {
                                    "type": "array",
                                    "items": "string"
                                },
                                "default": []
                            }
                        ]
                    }
                },
                "default": []
            },
            {
                "name": "dataFormats",
                "type": {
                    "type": "array",
                    "items": {
                        "name": "DataFormat",
                        "type": "record",
                        "fields": [
                            {
                                "name": "name",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "version",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            }
                        ]
                    }
                },
                "default": []
            },
            {
                "name": "links",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.Link"
                },
                "default": []
            },
            {
                "name": "responsibleParties",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.ResponsibleParty"
                },
                "default": []
            },
            {
                "name": "thumbnail",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "thumbnailDescription",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "creationDate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "revisionDate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "publicationDate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "citeAsStatements",
                "type": {
                    "type": "array",
                    "items": "string"
                },
                "default": []
            },
            {
                "name": "crossReferences",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.Reference"
                },
                "default": []
            },
            {
                "name": "largerWorks",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.Reference"
                },
                "default": []
            },
            {
                "name": "useLimitation",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "legalConstraints",
                "type": {
                    "type": "array",
                    "items": "string"
                },
                "default": []
            },
            {
                "name": "accessFeeStatement",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "orderingInstructions",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "edition",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "dsmmAccessibility",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmDataIntegrity",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmDataQualityAssessment",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmDataQualityAssurance",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmDataQualityControlMonitoring",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmPreservability",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmProductionSustainability",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmTransparencyTraceability",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmUsability",
                "type": "int",
                "default": 0
            },
            {
                "name": "dsmmAverage",
                "type": "float",
                "default": 0.0,
                "doc": "Calculated mean average of individual DSMM scores for Accessibility, Data Integrity, Data Quality Assessment, Data Quality Assurance, Data Quality Control Monitoring, Preservability, Production Sustainability, Transparency Traceability, and Usability."
            },
            {
                "name": "updateFrequency",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "presentationForm",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "services",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "record",
                        "name": "Service",
                        "fields": [
                            {
                                "name": "title",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "alternateTitle",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "description",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "date",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "dateType",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null
                            },
                            {
                                "name": "pointOfContact",
                                "type": [
                                    "null",
                                    "org.cedar.schemas.avro.psi.ResponsibleParty"
                                ],
                                "default": null
                            },
                            {
                                "name": "operations",
                                "type": {
                                    "type": "array",
                                    "items": "org.cedar.schemas.avro.psi.Link"
                                },
                                "default": []
                            }
                        ]
                    }
                },
                "default": [],
                "doc": "List of objects that represent an SV_ServiceIdentification section, if any, of ISO 19115 XML metadata document. Empty if not present."
            }
        ]
    }"""

    def to_dict(self) -> Dict:
        """
        Returns a dictionary version of this instance.
        """
        return asdict(self)

    @classmethod
    def from_dict(
            cls,
            the_dict: Dict
    ) -> 'Discovery':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
