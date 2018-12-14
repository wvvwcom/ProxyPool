# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
sys.path.append("Src")
import time
import threading
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler as Sch
from Manager.ProxyClean import ProxyCleanRaw, ProxyCleanUseful
from Manager.ProxyFetch import ProxyFetch

try:
    from Queue import Queue  # py3
except:
    from queue import Queue  # py2

from Log.LogManager import log
from Config.ConfigManager import config

def clean_raw_proxy():
    t = ProxyCleanRaw()
    t.daemon = True
    t.start()


def clean_useful_proxy():
    t = ProxyCleanUseful()
    t.daemon = True
    t.start()

def run():
    sch = Sch()
    now = datetime.datetime.now()
    sch.add_job(clean_raw_proxy, "interval", id="clean_raw_proxy", minutes=config.setting.Interval.clean_raw_proxy_interval, next_run_time=now)
    sch.add_job(clean_useful_proxy, "interval", id="clean_useful_proxy", minutes=config.setting.Interval.clean_useful_proxy_interval, next_run_time=now)
    sch.start()

if __name__ == '__main__':
    run()