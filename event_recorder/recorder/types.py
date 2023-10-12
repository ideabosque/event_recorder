#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene import ObjectType, InputObjectType, String, DateTime, List, Int
from silvaengine_utility import JSON

__author__ = "bl"


class EventLog(ObjectType):
    apply_to = String()
    subject_id = String()
    log_id = String()
    operation_type = Int()
    subject_type = String()
    subject = JSON()
    causer_id = String()
    causer = JSON()
    properties = JSON()
    description = String()
    adscription = String()
    created_at = DateTime()


class EventLogs(ObjectType):
    items = List(EventLog)
    total = Int()
    page_number = Int()
    page_size = Int()


class EventLogInput(InputObjectType):
    subject_id = String()
    subject_type = String()
    subject = JSON()
    causer_id = String()
    causer = JSON()
    properties = JSON()
    description = String()
