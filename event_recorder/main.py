#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene import Schema
from silvaengine_utility import Utility, Graphql
from .recorder.schema import Query, Mutations, type_class
from .recorder.handlers import add_event_log, get_event_logs
from .recorder.models import EventLogModel
from .recorder.enumerations import ClientType
import jsonpickle


__author__ = "bl"


# Hook function applied to deployment
def deploy() -> list:
    return [
        {
            "service": "event_recorder",
            "class": "Recorder",
            "functions": {
                "event_recorder_graphql": {
                    "is_static": False,
                    "label": "Event Recorder",
                    "query": [
                        {
                            "action": "eventLogs",
                            "label": "View All Event",
                        },
                        {
                            "action": "eventLog",
                            "label": "View Event Detail",
                        },
                    ],
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": True,
                    "is_graphql": True,
                    "settings": "beta_core_api",
                }
            },
        }
    ]


class Recorder(object):
    def __init__(self, logger, **setting):
        self.logger = logger
        self.setting = setting

    # Add new log
    def add_event_log(
        self,
        subject_type,
        subject_id,
        subject,
        operation_type,
        description,
        causer_id,
        causer,
        owner,
        properties=None,
        channel=None,
    ):
        try:
            event_log = {
                "subject_type": str(subject_type).strip().lower(),
                "subject": subject,
                "subject_id": str(subject_id).strip().lower(),
                "causer_id": causer_id,
                "operation_type": int(operation_type) if operation_type else 0,
                "description": description,
                "causer": causer,
                "properties": properties,
                "owner": owner,
            }

            if not channel:
                channel = ClientType.SS3.value

            return add_event_log(event_log, channel)
        except Exception as e:
            raise e

    # List logs.
    def get_event_logs(
        self,
        subject_type,
        operation_type=None,
        start_at=None,
        end_at=None,
        limit=50,
        last_evaluated_key=None,
        channel=None,
    ):
        try:
            if not channel:
                channel = ClientType.SS3.value

            return get_event_logs(
                subject_type,
                operation_type=operation_type,
                start_at=start_at,
                end_at=end_at,
                limit=limit,
                last_evaluated_key=last_evaluated_key,
                channel=channel,
            )
        except Exception as e:
            raise e

    # Event log recorder entry.
    def event_recorder_graphql(self, **params):
        try:
            channel = params.get("endpoint_id", ClientType.SS3.value)

            if not channel:
                raise Exception("Unrecognized request origin", 401)

            schema = Schema(
                query=Query,
                mutation=Mutations,
                types=type_class(),
            )
            context = {
                "logger": self.logger,
                "channel": str(channel).strip(),
            }
            variables = params.get("variables", {})
            operations = params.get("query")
            response = {
                "errors": "Invalid operations.",
                "status_code": 400,
            }

            if not operations:
                return jsonpickle.encode(response, unpicklable=False)

            execution_result = schema.execute(
                operations, context_value=context, variable_values=variables
            )

            if not execution_result:
                response = {
                    "errors": "Invalid execution result.",
                }
            elif execution_result.errors:
                response = {
                    "errors": [
                        Utility.format_error(e) for e in execution_result.errors
                    ],
                }
            elif execution_result.invalid:
                response = execution_result
            elif execution_result.data:
                response = {"data": execution_result.data, "status_code": 200}
            else:
                response = {
                    "errors": "Uncaught execution error.",
                }

            return jsonpickle.encode(response, unpicklable=False)
        except Exception as e:
            raise e
