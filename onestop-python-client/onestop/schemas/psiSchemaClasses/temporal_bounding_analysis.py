from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor

from onestop.schemas.psiSchemaClasses.time_range_descriptor import TimeRangeDescriptor
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.valid_descriptor import ValidDescriptor


@type_checked_constructor()
@dataclass
class TemporalBoundingAnalysis:
    #: Describes the state of the temporal bounding's beginning, i.e. VALID, INVALID, or UNDEFINED.
    beginDescriptor: Optional[ValidDescriptor]

    #: The precision of the beginning of the analyzed bounding, e.g. 'Years', 'Seconds', etc. See java.time.temporal.ChronoUnit. Note that this may sometimes not exactly match the input data, since it reflects the Java class the date is able to be parsed into.
    beginPrecision: Optional[str]

    #: Indicates whether or not beginUtcDateTimeString can be indexed into Elasticsearch for searching.
    beginIndexable: Optional[bool]

    #: The time zone indicated for the beginning of the analyzed temporal bounding with the format (+/-)hh:mm[:ss], or Z for UTC. See java.lang.ZoneOffset.
    beginZoneSpecified: Optional[str]

    #: If provided begin date is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the analyzed value.
    beginUtcDateTimeString: Optional[str]

    #: If provided begin date is VALID, a long indicating the beginning year.
    beginYear: Optional[int]

    #: If provided begin date is VALID, an integer indicating the day of year for the beginning value. This may be populated by extrapolating into a DateTime. See beginPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    beginDayOfYear: Optional[int]

    #: If provided begin date is VALID, an integer indicating the day of month for the beginning value. This may be populated by extrapolating into a DateTime. See beginPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    beginDayOfMonth: Optional[int]

    #: If provided begin date is VALID, an integer indicating the month for the beginning value. This may be populated by extrapolating into a DateTime. See beginPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    beginMonth: Optional[int]

    #: Describes the state of the temporal bounding's end, i.e. VALID, INVALID, or UNDEFINED.
    endDescriptor: Optional[ValidDescriptor]

    #: The precision of the end of the analyzed bounding, e.g. 'Years', 'Seconds', etc. See java.time.temporal.ChronoUnit. Note that this may sometimes not exactly match the input data, since it reflects the Java class the date is able to be parsed into.
    endPrecision: Optional[str]

    #: Indicates whether or not endUtcDateTimeString can be indexed into Elasticsearch for searching.
    endIndexable: Optional[bool]

    #: The time zone indicated for the end of the analyzed temporal bounding with the format (+/-)hh:mm[:ss], or Z for UTC. See java.lang.ZoneOffset.
    endZoneSpecified: Optional[str]

    #: If provided end date is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the analyzed end value.
    endUtcDateTimeString: Optional[str]

    #: If provided end date is VALID, an long indicating the end year.
    endYear: Optional[int]

    #: If provided end date is VALID, an integer indicating the day of year for the end value. This may be populated by extrapolating into a DateTime. See endPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    endDayOfYear: Optional[int]

    #: If provided end date is VALID, an integer indicating the day of month for the end value. This may be populated by extrapolating into a DateTime. See endPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    endDayOfMonth: Optional[int]

    #: If provided end date is VALID, an integer indicating the month for the end value. This may be populated by extrapolating into a DateTime. See endPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    endMonth: Optional[int]

    #: Describes the state of the temporal bounding's instant, i.e. VALID, INVALID, or UNDEFINED.
    instantDescriptor: Optional[ValidDescriptor]

    #: The precision of the instant of the analyzed bounding, e.g. 'Years', 'Seconds', etc. See java.time.temporal.ChronoUnit. Note that this may sometimes not exactly match the input data, since it reflects the Java class the date is able to be parsed into.
    instantPrecision: Optional[str]

    #: Indicates whether or not instantUtcDateTimeString/instantEndUtcDateTimeString can be indexed into Elasticsearch for searching.
    instantIndexable: Optional[bool]

    #: The time zone indicated for the instant of the analyzed temporal bounding with the format (+/-)hh:mm[:ss], or Z for UTC. See java.lang.ZoneOffset.
    instantZoneSpecified: Optional[str]

    #: If provided instant is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the analyzed instant value.
    instantUtcDateTimeString: Optional[str]

    #: If provided instant is VALID, a full ISO-8601 formatted date time string in the UTC time zone for the end analyzed instant value. The actual or assumed end date time based on precision of original data.
    instantEndUtcDateTimeString: Optional[str]

    #: If provided instant is VALID, an long indicating the instant year.
    instantYear: Optional[int]

    #: If provided instant is VALID, an integer indicating the day of year for the instant value. This may be populated by extrapolating into a DateTime. See instantPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    instantDayOfYear: Optional[int]

    #: If provided instant is VALID, an integer indicating the actual or assumed day of year the instant ends depending on the precision of the original content, e.g. the last day of a month or year.
    instantEndDayOfYear: Optional[int]

    #: If provided instant is VALID, an integer indicating the day of month for the instant value. This may be populated by extrapolating into a DateTime. See instantPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    instantDayOfMonth: Optional[int]

    #: If provided instant is VALID, an integer indicating the actual or assumed day of month the instant ends depending on precision, e.g. the last day of a month or year.
    instantEndDayOfMonth: Optional[int]

    #: If provided instant is VALID, an integer indicating the month for the instant value. This may be populated by extrapolating into a DateTime. See instantPrecision for the best indicator of if this value is extrapolated or provided in the original date format.
    instantMonth: Optional[int]

    #: If provided instant is VALID and instantPrecision does not include day, an integer indicating the assumed month the instant ends, e.g. the last month of the year.
    instantEndMonth: Optional[int]

    #: A label describing the nature of the time range in the analyzed temporal bounding. Any individual date descriptor being 'INVALID' results in 'NOT_APPLICABLE' for this field.
    rangeDescriptor: Optional[TimeRangeDescriptor]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
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
    ) -> 'TemporalBoundingAnalysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
