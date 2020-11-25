import pandas as pd
import logging
from unidecode import unidecode


class FilterTableData(object):

    medicina_generala = "DOMENIUL MEDICINĂ"
    medicina_dentara = "DOMENIUL MEDICINĂ DENTARĂ"
    medicina_farmaceutica = "DOMENIUL FARMACEUTIC"

    domains = {"farmacie clinica": medicina_farmaceutica,
               "chirurgie dento-alveolara": medicina_dentara,
               "neurologie": medicina_generala}

    def __init__(self, table):
        self.table = self.__set_header_and_index(table)
        self.normalize()

    def get_table(self):
        """
        Return table
        :return: table object
        """
        return self.table

    @staticmethod
    def __set_header_and_index(table):
        """
        Set Header and index for current table

        :return table: table
        """
        new_header = table.iloc[0]  # grab the first row for the header
        table = table[1:]  # take the data less the header row
        table.columns = new_header  # set the header row as the df header
        table = table.set_index(table.columns[0])
        return table

    def normalize(self):
        """
        Remove romanian characters, double spaces or spaces after comma
        """
        # normalize specialities
        specialities = self.table.index.values[:-1]
        specialities = [unidecode(s) for s in specialities]
        specialities = [s.replace("  ", " ").replace(", ", ",").replace("\n", "") for s in specialities]
        self.table.index.values[:-1] = specialities

        # normalize cities
        cities = self.table.columns.values[:-1]
        cities = [unidecode(c.upper()) for c in cities]
        self.table.columns.values[:-1] = cities

    def get_cities(self):
        """
        Get list of cities from the header of the table

        :return: list of cities
        """
        cities = self.table.columns.values[:-1]
        logging.info("Cities founded: {}".format(cities))
        return cities

    def get_specialities(self):
        """
        Return list of specialities

        :return: list of specialities
        """
        specialitites = self.table.index.values[:-1]
        logging.info("Specialities founded: {}".format(specialitites))
        return specialitites

    def get_total_availability(self):
        """
        Return available places for all specialities

        :return: number of available places for all specialities
        """
        total_column = self.table.columns[-1]
        total_row = self.table.index[-1]
        total = self.table.loc[total_row, total_column]
        logging.info("Total available places: {}".format(total))
        return total

    def get_speciality_total_availability(self, speciality):
        """
        Get total number of available places in all cities for a provided speciality

        :param speciality: desired speciality
        :return: number of available places for provided speciality
        """
        all_specialities = self.get_specialities()
        if speciality not in all_specialities:
            total_speciality_places = 0
        else:
            total_column = self.table.columns[-1]
            total_speciality_places = self.table.at[speciality, total_column]
            logging.info("Total available places for speciality: {} are {}"
                         .format(speciality, total_speciality_places))
        return total_speciality_places

    def get_speciality_availability_by_city(self, speciality, city):
        """
        Get total number of available places in a city for a provided speciality

        :param speciality: desired speciality
        :param city: location where to search
        :return: number of available places in a city for provided speciality
        """
        all_specialities = self.get_specialities()
        all_cities = self.get_cities()
        if speciality in all_specialities and city in all_cities:
            total_speciality_places = self.table.at[speciality, city]
            logging.info("Total available places for speciality: {} in city: {} are {}"
                         .format(speciality, city, total_speciality_places))
        else:
            total_speciality_places = 0

        return total_speciality_places

    def get_table_domain(self):
        """
        Get domain of the table

        :return: domain for table
        """
        all_specialities = self.get_specialities()
        for key, value in self.domains.items():
            if key in all_specialities:
                logging.info("This table has domain: {}.".format(value))
                return value
        raise Exception("No domain found for the table: {} ".format(self.table))

    def get_top_specialities_by_available_places_in_a_city(self, city=None, top=10, ascending=False):
        """
        Get top <n> available place sorted from a city

        :param city: filter data from city
        :param top: number of returned value
        :param ascending: sort ascending or not
        :return: DataFrame table
        """

        self.table = self.table[0:-1]
        table = self.get_table()
        table = table[[city]]
        table[city] = pd.to_numeric(table[city])  # convert values to numeric
        return table.sort_values(by=[city], ascending=ascending).head(top)

    def get_top_specialities_by_available_places(self, top=10, ascending=False):
        """
        Get top <n> available place sorted by Total

        :param top: number of returned value
        :param ascending: sort ascending or not
        :return: DataFrame table
        """
        last_column = self.table.columns[-1]
        self.table = self.table[0:-1]
        table = self.get_table()
        table[last_column] = pd.to_numeric(table[last_column])  # convert values to numeric
        return table.sort_values(by=[last_column], ascending=ascending).head(top)


