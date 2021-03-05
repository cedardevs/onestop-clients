from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor

from onestop.schemas.psiSchemaClasses.data_access_analysis import DataAccessAnalysis
from onestop.schemas.psiSchemaClasses.description_analysis import DescriptionAnalysis
from onestop.schemas.psiSchemaClasses.identification_analysis import IdentificationAnalysis
from onestop.schemas.psiSchemaClasses.spatial_bounding_analysis import SpatialBoundingAnalysis
from onestop.schemas.psiSchemaClasses.temporal_bounding_analysis import TemporalBoundingAnalysis
from onestop.schemas.psiSchemaClasses.thumbnail_analysis import ThumbnailAnalysis
from onestop.schemas.psiSchemaClasses.title_analysis import TitleAnalysis


@type_checked_constructor()
@dataclass
class Analysis:
    """
    The shape of the analysis object generated within Inventory Manager for a successfully parsed metadata document. Content within this object is related to the quality of the content of specific metadata fields, which can be used downstream to determine whether or not a given document should be accepted into another service, such as the OneStop search platform.
    """

    #: Assessment of the identifying elements of the metadata.
    identification: Optional[IdentificationAnalysis]

    #: Assessment of the titles in the metadata.
    titles: Optional[TitleAnalysis]

    #: Assessment of the description in the metadata.
    description: Optional[DescriptionAnalysis]

    #: Assessment of the data access information in the metadata
    dataAccess: Optional[DataAccessAnalysis]

    #: An object containing analysis of the metadata's thumbnail image
    thumbnail: Optional[ThumbnailAnalysis]

    #: Assessment of the temporal bounding information in the metadata
    temporalBounding: Optional[TemporalBoundingAnalysis]

    #: Assessment of the spatial bounding information in the metadata
    spatialBounding: Optional[SpatialBoundingAnalysis]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "Analysis",
        "namespace": "org.cedar.schemas.avro.psi",
        "doc": "The shape of the analysis object generated within Inventory Manager for a successfully parsed metadata document. Content within this object is related to the quality of the content of specific metadata fields, which can be used downstream to determine whether or not a given document should be accepted into another service, such as the OneStop search platform.",
        "fields": [
            {
                "name": "identification",
                "doc": "Assessment of the identifying elements of the metadata.",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "IdentificationAnalysis",
                        "fields": [
                            {
                                "name": "fileIdentifierExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a file identifier"
                            },
                            {
                                "name": "fileIdentifierString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The value of the analyzed record's file identifier, if present"
                            },
                            {
                                "name": "doiExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a Digital Object Identifier"
                            },
                            {
                                "name": "doiString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The value of the analyzed record's Digital Object Identifier, if present"
                            },
                            {
                                "name": "parentIdentifierExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a parent identifier"
                            },
                            {
                                "name": "parentIdentifierString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The value of the analyzed record's parent identifier, if present"
                            },
                            {
                                "name": "hierarchyLevelNameExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a hierarchy level name"
                            },
                            {
                                "name": "isGranule",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Resolves to true if metadata content indicates a record is a granule. That is, a parent identifier is present and the hierarchy level name is 'granule'."
                            }
                        ]
                    }
                ],
                "default": null
            },
            {
                "name": "titles",
                "doc": "Assessment of the titles in the metadata.",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "TitleAnalysis",
                        "fields": [
                            {
                                "name": "titleExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a title"
                            },
                            {
                                "name": "titleCharacters",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "The number of characters in the analyzed record's title"
                            },
                            {
                                "name": "alternateTitleExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has an alternate title"
                            },
                            {
                                "name": "alternateTitleCharacters",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "The number of characters in the analyzed record's alternate title"
                            },
                            {
                                "name": "titleFleschReadingEaseScore",
                                "type": [
                                    "null",
                                    "double"
                                ],
                                "default": null,
                                "doc": "Flesch reading-ease score measuring the reading ease of the record's title"
                            },
                            {
                                "name": "alternateTitleFleschReadingEaseScore",
                                "type": [
                                    "null",
                                    "double"
                                ],
                                "default": null,
                                "doc": "Flesch reading-ease score measuring the reading ease of the record's alternate title"
                            },
                            {
                                "name": "titleFleschKincaidReadingGradeLevel",
                                "type": [
                                    "null",
                                    "double"
                                ],
                                "default": null,
                                "doc": "Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's title"
                            },
                            {
                                "name": "alternateTitleFleschKincaidReadingGradeLevel",
                                "type": [
                                    "null",
                                    "double"
                                ],
                                "default": null,
                                "doc": "Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's alternate title"
                            }
                        ]
                    }
                ],
                "default": null
            },
            {
                "name": "description",
                "doc": "Assessment of the description in the metadata.",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "DescriptionAnalysis",
                        "fields": [
                            {
                                "name": "descriptionExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a description"
                            },
                            {
                                "name": "descriptionCharacters",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "The number of characters in the analyzed record's description"
                            },
                            {
                                "name": "descriptionFleschReadingEaseScore",
                                "type": [
                                    "null",
                                    "double"
                                ],
                                "default": null,
                                "doc": "Flesch reading-ease score measuring the reading ease of the record's description"
                            },
                            {
                                "name": "descriptionFleschKincaidReadingGradeLevel",
                                "type": [
                                    "null",
                                    "double"
                                ],
                                "default": null,
                                "doc": "Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's description"
                            }
                        ]
                    }
                ],
                "default": null
            },
            {
                "name": "dataAccess",
                "doc": "Assessment of the data access information in the metadata",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "DataAccessAnalysis",
                        "fields": [
                            {
                                "name": "dataAccessExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record includes any data access information"
                            }
                        ]
                    }
                ],
                "default": null
            },
            {
                "name": "thumbnail",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "ThumbnailAnalysis",
                        "fields": [
                            {
                                "name": "thumbnailExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a thumbnail"
                            }
                        ]
                    }
                ],
                "default": null,
                "doc": "An object containing analysis of the metadata's thumbnail image"
            },
            {
                "name": "temporalBounding",
                "doc": "Assessment of the temporal bounding information in the metadata",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "TemporalBoundingAnalysis",
                        "fields": [
                            {
                                "name": "beginDescriptor",
                                "type": [
                                    "null",
                                    "org.cedar.schemas.avro.psi.ValidDescriptor"
                                ],
                                "default": null,
                                "doc": "Describes the state of the temporal bounding's beginning, i.e. VALID, INVALID, or UNDEFINED."
                            },
                            {
                                "name": "beginPrecision",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The precision of the beginning of the analyzed bounding, e.g. 'Years', 'Seconds', etc. See java.time.temporal.ChronoUnit. Note that this may sometimes not exactly match the input data, since it reflects the Java class the date is able to be parsed into."
                            },
                            {
                                "name": "beginIndexable",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates whether or not beginUtcDateTimeString can be indexed into Elasticsearch for searching."
                            },
                            {
                                "name": "beginZoneSpecified",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The time zone indicated for the beginning of the analyzed temporal bounding with the format (+/-)hh:mm[:ss], or Z for UTC. See java.lang.ZoneOffset."
                            },
                            {
                                "name": "beginUtcDateTimeString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "If provided begin date is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the analyzed value."
                            },
                            {
                                "name": "beginYear",
                                "type": [
                                    "null",
                                    "long"
                                ],
                                "default": null,
                                "doc": "If provided begin date is VALID, a long indicating the beginning year."
                            },
                            {
                                "name": "beginDayOfYear",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided begin date is VALID, an integer indicating the day of year for the beginning value. This may be populated by extrapolating into a DateTime. See beginPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "beginDayOfMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided begin date is VALID, an integer indicating the day of month for the beginning value. This may be populated by extrapolating into a DateTime. See beginPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "beginMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided begin date is VALID, an integer indicating the month for the beginning value. This may be populated by extrapolating into a DateTime. See beginPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "endDescriptor",
                                "type": [
                                    "null",
                                    "org.cedar.schemas.avro.psi.ValidDescriptor"
                                ],
                                "default": null,
                                "doc": "Describes the state of the temporal bounding's end, i.e. VALID, INVALID, or UNDEFINED."
                            },
                            {
                                "name": "endPrecision",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The precision of the end of the analyzed bounding, e.g. 'Years', 'Seconds', etc. See java.time.temporal.ChronoUnit. Note that this may sometimes not exactly match the input data, since it reflects the Java class the date is able to be parsed into."
                            },
                            {
                                "name": "endIndexable",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates whether or not endUtcDateTimeString can be indexed into Elasticsearch for searching."
                            },
                            {
                                "name": "endZoneSpecified",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The time zone indicated for the end of the analyzed temporal bounding with the format (+/-)hh:mm[:ss], or Z for UTC. See java.lang.ZoneOffset."
                            },
                            {
                                "name": "endUtcDateTimeString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "If provided end date is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the analyzed end value."
                            },
                            {
                                "name": "endYear",
                                "type": [
                                    "null",
                                    "long"
                                ],
                                "default": null,
                                "doc": "If provided end date is VALID, an long indicating the end year."
                            },
                            {
                                "name": "endDayOfYear",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided end date is VALID, an integer indicating the day of year for the end value. This may be populated by extrapolating into a DateTime. See endPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "endDayOfMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided end date is VALID, an integer indicating the day of month for the end value. This may be populated by extrapolating into a DateTime. See endPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "endMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided end date is VALID, an integer indicating the month for the end value. This may be populated by extrapolating into a DateTime. See endPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "instantDescriptor",
                                "type": [
                                    "null",
                                    "org.cedar.schemas.avro.psi.ValidDescriptor"
                                ],
                                "default": null,
                                "doc": "Describes the state of the temporal bounding's instant, i.e. VALID, INVALID, or UNDEFINED."
                            },
                            {
                                "name": "instantPrecision",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The precision of the instant of the analyzed bounding, e.g. 'Years', 'Seconds', etc. See java.time.temporal.ChronoUnit. Note that this may sometimes not exactly match the input data, since it reflects the Java class the date is able to be parsed into."
                            },
                            {
                                "name": "instantIndexable",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates whether or not instantUtcDateTimeString/instantEndUtcDateTimeString can be indexed into Elasticsearch for searching."
                            },
                            {
                                "name": "instantZoneSpecified",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "The time zone indicated for the instant of the analyzed temporal bounding with the format (+/-)hh:mm[:ss], or Z for UTC. See java.lang.ZoneOffset."
                            },
                            {
                                "name": "instantUtcDateTimeString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the analyzed instant value."
                            },
                            {
                                "name": "instantEndUtcDateTimeString",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the end analyzed instant value. The actual or assumed end date time based on precision of original data."
                            },
                            {
                                "name": "instantYear",
                                "type": [
                                    "null",
                                    "long"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, an long indicating the instant year."
                            },
                            {
                                "name": "instantDayOfYear",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, an integer indicating the day of year for the instant value. This may be populated by extrapolating into a DateTime. See instantPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "instantEndDayOfYear",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, an integer indicating the actual or assumed day of year the instant ends depending on the precision of the original content, e.g. the last day of a month or year."
                            },
                            {
                                "name": "instantDayOfMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, an integer indicating the day of month for the instant value. This may be populated by extrapolating into a DateTime. See instantPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "instantEndDayOfMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, an integer indicating the actual or assumed day of month the instant ends depending on precision, e.g. the last day of a month or year."
                            },
                            {
                                "name": "instantMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID, an integer indicating the month for the instant value. This may be populated by extrapolating into a DateTime. See instantPrecision for the best indicator of if this value is extrapolated or provided in the original date format."
                            },
                            {
                                "name": "instantEndMonth",
                                "type": [
                                    "null",
                                    "int"
                                ],
                                "default": null,
                                "doc": "If provided instant is VALID and instantPrecision does not include day, an integer indicating the assumed month the instant ends, e.g. the last month of the year."
                            },
                            {
                                "name": "rangeDescriptor",
                                "type": [
                                    "null",
                                    {
                                        "type": "enum",
                                        "name": "TimeRangeDescriptor",
                                        "symbols": [
                                            "AMBIGUOUS",
                                            "BACKWARDS",
                                            "BOUNDED",
                                            "INSTANT",
                                            "INVALID",
                                            "ONGOING",
                                            "NOT_APPLICABLE",
                                            "UNDEFINED"
                                        ]
                                    }
                                ],
                                "default": null,
                                "doc": "A label describing the nature of the time range in the analyzed temporal bounding. Any individual date descriptor being 'INVALID' results in 'NOT_APPLICABLE' for this field."
                            }
                        ]
                    }
                ],
                "default": null
            },
            {
                "name": "spatialBounding",
                "doc": "Assessment of the spatial bounding information in the metadata",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "SpatialBoundingAnalysis",
                        "fields": [
                            {
                                "name": "spatialBoundingExists",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a spatial bounding"
                            },
                            {
                                "name": "isValid",
                                "type": [
                                    "null",
                                    "boolean"
                                ],
                                "default": null,
                                "doc": "Indicates if the analyzed record has a valid geometry"
                            },
                            {
                                "name": "validationError",
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "default": null,
                                "doc": "if invalid geometry, display the Error message"
                            }
                        ]
                    }
                ],
                "default": null
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
    ) -> 'Analysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
