import unittest

from policy_generator.role_generator import RoleGenerator


class TestRoleGenerator(unittest.TestCase):

    def setUp(self):
        self.cloudformation = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {}
        }

        self.expected_cloud_formation = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "Policy Generator Role",

            "Resources": {
                "PolicyGeneratorRole": {
                    "Properties": {
                        "Policies": [
                            {
                                "PolicyDocument": {
                                    "Statements": [
                                        {
                                            "Sid": "Policy-Generator-CloudFormation-MainCloudFormation",
                                            "Statement": {
                                                "Action": ["cloudformation:CreateStack",
                                                           "cloudformation:UpdateStack",
                                                           "cloudformation:DescribeStacks"],
                                                "Effect": "Allow",
                                                "Resource": "*"
                                            },
                                        }
                                    ],
                                    "Version": "2012-10-17"
                                },
                                "PolicyName": "Policy-Generator-CloudFormation-MainCloudFormation"
                            }
                        ]
                    },
                    "RoleName": "PolicyGeneratorRole",
                    "Type": "AWS::IAM::Role"
                }
            }
        }

    def test_s3_bucket(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [{
                        "Sid": "Policy-Generator-S3-Bucket-TestResource",
                        "Statement": {
                            "Effect": "Allow",
                            "Action": ["s3:CreateBucket", "s3:DeleteBucket"],
                            "Resource": "*"
                        }
                    }],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-S3-Bucket-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_s3_bucket_with_name(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket",
                "BucketName": "my-test-bucket"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [{
                        "Sid": "Policy-Generator-S3-Bucket-TestResource",
                        "Statement": {
                            "Effect": "Allow",
                            "Action": ["s3:CreateBucket", "s3:DeleteBucket"],
                            "Resource": "arn:aws:s3:::my-test-bucket"
                        }
                    }],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-S3-Bucket-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_lambda(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::Lambda::Function",
                "Role": "MOCKED_ROLE_ARN"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [{
                        "Sid": "Policy-Generator-Lambda-Function-TestResource-Global",
                        "Statement": {
                            "Effect": "Allow",
                            "Action": ["lambda:CreateFunction"],
                            "Resource": "*"
                        }
                    },
                        {
                            "Sid": "Policy-Generator-Lambda-Function-TestResource-Role",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["iam:PassRole"],
                                "Resource": "MOCKED_ROLE_ARN"
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
                    ],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-Lambda-Function-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_lambda_with_name(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::Lambda::Function",
                "FunctionName": "LambdaName",
                "Role": "MOCKED_ROLE_ARN"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
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
                            "Sid": "Policy-Generator-Lambda-Function-TestResource-Role",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["iam:PassRole"],
                                "Resource": "MOCKED_ROLE_ARN"
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
                    ],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-Lambda-Function-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_vpc_lambda(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::Lambda::Function",
                "VpcConfig": "TEMP",
                "Role": "MOCKED_ROLE_ARN"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [
                        {
                            "Sid": "Policy-Generator-Lambda-Function-TestResource-Global",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["lambda:CreateFunction", "ec2:AllocateAddress", "ec2:ReleaseAddress",
                                           "ec2:DescribeAddresses"],
                                "Resource": "*"
                            }
                        },
                        {
                            "Sid": "Policy-Generator-Lambda-Function-TestResource-Role",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["iam:PassRole"],
                                "Resource": "MOCKED_ROLE_ARN"
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
                    ],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-Lambda-Function-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_check_ref_params(self):
        self.cloudformation["Parameters"] = {
            "TestParam": {
                "Description": "TEST_DESCRIPTION",
                "Default": "TEST_DEFAULT",
                "Type": "TEST_TYPE"
            }
        }
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket",
                "BucketName": "!Ref TestParam"
            }
        }
        role_cloud_formation = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        print(role_cloud_formation)
        self.assertEqual(self.cloudformation["Parameters"], role_cloud_formation["Parameters"])

    def test_ec2_instance(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::EC2::Instance"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [
                        {
                            "Sid": "Policy-Generator-EC2-Instance-TestResource",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["ec2:RunInstances"],
                                "Resource": "*"
                            }
                        }
                    ],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-EC2-Instance-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_ec2_instance_with_image(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::EC2::Instance",
                "ImageId": "TEST_IMAGE_ID"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [
                        {
                            "Sid": "Policy-Generator-EC2-Instance-TestResource",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["ec2:RunInstances"],
                                "Resource": "arn:aws:ec2:us-east-1::image/TEST_IMAGE_ID"
                            }
                        }
                    ],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-EC2-Instance-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)

    def test_ec2_instance_with_instance_profile(self):
        self.cloudformation["Resources"] = {
            "TestResource": {
                "Type": "AWS::EC2::Instance",
                "IamInstanceProfile": "TEST_INSTANCE_PROFILE"
            }
        }
        policy = RoleGenerator(self.cloudformation, "us-east-1", "ABC123123").generate()
        self.expected_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] += [
            {
                "PolicyDocument": {
                    "Statements": [
                        {
                            "Sid": "Policy-Generator-EC2-Instance-TestResource",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["ec2:RunInstances"],
                                "Resource": "*"
                            }
                        },
                        {
                            "Sid": "Policy-Generator-EC2-Instance-TestResource-Role",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": ["iam:PassRole"],
                                "Resource": "arn:aws:iam::ABC123123:role/TEST_INSTANCE_PROFILE"
                            }
                        }
                    ],
                    "Version": "2012-10-17"
                },
                "PolicyName": "Policy-Generator-EC2-Instance-TestResource"
            }
        ]
        self.assertEqual(self.expected_cloud_formation, policy)
