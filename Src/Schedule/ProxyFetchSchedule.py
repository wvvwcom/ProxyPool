# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
sys.path.append("Src")
import time
import threading
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler as Sch
from Manager.ProxyFetch import ProxyFetch
from Manager.ProxyManager import ProxyManager
from Log.LogManager import log

from Log.LogManager import log
from Config.ConfigManager import config

def fetch_new_proxy():
    proxy_manager = ProxyManager()
    total_number = proxy_manager.getRawProxyNumber()
    hold_number = config.setting.Hold.hold_raw_proxy_number
    if total_number < hold_number or hold_number == -1:
        log.debug("fetch new proxy start, exist raw_proxy total_number:{total_number}, hold_number:{hold_number}".format(total_number=total_number, hold_number=hold_number))

        ProxyFetch.initQueue()
        for _ in range(config.setting.Thread.fetch_new_proxy_thread):
            pf = ProxyFetch()
            pf.daemon = True
            pf.start()
    else:
        log.info("fetch new proxy skip, exist raw_proxy total_number:{total_number}, hold_number:{hold_number}".format(total_number=total_number, hold_number=hold_number))


def run():
    sch = Sch()
    now = datetime.datetime.now()
    sch.add_job(fetch_new_proxy, 'interval', id="fetch_new_proxy", minutes=config.setting.Interval.fetch_new_proxy_interval, next_run_time=now)
    sch.start()

if __name__ == '__main__':
    run()