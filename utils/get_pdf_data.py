"""
Method which extract tables from provided pdf
author: iflorea
date: 10/10/2020
"""

from camelot import read_pdf
import pandas as pd
import logging


class TablesFromPDF(object):

    def __init__(self, pdf_path):
        self.pdf_tables = read_pdf(pdf_path, pages="all", stream=True)

    def get_tables(self):
        """
        Get founded tables

        :return: list of tables
        """
        return self.pdf_tables

    def get_tables_number(self):
        """
        Get number of tables found on provided pdf

        :return: number of founded tables
        """
        logging.info("Total number of tables: {}".format(len(self.pdf_tables)))
        return len(self.pdf_tables)

    def get_distinct_tables(self, selector="specialitatea"):
        """
        Return distinct tables from pdf. Merge a splited table from two pages

        :return:list of tables
        """
        tables = self.remove_unnecessary_tables()
        new_tables = []
        for i, table in enumerate(tables):
            try:
                if table[0][0] != tables[i + 1][0][0]:
                    if tables[i + 1][0][0].lower() != selector:
                        logging.info("Concatenate Table{} with Table{}.".format(i, i+1))
                        table = pd.concat([tables[i], tables[i + 1]], ignore_index=True)
                        new_tables.append(table)
                else:
                    new_tables.append(table)
            except IndexError:
                if table[0][0].lower() == selector:
                    new_tables.append(table)

        return new_tables

    def remove_unnecessary_tables(self, columns=14):
        """
        Remove table with different columns than provided number

        :param columns: reference number of columns
        :return: list of tables
        """
        tables = []
        for table in self.get_tables():
            if len(table.df.columns) == columns:
                tables.append(table.df)
        return tables



