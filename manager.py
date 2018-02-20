import locale
import os
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from gatpy import logging
from gatpy.config import get_data_dir
from gatpy.logging import logger
from gatpy.processor import Processor
from gatpy.gui.products import ProductsDialog
from ui.manager import Ui_MainWindow


app_root = os.path.dirname(os.path.abspath(sys.argv[0]))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setupUi(self)
        self.setFixedSize(300, 400)
        self.connectAll()

        logging.setStatusbar(self.statusBar)

    def connectAll(self):
        self.exportButton.clicked.connect(self.export)
        self.multiExportButton.clicked.connect(self.exportMultiple)
        self.manageProductsButton.clicked.connect(self.manageProducts)
        self.quitButton.clicked.connect(self.close)

    def export(self):
        date = -1
        for f in os.listdir(os.path.join(get_data_dir(), 'raw')):
            if date < int(f.split('_')[0]):
                date = int(f.split('_')[0])

        if date == -1:
            return logger.warn("Geen raw rapportage gevonden")

        proc = Processor(os.path.join(get_data_dir(), 'raw', '%s_raw.csv' % date))
        proc.process()
        os.startfile(proc.outfile)

        logger.info("Geëxporteerd naar %s_proc.csv" % str(date))

    def exportMultiple(self):
        files = QtGui.QFileDialog.getOpenFileNames(
            self,
            None,
            os.path.join(get_data_dir(), "raw"),
            "Ruwe verkoopdata (*.csv)")

        for file in files:
            proc = Processor(file).process()
            logger.info("%s verwerkt" % os.path.basename(file))

        if not files:
            logger.warn("Geen bestanden geselecteerd")

    def manageProducts(self):
        products = ProductsDialog(self)
        products.show()


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')

    log_dir = os.path.join(get_data_dir(), 'log')
    logging.init(log_dir)

    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    logger.info("Hallo!")
    sys.exit(app.exec_())
