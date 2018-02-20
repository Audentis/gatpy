import csv


class excel_semicolon(csv.excel):
    delimiter = ';'
    lineterminator = '\n'


csv.register_dialect('excel_semicolon', excel_semicolon)
