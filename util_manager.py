from email.utils import localtime
import time


def getLocalTime():
    local_time = time.localtime()
    return "{}-{}-{} {}:{}:{}".format(localtime[0], localtime[1], localtime[2], localtime[3], localtime[4], localtime[5])


def tprint(print_str):
    print('{} :: {}'.format(getLocalTime(), print_str))
