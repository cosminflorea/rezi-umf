from data import pdf_files
from utils.get_pdf_data import TablesFromPDF
from utils.filter_table_data import FilterTableData
import logging


class TableHandle(object):

    def __init__(self):
        self.pdfs_dict = pdf_files

    def get_tables_by_year(self, year):
        """
        Return list of FilterTableData by year

        :param year: year
        :return: list of FilterTableData object
        """

        pdf_path = self.pdfs_dict.get(year)
        tables = TablesFromPDF(pdf_path).get_distinct_tables()
        filtered_tables = []
        for t in tables:
            filtered_tables.append(FilterTableData(t))
        return filtered_tables

    @staticmethod
    def get_table_using_domain(list_of_tables, domain):
        """
        Get table from a list of tables using domain

        :param list_of_tables: list of FilterTableData objects
        :param domain: domain of the speciality
        :return: FilterTableData object if domain exists, None otherwise
        """
        for table in list_of_tables:
            if domain in table.get_table_domain():
                return table

