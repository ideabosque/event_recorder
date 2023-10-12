#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from silvaengine_utility import Utility
from datetime import datetime
from .models import EventLogModel
import pendulum, jsonpickle, random

__author__ = "bl"


def add_event_log(event_log_data, channel):
    try:
        # @TODO: data check
        now = pendulum.now(tz="UTC")
        log_id = "{}{:0>3}".format(
            str(int(now.timestamp() * 1000000)), random.randint(1, 999)
        )
        owner = (
            jsonpickle.decode(event_log_data.get("owner", {}))
            if event_log_data.get("owner")
            and Utility.is_json_string(event_log_data.get("owner"))
            else event_log_data.get("owner", {})
        )
        print("_____________________________________________________________________________________>>>")
        print(Utility.json_dumps(
                Utility.json_loads(
                    event_log_data.get("properties", {}),
                    parser_number=False,
                )
                if Utility.is_json_string(event_log_data.get("subject"))
                else event_log_data.get("subject", {})
            ))
        print("<<<_____________________________________________________________________________________")
        log = {
            "subject_type": str(event_log_data.get("subject_type")).strip(),
            "subject_id": str(event_log_data.get("subject_id")),
            "operation_type": int(event_log_data.get("operation_type")),
            # "subject": jsonpickle.decode(Utility.json_dumps(event_log_data.get("subject")).encode("utf-8"))
            # if Utility.is_json_string(event_log_data.get("subject"))
            # else jsonpickle.encode(event_log_data.get("subject"), unpicklable=False),
            "subject": Utility.json_dumps(
                Utility.json_loads(
                    event_log_data.get("properties", {}),
                    parser_number=False,
                )
                if Utility.is_json_string(event_log_data.get("subject"))
                else event_log_data.get("subject", {})
            ),
            "causer_id": str(event_log_data.get("causer_id")),
            "causer": event_log_data.get("causer")
            if Utility.is_json_string(event_log_data.get("causer"))
            else jsonpickle.encode(event_log_data.get("causer"), unpicklable=False),
            "properties": jsonpickle.encode(
                {
                    "owner": jsonpickle.decode(event_log_data.get("owner", {}))
                    if Utility.is_json_string(event_log_data.get("owner"))
                    else jsonpickle.decode(
                        jsonpickle.encode(
                            event_log_data.get("owner", {}),
                            unpicklable=False,
                        )
                    ),
                    "properties": Utility.json_loads(
                        event_log_data.get("properties", {}),
                        parser_number=False,
                    )
                    if Utility.is_json_string(event_log_data.get("properties"))
                    else jsonpickle.decode(
                        jsonpickle.encode(
                            event_log_data.get("properties", {}),
                            unpicklable=False,
                        )
                    ),
                },
                unpicklable=False,
            ),
            "adscription": str(owner.get("seller_name", "")).strip().lower()
            if type(owner) is dict
            else str(owner).strip().lower(),
            "description": str(event_log_data.get("description", "")),
            "created_at": now,
        }

        EventLogModel(
            str(channel).strip().lower(),
            log_id,
            **log,
        ).save()

        return {"log_id": log_id}
    except Exception as e:
        raise e


def get_event_logs(
    subject_type,
    operation_type=None,
    start_at=None,
    end_at=None,
    limit=50,
    last_evaluated_key=None,
    channel=None,
):
    try:
        limit = int(limit) if limit and int(limit) > 0 else None
        arguments = {
            "limit": limit,
            "hash_key": str(channel).strip().lower(),
            "last_evaluated_key": last_evaluated_key,
            "filter_condition": None,
        }

        filter_conditions = [EventLogModel.subject_type == str(subject_type).strip()]

        if operation_type is not None:
            filter_conditions.append(
                EventLogModel.operation_type == int(operation_type)
            )

        if start_at is not None:
            filter_conditions.append(
                EventLogModel.created_at
                > datetime.strptime(str(start_at), "%Y-%m-%dT%H:%M:%SZ")
            )

        if end_at is not None:
            filter_conditions.append(
                EventLogModel.created_at
                <= datetime.strptime(str(end_at), "%Y-%m-%dT%H:%M:%SZ")
            )

        if len(filter_conditions):
            arguments["filter_condition"] = filter_conditions.pop(0)

            for condition in filter_conditions:
                arguments["filter_condition"] = arguments.get("filter_condition") & (
                    condition
                )

        results = EventLogModel.query(**arguments)
        logs = [dict(**log.__dict__["attribute_values"]) for log in results]

        if results.total_count < 1:
            return None

        return {"logs": logs, "last_evaluated_key": results.last_evaluated_key}
    except Exception as e:
        raise e
