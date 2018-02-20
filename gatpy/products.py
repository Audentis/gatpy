from collections import OrderedDict
import csv
import os

from gatpy.logging import logger


class Product:
    def __init__(self, name, price, group, category):
        self.name = name
        self.price = price
        self.group = group
        self.category = category


class Products:
    def __init__(self, filename=""):
        self.products = []

        if not os.path.exists(filename):
            logger.warn("Productdatabase niet gevonden (%s)" % filename)
            return

        self._filename = os.path.abspath(filename)
        with open(self._filename, 'r') as f:
            reader = csv.reader(f, dialect='excel_semicolon')
            for row in reader:
                if len(row) != 4:
                    continue
                product = Product(row[0], row[1], row[2], row[3])
                self.products.append(product)

        num_products = len(self.products)
        if num_products:
            logger.info("%d producten uit database ingeladen" % num_products)
        else:
            logger.warn("Productdatabase is leeg")

    def __len__(self):
        return len(self.products)

    def dict(self):
        return dict((product.name, product) for product in self.products)

    def category_dict(self):
        result = OrderedDict([])

        for product in self.products:
            if product.category not in result:
                result[product.category] = []
            result[product.category].append(product)

        return result

    def categories(self):
        return list(self.category_dict().keys())

    def names(self):
        return list(self.dict().keys())

    def groups(self):
        return set(product.group for product in self.products)

    def save(self, filename=None):
        if filename:
            self._filename = filename

        with open(self._filename, 'w') as f:
            writer = csv.writer(f, dialect='excel_semicolon')
            for product in self.products:
                writer.writerow([
                    product.name,
                    product.price,
                    product.group,
                    product.category
                ])

        logger.info("%d producten naar database weggeschreven" % len(self.products))

    def productIsInGroup(self, name, group):
        return self.dict()[name].group == group
