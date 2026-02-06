"""
Author: Luc Bibeau
"""

# Classes

class Country:

    def __init__(self, country_code: str, name: str, imports: float, exports: float):
        self._country_code = country_code
        self._name = name
        self._imports = imports
        self._exports = exports

    def get_deficit(self):
        return round(self._imports - self._exports, 2)
    
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
            for k,v in enumerate(lines):
                split_line = v.split(",")

                for i,entry in enumerate(split_line):
                    split_line[i] = entry.strip()
                
                lines[k] = split_line

        return lines
        

def load_countries(filename):
    """
    Loads countries from a given file
    """
    data = read_file(filename)
    data.pop(0) # get rid of header line

    countries = []

    for entry in data:
        country = Country(entry[0], entry[1], float(entry[2]), float(entry[3]))
        countries.append(country)
    
    return countries
        

def display_table(headers, info, include_dollars=False):
    columns = len(headers)
    column_sizes = []
    temp = []

    for i in range(columns):
        temp.append([headers[i]])

    for entry in info:
        for i in range(columns):
            temp[i].append(entry[i])
    
    for i in range(columns):
        column_sizes.append(max(len(line) for line in temp[i]))

    print(column_sizes)


def main():
    # Section A
    countries = load_countries("country.txt")
    
    countries_sorted = sorted(countries, key=lambda x: x.get_deficit(), reverse=True)

    sorted_info = []
    for country in countries_sorted[0:10]:
        print(str(country))
        sorted_info.append((str(country), str(country.get_deficit())))

    display_table(
        ("Country", "Trade Deficit (Billions USD)"),
        sorted_info,
        True
    )

    # Section B

    # Section C

    # Section D
    

if __name__ == "__main__":
    main()