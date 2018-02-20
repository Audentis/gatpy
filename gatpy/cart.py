import csv
from datetime import datetime, timedelta
import os
import time

from gatpy.config import get_data_dir
from gatpy.logging import logger


class Method:
    CASH = 'cash'
    PIN = 'pin'
    EV = 'ev'
    NABORREL = 'naborrel'


class Cart:
    INPUT = 1
    CHECKED_OUT = 2

    def __init__(self, productDb, date=None):
        self.productDb = productDb
        self.setFile(date)
        self.clear()

    def add(self, num, product):
        subtotal = num * float(product.price)
        self.contents.append((num, product.name, subtotal))

    def clear(self):
        self.contents = []
        self.state = Cart.INPUT

    def total(self):
        num_products = 0
        amount = 0.0

        for entry in self.contents:
            num_products += entry[0]
            amount += entry[2]

        return (num_products, amount)

    def checkOut(self, method):
        self.addToFile(method)
        self.state = Cart.CHECKED_OUT

    def negate(self):
        new_contents = []

        for entry in self.contents:
            new_contents.append((-entry[0], entry[1], -entry[2]))

        self.contents = new_contents

    def isCheckedOut(self):
        return self.state == Cart.CHECKED_OUT

    def isEmpty(self):
        return len(self.contents) == 0

    def addToFile(self, method):
        row = [0] * (len(self.productDb) + 2)
        row[0] = time.strftime('%H:%M:%S')
        row[1] = method

        with open(self.filename, 'r') as f:
            reader = csv.reader(f, dialect='excel_semicolon')
            headerrow = next(reader)

        with open(self.filename, 'a') as f:
            writer = csv.writer(f, dialect='excel_semicolon')
            for entry in self.contents:
                idx = -1
                for i, name in enumerate(headerrow):
                    if name == entry[1]:
                        idx = i
                        break
                if idx == -1:
                    logger.warn('Het product %s is niet gevonden in de rawX' % entry[1])
                    return
                row[idx] += entry[0]
            writer.writerow(row)

    def addCommentToFile(self, comment):
        with open(self.filename, 'a') as f:
            writer = csv.writer(f, dialect='excel_semicolon')
            writer.writerow([time.strftime('%H:%M:%S'), 'comment', comment])

    def makeFile(self):
        with open(self.filename, 'w') as f:
            writer = csv.writer(f, dialect='excel_semicolon')
            header = ['', '']
            header.extend(self.productDb.names())
            writer.writerow(header)

    def setFile(self, date):
        if not date:
            date = self.defaultDate()

        self.filename = os.path.join(get_data_dir(), 'raw', '%s_raw.csv' % date.strftime('%Y%m%d'))

        if not os.path.exists(self.filename):
            self.makeFile()

        logger.info("Uitvoer naar %s" % self.filename)

    def defaultDate(self):
        today = datetime.now()

        if today.hour < 10:
            today -= timedelta(days=1)

        return today
