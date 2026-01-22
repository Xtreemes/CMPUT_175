"""
Author: Luc Bibeau
Date: January 19, 2026
"""


def read_file(filename: str) -> list:
    """
    Opens a file and returns a list of each line split by comma (,)
    :param filename:
    :return:
    """

    result = []

    with open(filename, 'r') as file:
        lines = file.read().splitlines()

        for line in lines:
            result.append(line.split(","))

    return result


def setup_stops(filename: str) -> tuple[dict, dict]:
    """
    Set up the stop dictionaries (converting name to code and vice versa)
    :param filename:
    :return:
    """
    code_to_name = {}
    name_to_code = {}

    data = read_file(filename)
    for entry in data:
        code_to_name[entry[0]] = entry[1]
        name_to_code[entry[1]] = entry[0]

    return code_to_name, name_to_code


def get_input(prompt) -> str:
    """
    Gets and title cases an input from the user
    :param prompt:
    :return:
    """
    return input(prompt).title()


def get_stop(prompt, name_to_code):
    """
    Gets a stop from the user
    :param prompt:
    :param name_to_code:
    :return:
    """
    stop = ""
    while not stop in name_to_code:
        stop = get_input(prompt)

    return name_to_code[stop]


def get_direct_route(start, destination, routes) -> list or None:
    """
    Gets and returns a direct bus route or none if not found.
    :param start:
    :param destination:
    :param routes:
    :return:
    """

    for route in routes:
        if start in route and destination in route:
            return route


def get_transfer_route(start, destination, routes) -> tuple[list, list, str] or None:
    """
    Gets and returns a transfer bus route or none if not found.
    :param start:
    :param destination:
    :param routes:
    :return:
    """

    start_routes = []
    destination_routes = []

    for route in routes:
        if start in route:
            start_routes.append(route)
        if destination in route:
            destination_routes.append(route)

    # avoid repeating checks for stops.
    # e.g. if D002 has already been confirmed to not be a valid transfer, don't check it again.
    checked_stops = []

    for route in start_routes:
        for stop in route[1:]:
            if not stop in checked_stops:
                for destination_route in destination_routes:
                    if stop in destination_route:
                        return route, destination_route, stop
                checked_stops.append(stop)


def display_direct_route(route, stops) -> None:
    """
    Displays a direct bus route.
    :param route:
    :param stops:
    :return:
    """
    names = [route[0]]

    for stop in route[1:]:
        names.append(stops[stop])

    print(f"Direct route found: {' -> '.join(names)}")


def display_transfer_route(transfer_info, stops) -> None:
    start_route = transfer_info[0]
    destination_route = transfer_info[1]
    stop = stops[transfer_info[2]]

    start_route_id = start_route.pop(0)
    destination_route_id = destination_route.pop(0)

    print("\nTransfer option found:\n")
    print(f"Take route {start_route_id} and get off at {stop}.\nThen take route {destination_route_id} to your destination.\n")

    start_names = []
    destination_names = []

    for stop in start_route:
        start_names.append(stops[stop])

    for stop in destination_route:
        destination_names.append(stops[stop])

    print(f"Route {start_route_id}: {' -> '.join(start_names)}")
    print(f"Route {destination_route_id}: {' -> '.join(destination_names)}")


def main():

    routes = read_file("routes.txt")

    code_to_name, name_to_code = setup_stops("codes.txt")

    starting = get_stop("Enter Starting Point: ", name_to_code)
    destination = get_stop("Enter Destination: ", name_to_code)

    direct_route = get_direct_route(starting, destination, routes)

    if direct_route:
        display_direct_route(direct_route, code_to_name)
    else:

        transfer_info = get_transfer_route(starting, destination, routes)

        if transfer_info:
            display_transfer_route(transfer_info, code_to_name)

        else:
            print("No routes serving that start point and end point")


if __name__ == "__main__":
    main()