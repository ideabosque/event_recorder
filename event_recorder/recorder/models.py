#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from silvaengine_utility import JSON
from pynamodb.models import Model

# from pynamodb.indexes import GlobalSecondaryIndex, LocalSecondaryIndex, AllProjection
from pynamodb.attributes import (
    UnicodeAttribute,
    UTCDateTimeAttribute,
    NumberAttribute,
    MapAttribute,
    ListAttribute,
    BooleanAttribute,
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from .enumerations import ClientType
import os

__author__ = "bl"


# Preset resource status
# class Status:
#     enabled = 1


# class SubjectTypeCreatedAtIndex(GlobalSecondaryIndex):
#     """
#     This class represents a local secondary index
#     """

#     class Meta:
#         billing_mode = "PAY_PER_REQUEST"
#         # All attributes are projected
#         projection = AllProjection()
#         index_name = "subject_type-created_at-index"

#     subject_type = UnicodeAttribute(hash_key=True)
#     created_at = UnicodeAttribute(range_key=True)


class BaseModel(Model):
    class Meta:
        billing_mode = "PAY_PER_REQUEST"
        region = os.getenv("REGIONNAME")

class SubjectTypeSubjectIdIndex(GlobalSecondaryIndex):
    """
    This class represents a local secondary index
    """

    class Meta:
        billing_mode = "PAY_PER_REQUEST"
        # All attributes are projected
        projection = AllProjection()
        index_name = "subject_type-subject_id-index"

    subject_type = UnicodeAttribute(hash_key=True)
    subject_id = NumberAttribute(range_key=True)

class SubjectTypeCreatedAtIndex(GlobalSecondaryIndex):
    """
    This class represents a local secondary index
    """

    class Meta:
        billing_mode = "PAY_PER_REQUEST"
        # All attributes are projected
        projection = AllProjection()
        index_name = "subject_type-created_at-index"

    subject_type = UnicodeAttribute(hash_key=True)
    created_at = NumberAttribute(range_key=True)
    


class EventLogModel(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "se-event_logs"

    apply_to = UnicodeAttribute(hash_key=True)
    log_id = UnicodeAttribute(range_key=True)
    subject_type_subject_id_index = SubjectTypeSubjectIdIndex()
    subject_type_created_at_index = SubjectTypeCreatedAtIndex()
    subject_type = UnicodeAttribute()
    operation_type = NumberAttribute(default=0)
    subject_id = UnicodeAttribute()
    subject = UnicodeAttribute()
    causer_id = UnicodeAttribute()
    causer = UnicodeAttribute()
    description = UnicodeAttribute()
    properties = UnicodeAttribute()
    adscription = UnicodeAttribute(default=str(ClientType.SS3.value).strip().lower())
    created_at = UTCDateTimeAttribute()
    # subject_type_created_at_index = SubjectTypeCreatedAtIndex()
