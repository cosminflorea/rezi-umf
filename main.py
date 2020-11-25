import streamlit as st
from data import pdf_files
from displaydata.sidebar import SideBar
from displaydata.build_view import BuildView
import cv2

st.set_page_config(
    page_title="Rezidențiat",
    initial_sidebar_state="expanded",
    layout="wide")


def main():
    st.title("Comparație locuri disponibile Rezidențiat Medicină")

    sidebar = SideBar()
    build_view = BuildView()
    years = list(pdf_files.keys())
    selected_years = sidebar.year_selector(years)
    selected_domain = sidebar.domain_selectbox()

    table, plots, details = sidebar.checkbox_displays()

    if not selected_domain:
        st.warning("Niciun domeniu nu este selectat!")

    build_view.display_tables(selected_years, selected_domain, display=table)
    filtered_specialities = build_view.get_filtered_specialities()
    speciality, all_specialities, top10 = sidebar.specialities_selector(specialities=filtered_specialities)
    cities = build_view.get_filtered_cities()
    cities_option, all_cities = sidebar.cities_selector(cities)
    if all_cities:
        cities_option = cities
    else:
        cities_option = [cities_option]

    if top10 is True:
        build_view.top10_table(selected_years, cities_option, selected_domain)
    if all_specialities:
        speciality = filtered_specialities

    if plots is True:
        build_view.bar_graph_specialities_availability(selected_years, cities_option, speciality)
    else:
        st.warning("Afișarea graficelor nu este selectată!")
    if details is True:
        build_view.write_details(selected_years, cities_option, speciality, selected_domain)
    else:
        st.warning("Afișarea detaliilor nu este selectată!")


if __name__ == "__main__":
    main()

