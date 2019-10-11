#!/usr/bin/env python3

import argparse
import logging
import sys

import libs.awsutils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('get_ssm_parameter')


def setup_argparser():
    parser = argparse.ArgumentParser(
        description='Get arbitrary AWS SSM parameter.')
    parser.add_argument(
        '--profile',
        required=False,
        help='AWS profile, needed if running on e.g dev machine.',
        type=str)
    parser.add_argument('--parameter',
                        required=True,
                        help='Target AWS SSM parameter.',
                        type=str)
    return parser


def fetch_parameter(parameter_name, profile=False):

    aws = libs.awsutils.AWSUtils(profile=profile)
    client = aws.get_client('ssm')
    parameter = client.get_parameter(Name=parameter_name, WithDecryption=True)
    if not parameter:
        logger.debug(
            'Could not get parameter: {}. Exiting.'.format(parameter_name))
        sys.exit(1)
    return parameter['Parameter']['Value']


def main():
    parser = setup_argparser()
    args = parser.parse_args()
    profile = args.profile
    parameter_value = fetch_parameter(args.parameter, profile=profile)
    print(parameter_value)


if __name__ == "__main__":
    main()
