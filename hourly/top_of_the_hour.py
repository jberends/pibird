#!/usr/bin/env python2

import os
import random
import subprocess
import sys
from datetime import datetime

import click
import pytz as pytz

MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
MEDIA_PATH = os.path.join(MEDIA_ROOT, "static", "sounds")
MEDIA_FILES = [
    "koe_0.wav",
    "koe_1.wav",
    "koe_2.wav",
    "koe_3.wav",
    "koe_4.wav",
    "koe_5.wav",
]
CMD = "aplay"

DEFAULT_START_HOUR = 8
DEFAULT_END_HOUR = 21
ACCURACY = 5  # minutes accuracy before and after the top of the hour or quarter


@click.command()
@click.option('--start', default=DEFAULT_START_HOUR, help="hour to start time window to be active")
@click.option('--end', default=DEFAULT_END_HOUR, help="hour to end time window to be active")
@click.option('--quarter/--no-quarter', default=False, help="run once on every quarter of an hour")
def main(**options):
    """This small python scripts runs wav files like your local churchclock.

    It will emulate a real clock: it will ring n times on the top of the hour.
    In the afternoon it starts at 1 again (at 13:00). When providing multiple wav files
    it randomise the selection from those files for every strike of the bell

    Optionally it can run with one strike every quarter of an hour.

    There is an accuracy built in of 5 minutes. So 5 mins before or after the top of the hour or quarter
    of an hour, the script will still be run.

    You may install a cron.d entry to run once every 15 minutes using the following cron line:

    `*/15 * * * *  root  /path/to/script/top_of_the_hour.py --start 8 --end 21 --quarter`
    """
    now = datetime.now(tz=pytz.timezone('Europe/Amsterdam'))
    print("___")
    print("___ running at: {}".format(now))
    hour = now.hour
    minute = now.minute

    is_top_of_the_hour = (minute + ACCURACY) % 60 <= 2 * ACCURACY
    is_quarter_of_an_hour = (minute + ACCURACY) % 15 <= 2 * ACCURACY
    in_time_window = hour >= options.get('start', DEFAULT_START_HOUR) and hour <= options.get('end', DEFAULT_END_HOUR)

    if in_time_window and is_top_of_the_hour:
        # do the cow between 8 and 21 every top of the hour

        # correct for afternoon.
        if hour > 12:
            hour = hour - 12

        print("___ running top of the hour. Play sound {} times".format(hour))

        for x in range(0, hour):
            # when hour = 5 , the range will be provided: [0,1,2,3,4] (so 5 times, 5 is not in there)
            subprocess.call([CMD, os.path.join(MEDIA_PATH, random.choice(MEDIA_FILES))])

    elif in_time_window and options.get('quarter', False) and is_quarter_of_an_hour:
        print("___ running quarter of the hour. Play sound 1 times")
        subprocess.call([CMD, os.path.join(MEDIA_PATH, random.choice(MEDIA_FILES))])
    elif not in_time_window:
        print("_!_ not in time window between {}:00 and {}:00".format(options.get('start', DEFAULT_START_HOUR),
                                                                      options.get('end', DEFAULT_END_HOUR)))
    else:
        print("_!_ not top of the hour, nor quarter")
    print("___ Done.")

if __name__ == '__main__':
    sys.exit(main())
