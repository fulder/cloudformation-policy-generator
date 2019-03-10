from policy_generator.resources.policy import Policy


class S3Bucket(Policy):

    def __init__(self, name, res):
        super(S3Bucket, self).__init__(name, res)

    def create_policy(self):
        resource = "*"
        if "BucketName" in self.res:
            resource = self._create_resource("arn:aws:s3:::{res_value}", res_value=self.res["BucketName"])

        actions = ["s3:CreateBucket", "s3:DeleteBucket"]
        self._add_policy_statement(actions, resource)
        return self.cloudformation_policies
