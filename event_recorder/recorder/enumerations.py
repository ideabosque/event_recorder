#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enum import Enum

__author__ = "bl"


class OperationType(Enum):
    CREATE = 0
    UPDATE = 1
    DELETE = 2
    APPROVAL = 3
    REJECT = 4
    CANCEL = 5
    ON_SALE = 10
    OFF_SALE = 11
    ASSIGN = 21
    UNASSIGN = 22


class LogType(Enum):
    PAYMENT_REQUEST = "payment_request"
    PRODUCT = "product"
    DOCUMENT = "document"
    PRICING = "pricing"
    SELLER = "seller"
    COMPANY = "company"
    FACTORY = "factory"
    USER = "user"
    ORDER_FULFILLMENT = "order_fulfillment"
    SHIPMENT = "shipment"
    PROMOTION = "promotion"
    PRICE_INQUIRY = "price_inquiry"


class ClientType(Enum):
    SS3 = "ss3"
    API = "api"
