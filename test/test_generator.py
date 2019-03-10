import unittest

from generate import PolicyGenerator


class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.cloudformation = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {}
        }

    def test_s3_bucket(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket"
            }
        }
        policy = PolicyGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [
                {
                    "Sid": "Policy-Generator-S3-Bucket-TestResource",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["s3:CreateBucket", "s3:DeleteBucket"],
                        "Resource": "*"
                    }
                }]
        }
        self.assertEqual(policy, expected_policy)

    def test_s3_bucket_with_name(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket",
                "BucketName": "my-test-bucket"
            }
        }
        policy = PolicyGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [
                {
                    "Sid": "Policy-Generator-S3-Bucket-TestResource",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["s3:CreateBucket", "s3:DeleteBucket"],
                        "Resource": "arn:aws:s3:::my-test-bucket"
                    }
                }]
        }
        self.assertEqual(policy, expected_policy)

    def test_lambda(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::Lambda::Function"
            }
        }
        policy = PolicyGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [
                {
                    "Sid": "Policy-Generator-Lambda-Function-TestResource-Global",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["lambda:CreateFunction"],
                        "Resource": "*"
                    }
                },
                {
                    "Sid": "Policy-Generator-Lambda-Function-TestResource",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["lambda:DeleteFunction"],
                        "Resource": "*"
                    }
                }
            ]
        }
        self.assertEqual(policy, expected_policy)

    def test_lambda_with_name(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::Lambda::Function",
                "FunctionName": "LambdaName"
            }
        }
        policy = PolicyGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [
                {
                    "Sid": "Policy-Generator-Lambda-Function-TestResource-Global",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["lambda:CreateFunction"],
                        "Resource": "*"
                    }
                },
                {
                    "Sid": "Policy-Generator-Lambda-Function-TestResource",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["lambda:DeleteFunction"],
                        "Resource": "arn:aws:lambda:us-east-1:ABC123123:function:LambdaName"
                    }
                }
            ]
        }
        self.assertEqual(policy, expected_policy)

    def test_vpc_lambda(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::Lambda::Function",
                "VpcConfig": "TEMP"
            }
        }
        policy = PolicyGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [
                {
                    "Sid": "Policy-Generator-Lambda-Function-TestResource-Global",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["lambda:CreateFunction", "ec2:AllocateAddress", "ec2:AssociateAddress",
                                   "ec2:DisassociateAddress"],
                        "Resource": "*"
                    }
                },
                {
                    "Sid": "Policy-Generator-Lambda-Function-TestResource",
                    "Statement": {
                        "Effect": "Allow",
                        "Action": ["lambda:DeleteFunction"],
                        "Resource": "*"
                    }
                }
            ]
        }
        self.assertEqual(policy, expected_policy)
