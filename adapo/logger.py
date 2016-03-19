"""
    Provides the adapo logger class
"""

import sys


class Logger(object):  # pylint: disable=too-few-public-methods
    """
        Adapo logger class
    """

    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    WARN = '\033[93m'
    ENDC = '\033[0m'
    INFO = ENDC

    def __getattr__(self, attr):

        def log_func(message):
            """Prints out log message.

            Args:
                message: Message to be printed out.
            """
            color = getattr(self, attr.upper())
            log_message = "{0}{1}: {2}{3}".format(
                color, attr, message, self.ENDC
            )

            print log_message
            sys.stdout.flush()

        return log_func
