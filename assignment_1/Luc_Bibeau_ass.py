"""
Assignment 1.
Analyses countries' trade information, product information,
and their given overlap (such as if product X is tariffed by
country Y).

Author: Luc Bibeau
When: Completed February 11, 2026
"""

INDUSTRIES = ("Agriculture", "Food", "Manufacturing", "Pharmacy", "Tech")


# Classes

class Country:
    """
    Country class. Can be fetched by country code.
    Stores information such as imports, exports, name, and tariffs.
    """
    _countries = {}

    @staticmethod
    def from_country_code(country_code: str) -> object:
        """
        Fetches a Country object via country code.
        :param country_code:
        :return: Country
        """
        return Country._countries.get(country_code, None)

    @staticmethod
    def all() -> list:
        """
        Returns every cached Country.
        :return: list[Country]
        """
        return list(Country._countries.values())

    def __init__(self, country_code: str, name: str, imports: float, exports: float):
        self._country_code = country_code
        self._name = name
        self._imports = imports
        self._exports = exports
        self._tariffs = {}  # will be set later when tariffs are loaded

        self._countries[country_code] = self  # store instance statically to fetch by id

    def set_tariff(self, industry, percent):
        """
        Sets a tariff
        :param industry: str, industry
        :param percent: float, percent
        :return: none
        """
        self._tariffs[industry] = percent  # ranges from 0.0 - 1.0

    def get_tariff(self, industry):
        """
        Gets a tariff
        :param industry: str, industry
        :return: float, percent
        """
        return self._tariffs.get(industry, 0.0)

    def get_highest_tariff(self):
        """
        Gets the highest tariff
        :return: float, highest tariff
        """
        if len(self._tariffs) == 0:
            return 0.0
        return max(self._tariffs.values())

    def get_deficit(self):
        """
        Gets the trade deficit
        :return: float, trade deficit
        """
        return round(self._imports - self._exports, 2)

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name


class Product:
    """
    Product class. Can be fetched by Product ID.
    Stores information about a product, such as
    the industry, name, and pricing by country.
    """
    _products = {}

    @staticmethod
    def from_product_id(product_id: str) -> object:
        """
        Gets a Product by id
        :param product_id: str
        :return: Product
        """
        return Product._products.get(product_id, None)

    def __init__(self, pid: str, industry: str, product_name: str, country_prices: list[tuple]):
        self._pid = pid
        self._industry = industry
        self._name = product_name
        self._country_prices = country_prices

        self._products[pid] = self  # static store, same as Country cache

    def get_id(self):
        """
        Gets the product ID
        :return: str
        """
        return self._pid

    def get_industry(self):
        """
        Gets the industry of the product
        :return: str
        """
        return self._industry

    def get_producers(self):
        """
        Gets the countries that produce the product and at what price
        :return: tuple(str, float)
        """
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
        if len(entry) == 4:  # verify entry is formatted properly
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
        if len(entry) == 3:  # verify entry is formatted properly
            key = entry[0]
            country_code = entry[1]
            price = entry[2]

            if key not in product_countries:
                product_countries[key] = []

            product_countries[key].append(
                (country_code, float(price))
            )

    data = read_file(products_filename)
    data.pop(0)

    products = []

    for entry in data:
        pid = entry[0]
        product = Product(pid, entry[1], entry[2], product_countries[pid])
        products.append(product)

    return products


def load_tariffs(filename):
    """
    Loads and stores tariffs in each country's
    respective object. Because it uses the static
    country fetch method, countries MUST be loaded
    first.
    :param filename: str, name of tariffs file
    :return: none
    """
    data = read_file(filename)

    for line in data:
        if len(line) == 3:  # verify entry is formatted properly
            country = Country.from_country_code(line[0])

            if country:
                percent = float(line[2]) / 100.
                country.set_tariff(line[1], percent)


def load_shopping_list(filename):
    """
    Loads a shopping list.
    :param filename: str, name of list
    :return: list, list of products
    """
    data = read_file(filename)
    shopping_list = []

    for line in data:
        product = Product.from_product_id(line)

        if product:  # verify product exists (from_product_id can return None)
            shopping_list.append(product)

    return shopping_list


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

    return f"\n{splitter}\n{formatted_header}\n{splitter}", splitter


def get_most_exclusive_countries(exclusive_products):
    """
    Gets the countries that produce the most amount
    of exclusive products.
    :param exclusive_products: list of exclusive products
    :return: list[tuple[str, int]] countries
    """
    country_count = {}

    for product in exclusive_products:
        producer_info = product.get_producers()[0]  # only 1 as it is exclusive
        country_code = producer_info[0]

        if Country.from_country_code(country_code):
            if country_code not in country_count:
                country_count[country_code] = 0

            country_count[country_code] += 1

    sorted_data = sorted(country_count.items(), key=lambda x: (-x[1], x[0]))

    # get only the top exclusive producers
    max_products = sorted_data[0][1]
    top_producers = []
    index = 0

    while sorted_data[index][1] == max_products:
        top_producers.append(sorted_data[index])
        index += 1

    return top_producers


def get_least_exclusive_industries(exclusive_products):
    """
    Gets the industries that produce the least amount
    of exclusive products.
    :param exclusive_products: list of exclusive products
    :return: list[tuple[str, int]] industries
    """
    industry_count = {}

    for product in exclusive_products:
        industry = product.get_industry()  # only 1 as it is exclusive

        if industry not in industry_count:
            industry_count[industry] = 0

        industry_count[industry] += 1

    sorted_data = sorted(industry_count.items(), key=lambda x: (x[1], x[0]))

    # get only the min exclusive producers
    min_products = sorted_data[0][1]
    least_producers = []
    index = 0

    while sorted_data[index][1] == min_products:
        least_producers.append(sorted_data[index])
        index += 1

    return least_producers


def get_most_productive_countries(products):
    """
    Gets the country (or countries if tie) that produces the
    most amount of products.
    :param products: list[Product]
    :return: list
    """

    country_count = {}

    for product in products:
        for producer in product.get_producers():
            country_code = producer[0]
            country = Country.from_country_code(country_code)

            if country:
                country_name = str(country)
                if country_name not in country_count:
                    country_count[country_name] = 0

                country_count[country_name] += 1

    # want to sort by number in descending BUT alphabetically ascending
    # to easily remedy this just flip the sign on the int to make it also ascending
    sorted_data = sorted(country_count.items(), key=lambda x: (-x[1], x[0]))

    max_value = sorted_data[0][1]
    top_entries = []
    index = 0

    while sorted_data[index][1] == max_value:
        top_entries.append(sorted_data[index])
        index += 1

    return top_entries


def get_most_widespread_products(products):
    """
    Gets a list of products that are produced by the
    most amount of countries.
    :param products: list, products
    :return: list, most widespread products
    """
    product_count = {}

    for product in products:
        product_count[str(product)] = len(product.get_producers())

    sorted_data = sorted(product_count.items(), key=lambda x: (-x[1], x[0]))

    trimmed_data = []
    index = 0
    changes = 0
    last_value = 0
    while changes < 3 and index < len(sorted_data):  # take top 3 (only allow 3 changes)
        trimmed_data.append(sorted_data[index])
        index += 1

        if last_value != sorted_data[index][1]:
            last_value = sorted_data[index][1]
            changes += 1

    return trimmed_data


def get_selective_tariff_countries():
    """
    Gets the countries with selective tariffs
    (not every industry has tariffs)
    :return: list[tuple], countries & their industry not taxed
    """
    selective = []

    for country in Country.all():
        if country.get_highest_tariff() > 0:
            for industry in INDUSTRIES:
                if country.get_tariff(industry) == 0:
                    selective.append((str(country), industry))

    return selective


def get_best_deals(shopping_list):
    """
    Gets the cheapest possible deal for each product in a shopping list.
    The resulting list includes raw price, tariff %, total cost, etc.
    :param shopping_list:
    :return:
    """
    best_shopping_list = []

    for product in shopping_list:
        industry = product.get_industry()
        producers = product.get_producers()

        best_deal = None
        best_price = None

        for producer in producers:
            country_code = producer[0]
            raw_price = producer[1]

            country = Country.from_country_code(country_code)
            if country:
                tariff = country.get_tariff(industry)
                tariff_value = raw_price * tariff
                total_price = raw_price + tariff_value

                if best_deal is None or total_price < best_price:
                    best_price = total_price
                    best_deal = (str(country), raw_price, tariff, tariff_value, total_price)

        formatted_info = (str(product), len(producers)) + best_deal
        best_shopping_list.append(formatted_info)

    return best_shopping_list


#
# DISPLAY FUNCTIONS
#
# While the display functions may have some repeated code
# in each one, they MUST differ as the specific formatting
# (prefixes, percentages, etc) differ from table to table.
# This decision was intentional.
#

def display_trade_deficits(countries):
    """
    Displays the trade deficits of the given countries.
    :param countries: list
    :return: none
    """
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
    """
    Displays the number of products per industry
    :param products_per_industry: dict
    :return: none
    """
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
    """
    Displays every product that are only produced
    by one country.
    :param products: list
    :return: none
    """
    headers = ("PID", "Product Name", "Producing Country")
    products_sorted = sorted(products, key=lambda x: str(x))  # sort by name

    sorted_info = []
    for product in products_sorted:
        producing_country_id = product.get_producers()[0][0]  # first producer, country code

        producing_country = Country.from_country_code(producing_country_id)
        if producing_country:  # may return None if country code not found.
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


def display_most_exclusive_countries(countries):
    """
    Displays the country/countries that produce the most exclusive products.
    :param countries: list
    :return: none
    """
    headers = ("Country", "No. of Exclusive Products")

    formatted_info = []
    for country_info in countries:
        country_name = str(Country.from_country_code(country_info[0]))

        formatted_info.append((country_name, str(country_info[1])))  # table formatting requires everything be str

    sizes = get_column_sizes(
        headers, formatted_info, ("", "")
    )
    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in formatted_info:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} |")
    print(splitter)


def display_least_exclusive_industries(industries):
    """
    Displays the industry/industries that produce the
    least amount of exclusive products.
    :param industries: list
    :return: none
    """
    headers = ("Industry", "No. of Exclusive Products")

    formatted_info = []
    for industry_info in industries:
        formatted_info.append((industry_info[0], str(industry_info[1])))  # table formatting requires everything be str

    sizes = get_column_sizes(
        headers, formatted_info, ("", "")
    )
    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in formatted_info:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} |")
    print(splitter)


def display_most_productive_countries(countries):
    """
    Displays the country/countries that produce the largest
    total number of products.
    :param countries: list
    :return: none
    """
    headers = ("Country", "Number of Products")

    formatted_info = []
    for country_info in countries:
        formatted_info.append((country_info[0], str(country_info[1])))  # table formatting requires everything be str

    sizes = get_column_sizes(
        headers, formatted_info, ("", "")
    )
    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in formatted_info:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} |")
    print(splitter)


def display_most_widespread_products(products):
    """
    Displays the products that are produced by the most amount of countries.
    :param products: list
    :return: none
    """
    headers = ("Product Name", "Number of Countries")

    formatted_info = []
    for product in products:
        formatted_info.append((product[0], str(product[1])))

    sizes = get_column_sizes(
        headers, formatted_info, ("", "")
    )
    header, splitter = get_table_strings(headers, sizes)
    print(header)
    for entry in formatted_info:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} |")
    print(splitter)


def display_tariff_related(func):
    """
    Displays a table for tariff related info.
    Function called must return a boolean to see if
    the passed country meets the required condition.
    :param func: function, passed value is the country to check
    :return: none
    """
    countries = []

    for country in Country.all():
        if country:
            if func(country):
                countries.append(
                    (str(country),)  # must use tuple for table formatting to work
                )

    # countries are already sorted alphabetically
    headers = ("Country",)
    sizes = get_column_sizes(
        headers, countries, ("",)
    )
    header, splitter = get_table_strings(headers, sizes)
    print(header)
    for entry in countries:
        print(f"| {entry[0]:<{sizes[0]}} |")
    print(splitter)


def display_selective_tariff_countries(selective_tariffs):
    """
    Displays countries with selective tariffs (not all industries tariffed)
    :param selective_tariffs:
    :return:
    """
    sorted_data = sorted(selective_tariffs, key=lambda x: x)  # sort alphabetically. data is already a list of tuples

    headers = ("Country", "Industry")
    sizes = get_column_sizes(
        headers, sorted_data, ("", "")
    )
    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in sorted_data:
        print(f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} |")
    print(splitter)


def display_best_deals(best_deals):
    """
    Displays the best deals and their total cost
    :param best_deals: list
    :return: none
    """
    headers = ("Product Name", "Countries", "Best Country", "Actual Cost", "Tariff %", "Tariff Val", "Total Cost")

    cost_before_tariff = 0
    tariff_paid = 0

    formatted_info = []
    for deal in best_deals:
        cost_before_tariff += deal[3]
        tariff_paid += deal[5]

        formatted_info.append(
            (
                deal[0],  # product
                str(deal[1]),  # num of countries
                deal[2],  # country
                f"{deal[3]:,.2f}",  # raw cost
                f"{deal[4] * 100.:.1f}",  # tariff %. multiply by 100 (e.g. 0.01 -> 1%)
                f"{deal[5]:,.2f}",  # tariff val
                f"{deal[6]:,.2f}"  # total cost
            )
        )

    sizes = get_column_sizes(
        headers, formatted_info, ("", "", "", "$ ", "%", "$ ", "$ ")
    )

    header, splitter = get_table_strings(headers, sizes)

    print(header)
    for entry in formatted_info:
        print(
            f"| {entry[0]:<{sizes[0]}} | {entry[1]:>{sizes[1]}} | {entry[2]:<{sizes[2]}} | $ {entry[3]:>{sizes[3] - 2}} " +
            f"| {entry[4]:>{sizes[4] - 1}}% | $ {entry[5]:>{sizes[5] - 2}} | $ {entry[6]:>{sizes[6] - 2}} |"
        )
    print(splitter)
    print(f"Cost Before Tariff: $ {cost_before_tariff:,.2f}")
    print(f"Total Tariff Paid: $ {tariff_paid:,.2f}")
    print(f"Grand Total: $ {cost_before_tariff + tariff_paid:,.2f}")


def main():
    # Section A
    countries = load_countries("country.txt")
    display_trade_deficits(countries)

    # Section B
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
    display_exclusive_products(exclusive_products)

    most_exclusive_countries = get_most_exclusive_countries(exclusive_products)
    display_most_exclusive_countries(most_exclusive_countries)

    least_exclusive_industries = get_least_exclusive_industries(exclusive_products)
    display_least_exclusive_industries(least_exclusive_industries)

    most_productive_countries = get_most_productive_countries(products)
    display_most_productive_countries(most_productive_countries)

    most_widespread_products = get_most_widespread_products(products)
    display_most_widespread_products(most_widespread_products)

    # Section C
    load_tariffs("tariff.txt")

    display_tariff_related(lambda x: x.get_highest_tariff() > 0.5)  # outrageous tariffs
    display_tariff_related(lambda x: x.get_highest_tariff() == 0.0)  # tariff-free

    selective_tariff = get_selective_tariff_countries()
    display_selective_tariff_countries(selective_tariff)

    # Section D
    shopping_list = load_shopping_list("shopping_list.txt")
    best_deals = get_best_deals(shopping_list)
    display_best_deals(best_deals)


if __name__ == "__main__":
    main()
