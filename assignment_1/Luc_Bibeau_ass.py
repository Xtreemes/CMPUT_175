"""
Author: Luc Bibeau
"""


# Classes

class Country:
    _countries = {}

    @staticmethod
    def from_country_code(country_code: str):
        return Country._countries.get(country_code, None)

    def __init__(self, country_code: str, name: str, imports: float, exports: float):
        self._country_code = country_code
        self._name = name
        self._imports = imports
        self._exports = exports

        self._countries[country_code] = self  # store instance statically to fetch by id

    def get_deficit(self):
        return round(self._imports - self._exports, 2)

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name


class Product:

    def __init__(self, pid: str, industry: str, product_name: str, country_prices: list[tuple]):
        self._pid = pid
        self._industry = industry
        self._name = product_name
        self._country_prices = country_prices

    def get_id(self):
        return self._pid

    def get_industry(self):
        return self._industry

    def get_producers(self):
        return self._country_prices

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name


# Methods

def read_file(filename):
    """
    Opens a file and returns an array (two dimensional if 2+ columns).
    Splits lines by comma and trims any leading or trailing whitespaces.
    """

    with open(filename, 'r') as file:
        lines = file.read().splitlines()

        # check if further processing for 2d arrays is required
        if "," in lines[0]:
            for k, v in enumerate(lines):
                split_line = v.split(",")

                for i, entry in enumerate(split_line):
                    split_line[i] = entry.strip()

                lines[k] = split_line

        return lines


def load_countries(filename):
    """
    Loads countries from a given file
    :param filename: str, file to load
    :return: list[Country]
    """
    data = read_file(filename)
    data.pop(0)  # get rid of header line

    countries = []

    for entry in data:
        country = Country(entry[0], entry[1], float(entry[2]), float(entry[3]))
        countries.append(country)

    return countries


def load_products(products_filename, products_country_filename):
    """
    Loads products from a given file
    :param products_filename: str, file detailing products
    :param products_country_filename: str, file detailing product by country
    :return:
    """

    product_countries = {}

    data = read_file(products_country_filename)
    data.pop(0)  # pop header

    for entry in data:
        key = entry[0]
        country_code = entry[1]
        price = entry[2]

        if key not in product_countries:
            product_countries[key] = []

        product_countries[key].append(
            (country_code, price)
        )

    data = read_file(products_filename)
    data.pop(0)

    products = []

    for entry in data:
        pid = entry[0]
        product = Product(pid, entry[1], entry[2], product_countries[pid])
        products.append(product)

    return products


def get_column_sizes(headers, info, prepostfixes):
    """
    Gets the maximum length of each column
    :param headers: list[str], list of headers
    :param info: list[list[?]], data
    :param prepostfixes: list[str], list of pre or postfixes. used for spacing (i.e. $)
    :return: list[int], max lengths
    """
    columns = len(headers)
    max_sizes = []

    for i in range(columns):
        max_sizes.append(len(headers[i]))

    for i in range(columns):
        # the pre/postfix needs to be accounted for in the values
        # to ensure the smallest length possible can be used
        # when printing the table.

        prepostfix = len(prepostfixes[i])
        for entry in info:
            length = len(entry[i]) + prepostfix
            if length > max_sizes[i]:
                max_sizes[i] = length

    return max_sizes


def get_table_strings(headers, column_sizes):
    """
    Gets a formatted string for the headers
    and splitter (line to close table)
    :param headers: list[str], headers
    :param column_sizes: list[int], column sizes
    :return: tuple(str), header and splitter (respectively)
    """

    formatted_header = "|"
    for i, header in enumerate(headers):
        formatted_header += f" {header:<{column_sizes[i]}} |"

    splitter = "-" * len(formatted_header)

    return f"{splitter}\n{formatted_header}\n{splitter}", splitter


def display_trade_deficits(countries):
    headers = ("Country", "Trade Deficit (Billions USD)")
    countries_sorted = sorted(countries, key=lambda x: x.get_deficit(), reverse=True)

    sorted_info = []
    for country in countries_sorted[0:5]:
        sorted_info.append((str(country), f"{country.get_deficit():.2f}"))

    sizes = get_column_sizes(
        headers,
        sorted_info,
        ("", "$ ")
    )

    header_string, splitter = get_table_strings(headers, sizes)

    print(header_string)
    for entry in sorted_info:
        name = entry[0]
        print(f"| {name:<{sizes[0]}} | $ {entry[1]:>{sizes[1] - 2}} |")  # remove for the "$ "

    print(splitter)


def display_products_per_industry(products_per_industry):
    headers = ("Industry", "Number of Products")
    sorted_keys = sorted(products_per_industry, key=lambda x: x[0])

    sorted_info = []
    for key in sorted_keys:
        sorted_info.append((key, str(products_per_industry[key])))

    sizes = get_column_sizes(
        headers,
        sorted_info,
        ("", "")
    )
    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in sorted_info:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} |")
    print(splitter)


def display_exclusive_products(products):
    headers = ("PID", "Product Name", "Producing Country")
    products_sorted = sorted(products, key=lambda x: str(x))  # sort by name

    sorted_info = []
    for product in products_sorted:
        producing_country_id = product.get_producers()[0][0]  # first producer, country code

        producing_country = Country.from_country_code(producing_country_id)
        if producing_country: # may return None if country code not found.
            sorted_info.append((
                product.get_id(), str(product), str(producing_country)
            ))

    sizes = get_column_sizes(
        headers, sorted_info, ("", "", "")
    )

    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in sorted_info:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:<{sizes[1]}} | {entry[2]:<{sizes[2]}} |")
    print(splitter)

def main():
    # Section A

    countries = load_countries("country.txt")
    display_trade_deficits(countries)

    # Section B
    print()

    products_per_industry = {}
    exclusive_products = []

    products = load_products("product.txt", "product_country.txt")
    for product in products:
        industry = product.get_industry()
        if industry not in products_per_industry:
            products_per_industry[industry] = 1
        else:
            products_per_industry[industry] += 1

        if len(product.get_producers()) == 1:
            exclusive_products.append(product)

    display_products_per_industry(products_per_industry)
    print()
    display_exclusive_products(exclusive_products)

    # Section C

    # Section D


if __name__ == "__main__":
    main()
