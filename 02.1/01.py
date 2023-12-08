import psycopg2
import json
import xml.etree.ElementTree as ET
import concurrent.futures
import pytest


class Country:
    def __init__(self, name, rank, year, gdp_per_capita, neighbor):
        self.name = name
        self.rank = rank
        self.year = year
        self.gdp_per_capita = gdp_per_capita
        self.neighbor = neighbor

    def __str__(self):
        return f"Country: {self.name} \n\tRank: {self.rank}\n\tYear: {self.year}\n\tGDP per capita: {self.gdp_per_capita}\n\tNeighbour: {self.neighbor}"


def parse_xml(filename):
    """Parse the XML file and return a list of Country instances."""
    tree = ET.parse(filename)
    root = tree.getroot()

    countries = []
    for child in root:
        name = child.attrib['name']
        rank = child.find('rank').text
        year = child.find('year').text
        gdp_per_capita = child.find('gdppc').text
        neighbor = child.find('neighbor').attrib

        country = Country(name, rank, year, gdp_per_capita, neighbor)
        countries.append(country)

    return countries


def create_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="test",
        user="romantolmachev",
        password="admin"
    )
    return conn


def get_countries(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries")
    rows = cur.fetchall()
    return rows


def save_country(country, conn):
    cur = conn.cursor()
    neighbor_json = json.dumps(country.neighbor)
    try:
        cur.execute("""
                INSERT INTO countries (name, rank, year, gdp_per_capita, neighbor)
                VALUES (%s, %s, %s, %s, %s)
            """, (country.name, country.rank, country.year, country.gdp_per_capita, neighbor_json))
        conn.commit()
    except Exception as e:
        print(f'Error while inserting the row: {e}')
        conn.rollback()


if __name__ == '__main__':
    countries = parse_xml('data.xml')
    for country in countries:
        print(country)

    conn = create_conn()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(save_country, countries, [conn]*len(countries))

    countries_from_database = get_countries(conn)
    print("Countries from the database:")
    for row in countries_from_database:
        print(f"\t{row}")

    conn.close()


def test_countries():
    # Parse countries from XML file
    expected_countries = parse_xml('data.xml')

    # Save countries to the database
    conn = create_conn()
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(save_country, expected_countries,
    #                  [conn]*len(expected_countries))

    # Get countries from the database
    actual_countries = get_countries(conn)

    # Sort countries by rank
    expected_countries = sorted(expected_countries, key=lambda c: c.rank)
    # assuming rank is at index 2
    actual_countries = sorted(actual_countries, key=lambda c: c[2])

    # Compare the name and gdp per capita of each country
    for expected, actual in zip(expected_countries, actual_countries):
        actual_id, actual_name, actual_rank, actual_year, actual_gdp_per_capita, actual_neighbor = actual
        assert expected.name == actual_name
        assert int(expected.year) == actual_year
        assert float(expected.gdp_per_capita) == actual_gdp_per_capita

    conn.close()
