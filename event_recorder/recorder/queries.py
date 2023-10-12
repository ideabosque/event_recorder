#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene.types import argument
import jsonpickle
from silvaengine_utility import Utility
from datetime import datetime
from .types import EventLog, EventLogs
from .models import EventLogModel


__author__ = "bl"


def resolve_event_logs(info, **kwargs):
    limit = kwargs.get("page_size", 10)
    page_number = kwargs.get("page_number", 0)
    subject_type = kwargs.get("subject_type")
    subject_id = kwargs.get("subject_id")
    descriptions = kwargs.get("descriptions")
    duration = kwargs.get("duration")
    channel = str(info.context.get("channel")).strip().lower()
    adscription = kwargs.get("adscription")

    if page_number > 0 and (limit is None or int(limit) < 1):
        raise Exception("The page number must be used in conjunction with limit.", 400)

    if type(limit) is not int and limit < 1:
        limit = None

    queryModel = EventLogModel
    arguments = {
        "hash_key": channel,
        "range_key_condition": None,
        "scan_index_forward": False,
        "limit": limit,
    }
    filter_conditions = []

    # Filter by subject type
    if type(subject_type) is list and len(subject_type):
        subject_type = list(set([str(item).strip() for item in subject_type]))

        if len(subject_type) == 1:
            queryModel = EventLogModel.subject_type_created_at_index
            arguments["hash_key"] = subject_type[0]
        else:
            filter_conditions.append(EventLogModel.subject_type.is_in(*subject_type))

    # Filter by subject ID
    if type(subject_id) is list and len(subject_id):
        subject_id = list(set([str(item).strip() for item in subject_id]))
        
        # if queryModel == EventLogModel.subject_type_created_at_index:
        #     if len(subject_id)==1:
        #         arguments["range_key_condition"] = (EventLogModel.subject_id == subject_id[0])
        # else:
        filter_conditions.append(EventLogModel.subject_id.is_in(*subject_id))

    # Filter by adscription relationship.
    if adscription:
        filter_conditions.append(
            EventLogModel.adscription.contains(str(adscription).strip().lower())
        )

    # Filter by duration of created at
    if type(duration) is list and len(duration):
        if type(arguments.get("filter_condition")) is not list:
            arguments["filter_condition"] = []

        start = duration.pop(0)
        end = datetime.utcnow()

        if len(duration):
            end = duration.pop()

        filter_conditions.append(EventLogModel.created_at.between(start, end))

    # Filter by desciptions
    if type(descriptions) is list and len(descriptions):
        filter_conditions.append(
            EventLogModel.description.is_in(*list(set(descriptions)))
        )

    if len(filter_conditions):
        arguments["filter_condition"] = filter_conditions.pop(0)

        for condition in filter_conditions:
            arguments["filter_condition"] = arguments.get("filter_condition") & (
                condition
            )

    # Count logs
    count = queryModel.count(
        hash_key=arguments["hash_key"],
        range_key_condition=arguments["range_key_condition"],
        filter_condition=arguments.get("filter_condition"),
    )

    # Pagination
    if limit and limit > 0 and page_number > 1:
        pagination_arguments = {
            "hash_key": arguments["hash_key"],
            "range_key_condition": arguments["range_key_condition"],
            "limit": (int(page_number) - 1) * int(limit),
            "last_evaluated_key": None,
            "scan_index_forward": False,
            "filter_condition": arguments.get("filter_condition"),
            "attributes_to_get": ["apply_to", "log_id", "subject_type", "subject_id", "created_at"],
        }

        pagination_results = queryModel.query(**pagination_arguments)
        _ = sum(1 for _ in pagination_results)
        arguments["last_evaluated_key"] = pagination_results.last_evaluated_key

        if arguments["last_evaluated_key"] is None:
            return None

    # Read data from dynamodb
    results = queryModel.query(**arguments)
    items = []

    for log in results:
        for field in ["subject", "causer", "properties"]:
            if hasattr(log, field):
                value = getattr(log, field)

                if Utility.is_json_string(value):
                    setattr(log, field, jsonpickle.decode(value))

        items.append(EventLog(**dict(**log.__dict__["attribute_values"])))

    return EventLogs(
        items=items,
        total=count,
        page_number=int(page_number),
        page_size=int(limit),
    )


def resolve_event_log(info, **kwargs):
    log_id = kwargs.get("log_id")
    channel = str(info.context.get("channel")).strip().lower()

    if log_id and channel:
        event_log = EventLogModel.get(hash_key=channel, range_key=log_id)

        for field in ["subject", "causer", "properties"]:
            if hasattr(event_log, field):
                setattr(event_log, jsonpickle.decode(getattr(event_log, field)))

        return EventLog(**dict(**event_log.__dict__["attribute_values"]))
    return None
