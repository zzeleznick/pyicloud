#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Command Line Wrapper to allow easy use of pyicloud for
command line scripts, and related.
"""
from __future__ import print_function
import argparse
import sys
import os

import pyicloud


def main(args=None):
    """Main commandline entrypoint"""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Find My iPhone CommandLine Tool")

    parser.add_argument(
        "--username",
        action="store",
        dest="username",
        default="",
        help="Apple ID to Use"
    )
    parser.add_argument(
        "--password",
        action="store",
        dest="password",
        default="",
        help=(
            "Apple ID Password to Use; if unspecified, password will be "
            "fetched from the os environment (APPLE_PW)."
        )
    )

    command_line = parser.parse_args(args)

    username = command_line.username
    password = command_line.password or os.environ.get("APPLE_PW")

    if not username:
        parser.error('No username supplied')

    if not password:
        parser.error('No password supplied')

    try:
        api = pyicloud.PyiCloudService(
            username.strip(),
            password.strip()
        )
    except pyicloud.exceptions.PyiCloudFailedLoginException:
        parser.error("Bad username or password for {username}".format(
            username=username))

    print(str(api.iphone))

if __name__ == '__main__':
    main()
