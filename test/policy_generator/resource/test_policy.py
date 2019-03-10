import unittest

from policy_generator.resources.policy import Policy


class TestPolicy(unittest.TestCase):

    def setUp(self):
        self.policy = Policy("TEST_POLICY_NAME", {"Type": "AWS::TEST_RES::TEST_RES_SUB"}, "us-east-1", "ABC123123")

    def test_create_resource(self):
        res = self.policy._create_resource("arn::{res_value}", "TEST_RES_VALUE")
        self.assertEqual("arn::TEST_RES_VALUE", res)

    def test_create_resource_with_region(self):
        res = self.policy._create_resource("arn::{region}:{res_value}", "TEST_RES_VALUE")
        self.assertEqual("arn::us-east-1:TEST_RES_VALUE", res)

    def test_create_resource_with_account(self):
        res = self.policy._create_resource("arn::{account}:{res_value}", "TEST_RES_VALUE")
        self.assertEqual("arn::ABC123123:TEST_RES_VALUE", res)

    def test_create_resource_from_dict(self):
        res = self.policy._create_resource("arn::{region}:{account}:{res_value}",
                                           {"Fn::ImportValue": "my-stack-Import"})
        expected_res = {
            "Fn::Sub": [
                "arn::us-east-1:ABC123123:${TEST_RES-TEST_RES_SUB-TEST_POLICY_NAME}",

                {
                    "TEST_RES-TEST_RES_SUB-TEST_POLICY_NAME": {
                        "Fn::ImportValue": "my-stack-Import"
                    }
                }
            ]
        }
        self.assertEqual(expected_res, res)

    def test_create_super_class_policy(self):
        self.assertRaises(NotImplementedError, self.policy.create_policy)
