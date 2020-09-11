#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: pinger

:Synopsis:
    Ping network resources and report response time.

:Author:
    servilla

:Created:
    9/10/20
"""
from datetime import datetime
import logging
import os
from time import sleep

import click
import daiquiri
import requests


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/ping.log"
daiquiri.setup(level=logging.INFO, outputs=(daiquiri.output.File(logfile),
                                            "stdout",))
logger = daiquiri.getLogger(__name__)

help_duration = (
    "Set how long pinging should last in seconds (default is continuous)."
)
help_frequency = (
    "Set how frequent the ping request should be sent (default "
    "is every 5 seconds)."
)
help_timeout = (
    "Set how long the ping request should wait before aborting "
    "(default is 5 seconds)."
)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("target", nargs=1, required=True)
@click.option("-d", "--duration", default=0, help=help_duration)
@click.option("-f", "--frequency", default=5, help=help_frequency)
@click.option("-t", "--timeout", default=5, help=help_timeout)
def main(target: str, duration: int, frequency: int, timeout: int):
    """
        Ping network resources and report response time.

        \b
            TARGET: resource target URL
    """
    start = datetime.now()
    while True:
        now = datetime.now()
        time_delta = now - start
        if duration != 0 and time_delta.seconds >= duration:
            break
        failure = False
        before = datetime.now()
        r = requests.get(target, timeout=timeout)
        after = datetime.now()
        response_time = (after - before).microseconds
        if r.status_code != requests.codes.ok:
            failure = True
        if failure:
            logger.error(f"Failure: {response_time}")
        else:
            logger.info(f"Success: {response_time}")
        sleep(frequency)

    return 0


if __name__ == "__main__":
    main()
