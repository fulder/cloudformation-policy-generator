import unittest

from generator import PolicyGenerator


class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.cloudformation: dict = {
            "AWSTemplateFormatVersion": "2010-09-09"
        }

    def test_s3_bucket(self):
        self.cloudformation["Resources"] = {
            "TestBucket": {
                "Type": "AWS::S3::Bucket"
            }
        }
        policy = PolicyGenerator(self.cloudformation).generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [{
                "Sid": "Policy-Generator-S3-Bucket-TestBucket",
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
            "TestBucket": {
                "Type": "AWS::S3::Bucket",
                "BucketName": "my-test-bucket"
            }
        }
        policy = PolicyGenerator(self.cloudformation).generate()
        expected_policy = {
            "Version": "2012-10-17",
            "Statements": [{
                "Sid": "Policy-Generator-S3-Bucket-TestBucket",
                "Statement": {
                    "Effect": "Allow",
                    "Action": ["s3:CreateBucket", "s3:DeleteBucket"],
                    "Resource": "arn:aws:s3:::my-test-bucket"
                }
            }]
        }
        self.assertEqual(policy, expected_policy)
