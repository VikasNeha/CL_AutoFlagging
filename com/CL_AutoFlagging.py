import logging
import sys
from Utilities import myLogger
from Main import inputContent
from Main import FlagAllAds
import imp
import os

module_logger = logging.getLogger('main')


def main():
    # noinspection PyBroadException
    try:
        readAllInput()
        FlagAllAds.flagAllAds()
    except:
        module_logger.exception(sys.exc_info())
    finally:
        inputContent.writeResults()
        return 1


def readAllInput():
    inputContent.readProxies()
    inputContent.readAds()


def main_is_frozen():
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers")  # old py2exe
            or imp.is_frozen("__main__"))  # tools/freeze


def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(os.path.dirname(sys.executable))
    return os.path.dirname(sys.argv[0])


if __name__ == '__main__':
    main()
