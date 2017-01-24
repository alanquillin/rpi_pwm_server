#!/usr/bin/env python

import logging

try:
    import wiringpi
    HAS_WIRINGPI = True
except ImportError:
    HAS_WIRINGPI = False

from rpi_pwm_server.exceptions import InvalidPWMValue
from rpi_pwm_server.exceptions import UnknownPWMNamedValue
from rpi_pwm_server.exceptions import UnknownMode

GPIO_PIN = 18  # needs to be 18 to utilize hardware PWM

HIGH = 1024
MHIGH = 768
MED = 512
MLOW = 256
LOW = 128
VLOW = 64
OFF = 0
ON = -1

pwm_named_values = dict(high=HIGH,
                        mhigh=MHIGH,
                        med_high=MHIGH,
                        medium_high=MHIGH,
                        med=MED,
                        medium=MED,
                        mlow=MLOW,
                        med_low=MLOW,
                        medium_low=MLOW,
                        low=LOW,
                        vlow=VLOW,
                        very_low=VLOW)

modes = dict(off=OFF, on=ON)


def str_to_named_value(str_):
    v = pwm_named_values.get(str_.lower())

    if v is None:
        raise UnknownPWMNamedValue(str_)

    return v


def str_to_mode(str_):
    m = modes.get(str_.lower())

    if m is None:
        raise UnknownMode(str_)

    return m


def get_mode(mode_val):
    if mode_val in [ON, OFF, str(ON), str(OFF)]:
        return int(mode_val)

    return str_to_mode(mode_val)


def get_pwm_value(val):
    if val is None:
        return None

    try:
        v = int(val)
        if v > HIGH or v < 0:
            raise InvalidPWMValue(val)
        return v
    except ValueError:
        return str_to_named_value(val)


def get_dict_key_for_value(d, val, def_val=None):
    if not d:
        return None

    for k, v in d.iteritems():
        if v == val:
            return k

    return def_val


class PWMCtl_(object):
    _current_pwm_value = None
    _current_mode = None

    def __init__(self):
        self.setup()

    def setup(self):
        if HAS_WIRINGPI:
            wiringpi.wiringPiSetupGpio()
            wiringpi.pinMode(GPIO_PIN, wiringpi.PWM_OUTPUT)

    def setmode(self, mode, pwm_value=None):
        mode = get_mode(mode)
        pwm_value = get_pwm_value(pwm_value)

        if mode == ON:
            if pwm_value is None:
                pwm_value = self._current_pwm_value
                if pwm_value is None:
                    pwm_value = MHIGH
            self._current_pwm_value = pwm_value
            pwm_value = pwm_value
        else:
            pwm_value = OFF

        self._current_mode = mode
        if HAS_WIRINGPI:
            wiringpi.pwmWrite(GPIO_PIN, pwm_value)

    def get_pwm_display_value(self):
        if self._current_pwm_value is None:
            return None

        return get_dict_key_for_value(pwm_named_values,
                                      self._current_pwm_value,
                                      def_val=self._current_pwm_value)

    def get_mode_display_value(self):
        if self._current_mode is None:
            return None

        return get_dict_key_for_value(modes, self._current_mode,
                                      def_val=self._current_mode)

PWMCtl = PWMCtl_()

if __name__ == '__main__':
    import argparse
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    LOG = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='Sets mode [On, Off]')
    parser.add_argument('-v', '--value', help='Sets PWM value for mode \'On\'')

    args = parser.parse_args()

    try:
        if not HAS_WIRINGPI:
            raise Exception('Required module \'wiringpi\' not found.')
        PWMCtl.setmode(args.mode, pwm_value=args.value)
    except Exception as ex:
        LOG.exception('An error occurred: %s' % ex.message)
        sys.exit(1)

else:
    LOG = logging.getLogger(__name__)
