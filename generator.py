import argparse
import json

import yaml


class PolicyGenerator:

    def __init__(self, cloudformation: dict):
        self.cloudformation = cloudformation

    def generate(self):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloudformation Generator")
    parser.add_argument("-f", "--file", help="Path to the CloudFormation template", required=True)
    parser.add_argument("-o", "--out", help="Save output to the specified file")
    args = parser.parse_args()

    cloudformation = yaml.safe_load(args.file)
    policy = PolicyGenerator(cloudformation).generate()

    if args.out is not None:
        with open('data.txt', 'w') as outfile:
            json.dump(policy, outfile)
