#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from math import ceil

__author__ = "bl"

import logging, sys, unittest, os, random
from dotenv import load_dotenv

load_dotenv()

setting = {
    "region_name": os.getenv("REGION_NAME"),
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
}

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

from event_recorder import Recorder


class EventRecorderTest(unittest.TestCase):
    def setUp(self):
        self.recorder = Recorder(logger, **setting)
        logger.info("Initiate EventRecorderTest ...")

    def tearDown(self):
        logger.info("Destory EventRecorderTest ...")

    @unittest.skip("demonstrating skipping")
    def test_add_evnet_log(self):
        # subject_types = ["pricing", "factory", "documents", "product", "seller"]
        # names = ["test", "haha"]
        # descriptions = ["A product packaging toggled status.", "created", "deleted"]
        # i = 0

        # while i < 10:
        event_log = {
            "channel": "ss3",
            "subject_type": "user",
            "subject": {
                "product_id": "5819",
                "seller_id": "2018",
                "start_date": "2021-01-19",
                "end_date": "2021-01-21",
                "high_volume_lines": "6",
                "price_tiers": [
                    {"qty": "150", "price": "7"},
                    {"qty": "300", "price": "6"},
                    {"qty": "450", "price": "5"},
                ],
                "allow_vip": False,
                "allow_high_volume_bid": False,
            },
            "subject_id": 5811,
            "causer_id": 118,
            "operation_type": 1,
            "description": "New product price list created.",
            "causer": {
                "email": "klee@abacusipllc.com",
                "email_verified_at": None,
                "created_at": "2020-04-16 14:49:16",
                "updated_at": "2021-04-29 17:22:13",
                "is_active": 1,
                "is_admin": 1,
                "ns_internal_id": 32767,
                "lang_code": "en",
                "first_name": "Kuan",
                "last_name": "Lee",
                "title": "Developer",
                "phone": "1234",
                "ext": None,
                "locale_code": "en",
                "seller_id": None,
                "erp_employee_ref": 35678,
                "cognito_user_sub": None,
            },
            "properties": {},
            "owner": {
                "active": 1,
                "seller_name": "Super System Foods (TEST)",
                "logo_file": "seller-logo/2018.png",
                "website": "http://example.com",
                "created_date": "2019-12-18 19:47:52",
                "created_by": 19,
                "updated_date": "2021-04-05 15:49:48",
                "updated_by": 427,
                "seller_telephone": "1234",
                "emergency_phone_number": "966331445",
                "s_vendor_id": "S10763",
            },
        }

        result = self.recorder.add_event_log(**event_log)
        logger.info(result)

    @unittest.skip("demonstrating skipping")
    def test_get_event_log(self):
        query = """
            query evnetLog($evnet_log_id: String!){
                evnetLog(evnet_log_id: $evnet_log_id){
                    subjectId
                    subjectType
                    subject
                    causerId
                    causer
                    propertie
                    createdAt
                }
            }
        """

        variables = {
            "evnet_log_id": "test",
        }

        payload = {"query": query, "variables": variables}
        response = self.recorder.event_recorder_graphql(**payload)
        logger.info(response)

    # @unittest.skip("demonstrating skipping")
    def test_get_event_logs(self):
        query = """
            query eventLogs(
                $pageSize: Int
                $pageNumber: Int
                $subjectType: [String]
                $subjectId: [String]
                $descriptions: [String]
                $duration: [DateTime]
            ) {
                eventLogs(
                    pageSize: $pageSize
                    pageNumber: $pageNumber
                    subjectType: $subjectType
                    subjectId: $subjectId
                    descriptions: $descriptions
                    duration: $duration
                ) {
                    items {
                        # logId
                        subjectType
                        createdAt
                        subjectId
                    }
                    pageSize
                    pageNumber
                    total
                }
            }
        """
        # variables = {
        #     "pageSize": 2,
        #     "pageNumber": 2,

        #     # "descriptions": [
        #     #     "A product packaging toggled status.",
        #     #     "New product price list created.",
        #     # ],
        #     # # "subjectType": "user",
        #     # "subjectId": "5811",
        #     # "duration": ["2021-08-01T00:00:00Z", "2021-08-29T23:59:59Z"],
        # }
        variables = {
            "pageSize": 10,
            "pageNumber": 1,
            "subjectType": ["pricing"],
            "subjectId": ["c9c12a42-2b3d-11ee-99ea-b67b9efc0cc2"],
            # "descriptions": [
            #     "User updated.",
            #     "A product packaging toggled status.",
            # ],
            # "duration": ["2021-08-01T00:00:00Z", "2021-08-30T23:59:59Z"],
        }

        payload = {"query": query, "variables": variables}
        response = self.recorder.event_recorder_graphql(**payload)
        logger.info(response)

    @unittest.skip("demonstrating skipping")
    def test_get_event_logs_by_backend(self):
        payload = {
            "operation_type": 1,
            "start_at": "2021-09-15T05:03:58Z",
            "end_at": "2021-09-16T05:03:58Z",
            "limit": 1000,
            "last_evaluated_key": None,
        }
        response = self.recorder.get_event_logs("product", **payload)
        logger.info(response)


if __name__ == "__main__":
    unittest.main()
