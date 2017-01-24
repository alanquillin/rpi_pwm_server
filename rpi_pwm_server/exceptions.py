class UnknownPWMNamedValue(Exception):
    def __init__(self, brightness_str):
        msg = 'Unknown brightness \'%s\'' % brightness_str

        super(UnknownPWMNamedValue, self).__init__(msg)


class UnknownMode(Exception):
    def __init__(self, mode_str):
        msg = 'Unknown mode \'%s\'' % mode_str

        super(UnknownMode, self).__init__(msg)


class InvalidPWMValue(Exception):
    def __init__(self, value):
        msg = ("Invalid brightness value \'%s\'.  "
               "Value must be between 0 and 1024" % value)

        super(InvalidPWMValue, self).__init__(msg)
