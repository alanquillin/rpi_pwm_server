#!/usr/bin/env python

import logging
import os
import signal
import sys

try:
    import wiringpi
    HAS_WIRINGPI = True
except ImportError:
    HAS_WIRINGPI = False

from rpi_pwm_server import hub
from rpi_pwm_server import wsgi

LOG = logging.getLogger(__name__)

threads = []


def on_exit(sig, func=None):
    shutdown()
    sys.exit(0)


def shutdown():
    LOG.info('Shutting down server...')
    wsgi.stop()

    # Wait for all threads to shut down
    hub.joinall(threads)


def main():
    LOG.info('Starting up server... pid: %s', os.getpid())

    if not HAS_WIRINGPI:
        LOG.error('Required module \'wiringpi\' not found.')
        sys.exit(1)

    try:
        threads.append(hub.spawn(wsgi.run))

        # Keep main thread alive to capture kill events
        while True:
            hub.sleep(.1)
    except (KeyboardInterrupt, SystemExit):
        LOG.error('Caught KeyboardInterrupt, initiate shutdown')
    finally:
        shutdown()

signal.signal(signal.SIGTERM, on_exit)

if __name__ == '__main__':
    main()
