#!/usr/bin/env python3

import argparse

import requests
from github import Github

import get_ssm_parameter


def setup_argparser():
    parser = argparse.ArgumentParser(
        description='Get a specific asset version from GitHub repository.')
    parser.add_argument('-r', '--repo', required=True)
    parser.add_argument('-v', '--version', required=True)
    parser.add_argument(
        '--profile',
        required=False,
        help='AWS profile, needed if running on e.g dev machine.',
        type=str)
    return parser


def fetch_artifact(repo_name, version, profile=None):
    github_token = get_ssm_parameter.fetch_parameter('CiGithubAccessToken',
                                                     profile=profile)
    g = Github(github_token)
    repo = g.get_organization("HBONordic").get_repo(repo_name)

    for release in repo.get_releases():
        if release.tag_name == version:
            for asset in release.get_assets():
                print(asset.name)
                c = requests.Session()
                c.auth = (github_token, '')
                r = c.get(asset.url,
                          headers={'Accept': 'application/octet-stream'})
                open(asset.name, 'wb').write(r.content)


def main():
    parser = setup_argparser()
    args = parser.parse_args()
    profile = args.profile
    repo_name = args.repo
    version = args.version
    fetch_artifact(repo_name, version, profile=profile)


if __name__ == "__main__":
    main()
