"""
Option 1

Author: Luc Bibeau
When: February 4, 2026
"""

PROPERTY_SQ_FOOTAGE = 1
PROPERTY_OWNER = 2

def read_file(filename):
    """
    Opens a file and returns a 2D array of strings.
    Splits by line and comma (,)
    :param filename:
    :return:
    """

    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        lines.pop(0)  # pop the header entry

        for i in range(len(lines)):
            lines[i] = lines[i].split(',')

        return lines


def load_properties(filename):
    """
    Loads properties as a dictionary. Key is location.
    Entry is list of properties belonging to said location.
    :param filename:
    :return:
    """
    result = {}

    data = read_file(filename)

    for entry in data:
        location = entry.pop(0)

        if location not in result:
            result[location] = []

        entry[PROPERTY_SQ_FOOTAGE] = float(entry[1])  # turn square footage into float

        result[location].append(entry)

    return result


def load_price_index(filename):
    """
    Loads the price index of locations
    :param filename:
    :return:
    """
    result = {}

    data = read_file(filename)

    for entry in data:
        result[entry[0]] = float(entry[1])

    return result


def aggregate_data(properties, price_index):
    """
    Gets the relevant information (available properties, avg price, avg sq ft.) of each location.
    :param properties:
    :param price_index:
    :return:
    """
    result = {}

    for location in properties:
        square_footage = 0
        available_properties = 0
        number_of_properties = len(properties[location])

        for entry in properties[location]:
            square_footage += entry[PROPERTY_SQ_FOOTAGE]
            if entry[PROPERTY_OWNER] == "0":
                available_properties += 1

        avg_area = square_footage / number_of_properties
        avg_price = avg_area * price_index[location]

        result[location] = (round(avg_area, 2), round(avg_price, 2), available_properties)

    sorted_result = sorted(result.items(), key=lambda x: x[1][2], reverse=True)

    return dict(sorted_result)


def display_data(data):

    separator = f"+{'-' * 15}" * 3 + "+" + ("-" * 11) + "+"

    print(separator)
    print(f"| {'Location':<14}| {'Average Area':<14}| {'Average Price':<14}| {'Available':<10}|")
    print(separator)

    for location in data:
        avg_area, avg_price, available = data[location]

        location_string = f" {location:<14}"
        area_string = f"{(f'{avg_area:,.2f}' + ' sqft'):^15}"
        price_string = f" $ {avg_price:>11,.2f} "
        available_string = f"{available:>10} "

        print(f"|{location_string}|{area_string}|{price_string}|{available_string}|")
    print(separator)


def main():
    properties = load_properties("properties.txt")
    price_index = load_price_index("price_index.txt")

    data = aggregate_data(properties, price_index)
    display_data(data)


if __name__ == '__main__':
    main()