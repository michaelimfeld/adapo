#!/usr/bin/python

class Logger(object):
    """
        tiny logger
    """

    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    WARN = '\033[93m'
    ENDC = '\033[0m'

    def info(self, message):
        """
            print info message
        """
        print "info: %s" % message

    def warn(self, message):
        """
            print warn message
        """
        print "%swarn: %s" % (self.WARN, message + self.ENDC)

    def error(self, message):
        """
            print error message
        """
        print "%serror: %s" % (self.ERROR, message + self.ENDC)

    def success(self, message):
        """
            print success message
        """
        print "%ssuccess: %s" % (self.SUCCESS, message + self.ENDC)
