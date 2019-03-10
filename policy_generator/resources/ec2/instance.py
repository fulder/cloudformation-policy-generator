from policy_generator.resources.policy import Policy


class EC2Instance(Policy):

    def __init__(self, name, res, region, account):
        super(EC2Instance, self).__init__(name, res, region, account)

    def create_policy(self):
        actions = ["ec2:RunInstances"]
        resource = "*"
        if "ImageId" in self.res:
            resource = self._create_resource("arn:aws:ec2:{region}::image/{res_value}", self.res["ImageId"])
        self._add_policy_statement(actions, resource)

        if "IamInstanceProfile" in self.res:
            actions = ["iam:PassRole"]
            resource = self._create_resource("arn:aws:iam::{account}:role/{res_value}", self.res["IamInstanceProfile"])
            self._add_policy_statement(actions, resource, name_suffix="Role")

        return self.cloudformation_policies
