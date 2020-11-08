import streamlit as st
from utils.tables_handler import TableHandle
from data import pdf_files
import altair as alt
import pandas as pd


class BuildView(object):

    def __init__(self):
        self.table_handler = TableHandle()
        self.filtered_table = []
        self.filtered_specilities = []

    @staticmethod
    def __filter_tables(table_list, domain):
        for table in table_list:
            table_domain = table.get_table_domain()
            if table_domain == domain:
                return table

    def display_tables(self, years, domain, display=True):
        """
        Display tables with title which contain year and domain

        :param years: list of years of table
        :param domain: selected domain
        :param display: display data
        :return: list of FilterTableData object filtered by domain and years
        """
        if not years:
            st.warning("Niciun an nu este selectat!")
            self.filtered_table = []
        else:
            if display:
                if years == list(pdf_files.keys()):
                    st.title("Tabele Rezidentiat: {}-{}".format(years[0], years[-1]))
                else:
                    if len(years) > 1:
                        years_str = ", ".join(map(str, years))
                        st.title("Tabele Rezidentiat pentru anii: {}".format(years_str))
                    else:
                        st.title("Tabele Rezidentiat pentru anul: {}".format(*years, sep=""))
            else:
                st.warning("Afișarea tabelelor nu este selectată!")

            for year in years:
                table_list = self.table_handler.get_tables_by_year(year)
                table = BuildView.__filter_tables(table_list, domain)
                self.filtered_table.append({year: table})
                if display:
                    with st.beta_expander("Expandează/Restrânge secțiunea", expanded=True):
                        st.title(year)
                        st.write(domain)
                        st.write(table.get_table())

    def get_filtered_specialities(self):
        """
        Get filtered specialities by selected years and domains

        :return: list of distinct specialities
        """
        self.filtered_specilities = []
        filtered = []
        for table in self.filtered_table:
            table = list(table.values())[0]
            filtered.extend(table.get_specialities())
        self.filtered_specilities.extend(list(set(filtered)))
        return sorted(self.filtered_specilities, key=str.lower)

    def get_filtered_cities(self):
        """
        Get filtered cities by years and domains

        :return: list of distinct cities
        """
        distinct_cities = []
        for table in self.filtered_table:
            table = list(table.values())[0]
            distinct_cities.extend(list(table.get_cities()))
        return sorted(list(set(distinct_cities)), key=str.lower)

    def __filter_available_specialities_by_year(self, years, cities, specialities):
        """
        Get filtered data table by years, cities and specialities

        :param years: selected years
        :param cities: selected city / all cities
        :param specialities: list of selected specialities
        :return: DataFrame object
        """
        # create dataframe
        custom_columns = ["An", "Oraș", "Specialitate", "Locuri disponibile"]
        row_list = []
        for year in years:
            for city in cities:
                for speciality in specialities:
                    for table in self.filtered_table:
                        if list(table.keys())[0] == year:
                            table = list(table.values())[0]
                            row = [year, city, speciality]
                            available_place = table.get_speciality_availability_by_city(speciality, city)
                            row.append(available_place)
                            row_list.append(row)
                        continue
        return pd.DataFrame(row_list, columns=custom_columns)

    def bar_graph_specialities_availability(self, years, cities, specialities):
        """
        Plot bar graph of available specialites from selected cities.

        :param years: selected years
        :param cities: selected city / all cities
        :param specialities: list of selected specialities
        """

        if len(specialities) == 0:
            st.warning("Nicio specialitate nu a fost selectă")
            return
        st.title("Grafice comparative")
        df = self.__filter_available_specialities_by_year(years, cities, specialities)
        if len(years) > 1:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Oraș:N', axis=alt.Axis(title='Oraș')),
                y=alt.Y('Locuri disponibile:Q', axis=alt.Axis(grid=False, title='Locuri disponibile'), sort="-x"),
                column=alt.Column('An:N'),
                color=alt.Color('Specialitate:N'),
                tooltip=['Specialitate:N', 'Locuri disponibile:Q', 'Oraș:N']
            )
            st.altair_chart(chart)
        else:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Locuri disponibile:Q', axis=alt.Axis(grid=False, title='Locuri disponibile'), sort="-x"),
                y=alt.Y('Oraș'),
                color=alt.Color('Specialitate:N'),
                tooltip=['Specialitate:N', 'Locuri disponibile:Q', 'Oraș:N']
            )
            st.altair_chart(chart)

    def write_details(self, years, cities, specialities, domain):
        """
        Write details for selected date

        :param years: list of years
        :param cities: list of cities
        :param specialities: list of specialities
        :param domain: domain of the table
        """
        st.title("Detalii despre informațiile selectate")
        with st.beta_expander("Expandează/Restrânge secțiunea", expanded=True):
            if not years or not cities or not specialities:
                st.warning("Selectați datele pentru a afișa informațiile")
            df = self.__filter_available_specialities_by_year(years, cities, specialities)
            for year in years:
                st.header("Anul: **{}**".format(year))
                tables = self.table_handler.get_tables_by_year(year)
                my_table = self.table_handler.get_table_using_domain(tables, domain)
                total_availability = my_table.get_total_availability()
                text = ":star2: Numar total de locuri pentru anul *{}* pentru domeniul *{}* este **{}**"
                st.write(text.format(year, domain, total_availability))

                if len(specialities) == 0:
                    st.warning("Selectați cel puțin o specialitate")
                else:
                    total_per_speciality = ":star: Pentru specialitatea selectata **{}** din orașul **{}** " \
                                           "avem disponibile **{}** locuri."
                    for city in cities:
                        st.subheader("Orașul: **{}**".format(city))
                        for speciality in specialities:
                            for i in df.index:
                                if (df.loc[i, "Specialitate"] == speciality) and (df.loc[i, "Oraș"] == city) and (
                                        df.loc[i, "An"] == year):
                                    st.write(
                                        total_per_speciality.format(speciality, city, df.loc[i, "Locuri disponibile"]))
                                continue

    def top10_table(self, years=None, cities=None, domain=None):
        """
        Print top <values> of available places

        :param years: list of years to display
        :param cities: list of cities to display
        :param domain: domain of the table
        """

        st.title("Tabele Top 10 pentru {}".format(domain))
        with st.beta_expander("Expandează/Restrânge secțiunea", expanded=True):
            for year in years:
                tables = self.table_handler.get_tables_by_year(year)
                my_table = self.table_handler.get_table_using_domain(tables, domain)
                st.header("Anul: {}".format(year))
                if len(cities) > 1:
                    st.header("Top 10: specialități cele mai multe locuri".format(year))
                    st.write(my_table.get_top_specialities_by_available_places())
                    st.header("Top 10: specialități cele mai puține locuri".format(year))
                    st.write(my_table.get_top_specialities_by_available_places(ascending=True))
                else:
                    city = cities[0]
                    st.subheader("Oraș: {}".format(city))
                    col1, col2 = st.beta_columns(2)
                    col1.subheader("Top 10: specialități cele mai multe locuri")
                    col1.write(my_table.get_top_specialities_by_available_places_in_a_city(city=city))
                    col2.subheader("Top 10: specialități cele mai puține locuri")
                    col2.write(my_table.get_top_specialities_by_available_places_in_a_city(city=city, ascending=True))
