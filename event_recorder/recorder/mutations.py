#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene import Field, Mutation
from silvaengine_utility import Utility
from .types import EventLog, EventLogInput
from .handlers import add_event_log
import traceback


__author__ = "bl"


# Append or modify role info.
class AddEventLog(Mutation):
    event_log = Field(EventLog)

    class Arguments:
        event_log_data = EventLogInput(required=True)

    @staticmethod
    def mutate(root, info, event_log=None):
        try:
            _event_log = add_event_log(event_log)
            event_log = EventLog(
                **Utility.json_loads(
                    Utility.json_dumps(_event_log.__dict__["attribute_values"])
                )
            )
        except Exception:
            log = traceback.format_exc()
            info.context.get("logger").exception(log)
            raise

        return AddEventLog(event_log=event_log)
