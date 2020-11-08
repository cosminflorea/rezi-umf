import streamlit as st
from utils.filter_table_data import FilterTableData


class SideBar(object):

    def __init__(self):
        self.sidebar = st.sidebar
        self.sidebar.title("Configurează datele")

    def year_selector(self, list_of_years):
        """
        Select desired year to view data

        :param list_of_years: list of string representing years
        :return: selected data
        """
        self.sidebar.write("Selectează anul rezidențiatului")
        years = self.sidebar.multiselect("An", list_of_years)
        return years

    def checkbox_displays(self):
        """
        Checkbox for displaying desired data

        :return: tuples of selected checkboxes
        """
        self.sidebar.write("Selectează ce dorești să afișezi:")
        table = self.sidebar.checkbox("Tabel", value=False)
        plots = self.sidebar.checkbox("Grafice", value=False)
        details = self.sidebar.checkbox("Detalii", value=False)
        return table, plots, details

    def domain_selectbox(self):
        """
        SelectBox for domains

        :return: list of selected domains
        """
        self.sidebar.write("Selectează un domeniu:")
        selector_list = self.sidebar.selectbox("Domeniu", [FilterTableData.medicina_generala,
                                                           FilterTableData.medicina_dentara,
                                                           FilterTableData.medicina_farmaceutica], key=None)
        return selector_list

    def specialities_selector(self, specialities):
        """
        Select specialities to display data

        :return: list of selected specialities
        """
        self.sidebar.write("Selectează una sau mai multe specialități")
        option = self.sidebar.multiselect("Specialitate", specialities)
        all_specialities = self.sidebar.checkbox("Toate specialitățile", value=False)
        top10 = None
        if all_specialities is True:
            top10 = self.sidebar.checkbox("Top 10 specialități", value=False)
        return option, all_specialities, top10

    def cities_selector(self, list_of_cities):
        """
        Select desired city to view data

        :param list_of_cities: list of string representing cities

        :return: tuple of selected cities and all cities selected
        """
        self.sidebar.write("Selectează orasul rezidențiatului")
        option = self.sidebar.selectbox("Oras", list_of_cities, key=None)
        all_cities = self.sidebar.checkbox("Toate orasele", value=False)
        return option, all_cities
