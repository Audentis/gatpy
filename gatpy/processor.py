import csv
import locale
import os

from gatpy.config import get_data_dir
from gatpy.products import Products

class Processor:
    def __init__(self, infile, outfile=None):
        self.infile = infile
        self.outfile = outfile if outfile else self.defaultFilename()
        self.products = Products(os.path.join(get_data_dir(), "products.csv"))

        if not os.path.exists(self.infile):
            logger.error("Kon rawX niet vinden (%s)" % infile)

    def defaultFilename(self):
        filename = os.path.basename(self.infile).replace('raw.csv', 'proc.csv')
        return os.path.join(get_data_dir(), 'proc', filename)

    def process(self):
        self.processInfile()
        self.generateOutfile()

    def processInfile(self):
        self.entries = {}
        self.modes = []
        self.comments = []

        with open(self.infile, 'r') as f:
            reader = csv.reader(f, dialect='excel_semicolon')

            productNames = next(reader)

            for row in reader:
                self.lastTime = row[0]
                mode = row[1]

                if mode == 'comment':
                    self.comments.append((row[0], row[2]))
                    continue

                if mode not in self.modes:
                    self.modes.append(mode)

                for i, product in enumerate(row[2:]):
                    if product == "0":
                        continue
                    name = productNames[i + 2]
                    if name not in self.entries:
                        self.entries[name] = {}
                    if mode not in self.entries[name]:
                        self.entries[name][mode] = 0
                    self.entries[name][mode] += int(product)

    def generateOutfile(self):
        with open(self.outfile, 'w') as f:
            writer = csv.writer(f, dialect='excel_semicolon')

            writer.writerow(['Laatste', self.lastTime])
            writer.writerow([])

            writer.writerow(['Opmerkingen'])
            for comment in self.comments:
                writer.writerow([comment[0], comment[1]])
            writer.writerow([])

            row = ['']
            for mode in self.modes:
                row.extend(['%s aantal' % mode, '%s omzet' % mode])
            row.extend(['','groep totaal'])
            writer.writerow(row)

            totalAmount = 0
            totalPrice = 0
            for group in self.products.groups():	
                totalGroupPrice = 0
                row = [group.capitalize()]
                for mode in self.modes:
                    amount, price = self.getAllInGroup(group, mode)
                    row.extend([amount, locale.currency(price)])
                    if mode == 'cash' or mode == 'pin':
                        totalAmount += amount
                        totalPrice += price
                        totalGroupPrice += price 
                row.extend([''])
                row.extend([locale.currency(totalGroupPrice)])
                writer.writerow(row)
            writer.writerow([])
            writer.writerow(['Totaal', totalAmount, locale.currency(totalPrice)])

            writer.writerow([])

            row = ['']
            for mode in self.modes:
                row.extend(['%s aantal' % mode, '%s omzet' % mode])
            writer.writerow(row)
            for name, entry in self.entries.items():
                row = [name]
                for mode in self.modes:
                    amount = entry[mode] if mode in entry else 0
                    price = amount * float(self.products.dict()[name].price)
                    row.extend([amount, locale.currency(price)])
                writer.writerow(row)

    def getAllInGroup(self, group, mode):
        amount = 0
        price = 0

        for name, entry in self.entries.items():
            if self.products.productIsInGroup(name, group):
                a = entry[mode] if mode in entry else 0
                amount += a
                price += a * float(self.products.dict()[name].price)

        return amount, price
