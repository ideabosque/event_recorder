#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from email.policy import default
from graphene import ObjectType, String, Int, Schema, Field, List, DateTime
from .types import EventLog, EventLogs
from .queries import resolve_event_logs, resolve_event_log
from .mutations import AddEventLog
from silvaengine_utility import JSON

__author__ = "bl"


def type_class():
    return [EventLogs, EventLog]


# Query resource or role list
class Query(ObjectType):
    event_logs = Field(
        EventLogs,
        page_size=Int(),
        page_number=Int(),
        descriptions=List(String),
        subject_type=List(String),
        subject_id=List(String),
        duration=List(DateTime),
        owner=String(),
        adscription=String(),
    )
    event_log = Field(
        EventLog,
        log_id=String(),
    )

    def resolve_event_logs(self, info, **kwargs):
        return resolve_event_logs(info, **kwargs)

    def resolve_event_log(self, info, **kwargs):
        return resolve_event_log(info, **kwargs)


# Add event log
class Mutations(ObjectType):
    add_event_log = AddEventLog.Field()


# Generate API documents.
def graphql_schema_doc():
    from graphdoc import to_doc

    schema = Schema(
        query=Query,
        types=type_class(),
    )

    return to_doc(schema)
