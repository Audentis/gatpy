import logging
import logging.handlers
import os
import sys

FMT = '%(asctime)s %(levelname)-8s %(message)s'
DATEFMT = '%Y-%m-%d %H:%M'
logger = logging.getLogger()


def init(path):
    logging.basicConfig(format=FMT,
                        datefmt=DATEFMT,
                        level=logging.INFO,
                        stream=sys.stdout)

    file = logging.handlers.RotatingFileHandler(
        os.path.join(path, 'gatpy.log'),
        maxBytes=1024*1024,
        backupCount=5)
    formatter = logging.Formatter(FMT, DATEFMT)
    file.setFormatter(formatter)
    logger.addHandler(file)


class StatusbarHandler(logging.Handler):
    def __init__(self, statusBar, level=logging.NOTSET):
        self.statusBar = statusBar
        super(StatusbarHandler, self).__init__(level)

    def emit(self, record):
        self.statusBar.showMessage(self.format(record))


def setStatusbar(ui):
    statusbar = StatusbarHandler(ui)
    formatter = logging.Formatter('%(asctime)s | %(message)s', '%H:%M:%S')
    statusbar.setFormatter(formatter)
    logger.addHandler(statusbar)
