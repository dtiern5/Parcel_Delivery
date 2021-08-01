# Daniel Tierney, Student ID: #001510821

import csv
from datetime import timedelta
from package_time import check_packages_by_truck, convert_time, print_all_packages_at_time, print_single_package_by_time
from hash_table import ChainingHashTable
from package import Package
from truck import Truck
from undirected_graph import UndirectedGraph


def main():
    """
    Creates hash table, graph, and three trucks.
    Hashes the packages and loads them to the trucks.
    Sets each truck to depart at a given time so data can be pulled in the UI.
    Starts the UI.
    :return: None
    Time Complexity for the entire application is O(n^2), both the create_distance_graph function
    and the nearest_neighbor algorithm perform at O(n^2)
    """
    my_hash = ChainingHashTable()  # Create a chaining hash table for the packages
    my_graph = create_distance_graph('WGUPS Distance Table.csv')  #
    # Create truck objects
    truck_one = Truck('Truck 1')
    truck_two = Truck('Truck 2')
    truck_three = Truck('Truck 3')
    hash_packages('WGUPS Package Data.csv', my_hash, truck_one, truck_two, truck_three)

    truck_one.depart(convert_time('8:00:00'))
    nearest_neighbor(my_graph, truck_one)

    truck_two.depart(convert_time('9:05:00'))
    nearest_neighbor(my_graph, truck_two)

    truck_three.depart(convert_time('10:45:00'))
    nearest_neighbor(my_graph, truck_three)

    ui(my_hash, my_graph, truck_one, truck_two, truck_three)


def ui(hash_table, distance_graph, truck_one, truck_two, truck_three):
    """
    Prompts the user with choices for displaying truck and package data.
    User types the number and presses enter

    :param hash_table: The hash_table containing package information
    :param distance_graph: The graph containing addresses as vertices and distances as edges
    :param truck_one: First truck, leaves immediately at 8:00:00
    :param truck_two: Second truck, leaves when delayed packages arrive at 9:05:00
    :param truck_three: Third truck, leaves after first truck returns to the hub at 10:45:00
    :return: None
    """

    print("WGUPS Parcel Delivery System\n"
          "Please select an option (type the number and press Enter):\n"
          "1. Individual package status\n"
          "2. All package statuses\n"
          "3. Package status by truck\n"
          "4. Truck travel distances\n"
          "5. Number of packages in each truck\n"
          "6. Truck route and finish time\n"
          "7. Exit application\n")

    user_selection = input("Select a number: ")

    if user_selection == '1':
        # Display a package's status at a chosen time
        package_id = int(input("Package ID number: "))
        package_at_time = input("Time of day to display package (HH:MM:SS): ")
        print("\nPackage status: ")
        try:
            print_single_package_by_time(hash_table, package_at_time, package_id)
        except AttributeError:
            print("Package not found")
        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '2':
        # Display all package statuses at a chosen time
        time_to_check = input("Time of day to display package statuses (HH:MM:SS): ")
        try:
            print("\nDisplaying all packages:")
            print_all_packages_at_time(hash_table, time_to_check)
        except TypeError:
            print("Correct format: (HH:MM:SS)")
        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '3':
        # Display the chosen truck's package statuses at the chosen time
        current_truck = None
        truck_number = input("Which truck? (1, 2, or 3) ")
        if truck_number == '1':
            current_truck = truck_one
        elif truck_number == '2':
            current_truck = truck_two
        elif truck_number == '3':
            current_truck = truck_three
        else:
            print("Truck not found")
            print()
            ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

        time_to_check = input("Time of day to display package statuses (HH:MM:SS): ")
        try:
            check_packages_by_truck(current_truck, time_to_check)
        except TypeError:
            print("Correct format: (HH:MM:SS)")

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '4':
        # Display the total miles on each truck, as well as the total miles of all trucks
        print("\nTruck travel distances:")
        print("Truck one miles: %.2f" % truck_one.miles)
        print("Truck two miles: %.2f" % truck_two.miles)
        print("Truck three miles: %.2f" % truck_three.miles)
        print("Total miles: %.2f" % (truck_one.miles + truck_two.miles + truck_three.miles))

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '5':
        # Display the number of packages on each truck
        print("Truck one: %s packages" % len(truck_one.package_list))
        print("Truck two: %s packages" % len(truck_two.package_list))
        print("Truck three: %s packages" % len(truck_three.package_list))

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '6':
        print("\nTruck one finished its route at ", truck_one.finish_time)
        print("Route:")
        print(truck_one.route)
        print("\nTruck two finished its route at ", truck_two.finish_time)
        print("Route:")
        print(truck_two.route)
        print("\nTruck three finished its route at ", truck_three.finish_time)
        print("Route:")
        print(truck_three.route)
        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '7':
        print("Exiting...")
        quit()

    else:
        print("Numbers 1 through 7 are valid inputs\n")
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

def hash_packages(filename, hash_table, truck_one, truck_two, truck_three):
    """
    Inserts all packages into a hash table by first creating a package object from each line
    of the CSV, then calling the hash table's insert function using the package ID as the key.
    Also calls the load_package function to place the package in the correct truck

    :param filename: The CSV to retrieve packages data from
    :param hash_table: The hash table to store the package data
    :param truck_one: First truck
    :param truck_two: Second truck
    :param truck_three: Third truck
    :return: None
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    with open(filename) as wguPackages:
        reader = csv.reader(wguPackages, delimiter=',')

        for line in reader:
            p_id = int(line[0])
            p_address = line[1]
            p_city = line[2]
            p_state = line[3]
            p_zip = line[4]
            p_deadline = line[5]
            p_weight = line[6]
            p_notes = line[7]
            p_truck = line[8]

            # Create Package object
            package = Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_notes, p_truck)

            # Insert it into the hash table
            hash_table.insert(p_id, package)

            # Load package onto truck (manually for now)
            load_package(package, truck_one, truck_two, truck_three)


def load_package(package, truck_one, truck_two, truck_three):
    """
    Loads a package onto the trucks based on the manually added column 9 in the CSV
    :param package: The package to load
    :param truck_one: First truck
    :param truck_two: Second truck
    :param truck_three: Third truck
    :return: None
    Time Complexity: O(1)
    """

    if package.truck == '1':
        truck_one.package_list.append(package)
        truck_one.route.append(package.address)
    if package.truck == '2':
        truck_two.package_list.append(package)
        truck_two.route.append(package.address)
    if package.truck == '3':
        truck_three.package_list.append(package)
        truck_three.route.append(package.address)


def create_distance_graph(filename):
    """
    Creates and returns a graph object with addresses as vertices and distances between addresses as edges.
    :param filename: CSV of the distance table containing addresses and distances.
    :return: A graph object derived from the given CSV
    Time complexity: O(n^2) due to the nested for loops
    Space complexity: O(n)
    """
    graph = UndirectedGraph()

    csv_data_list = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for line in reader:
            csv_data_list.append(line)

    for line in csv_data_list:
        graph.add_vertex(line[1])  # Vertex is the address
    for row in range(0, len(csv_data_list)):
        edges = (csv_data_list[row])[2:len(csv_data_list) + 2]  # Skip the first two columns
        for j in range(2, len(edges)):  # j is each edge weight
            # [j-2] gets us the correct row for the second address
            graph.add_undirected_edge(csv_data_list[row][1], csv_data_list[j - 2][1], float(csv_data_list[row][j]))
    return graph


def nearest_neighbor(graph, truck):
    """
    The nearest neighbor algorithm populates a list of unvisited locations in a truck's route.
    Starting at the hub, it calculates the closest destination in miles, drops off the package,
    and repeats until no destinations are left. At that point, it returns to the hub.
    The time and miles travelled are updated at each stop along the route.

    :param graph: The graph containing addresses as vertices and distances as edges
    :param truck: The truck whose route is being planned by the nearest neighbor algorithm
    :return: None
    Time complexity: O(n^2) The for loop, as well as the while loop it is nested within, each loop 'n' number of times
    based on the length truck's route
    Space complexity: O(n)
    """
    # Create a list of all unvisited locations on the truck's route
    unvisited_list = []
    for address in truck.route:
        unvisited_list.append(address)

    # Every truck starts at the hub.
    # We select the current location of the truck in the loop with visited_list[-1] selecting the last index
    start = '4001 South 700 East'
    visited_list = [start]

    distance_dict = graph.edge_weights  # Dictionary {('address1', 'address2'): distance, ...}
    time = truck.start_time  # Start time is chosen when the truck departs
    truck.status = "ON ROUTE"

    while len(unvisited_list) > 0:
        # Initialize the shortest_distance and next_address. They will be given values with the first checked address
        shortest_distance = None
        next_address = None

        for address in unvisited_list:
            distance = distance_dict[visited_list[-1], address]  # From current location to next address
            if shortest_distance is None:  # 'None' if it's the first address checked in this loop
                shortest_distance = distance
                next_address = address
            if distance < shortest_distance:
                shortest_distance = distance
                next_address = address

        # 'time' will be stored with the delivered package
        elapsed_time = timedelta(minutes=(shortest_distance / truck.speed) * 60)
        time += elapsed_time

        # Add the address to the visited_list. On the next loop it will be called as visited_list[-1]
        visited_list.append(next_address)

        # Store the time the package was delivered, and increment the distance in miles that the truck has travelled
        for package in truck.package_list:
            if package.address == next_address:
                package.deliver(time)
                truck.travel(shortest_distance)

        # Remove the address from the unvisited_list in order to not visit the same address twice
        unvisited_list.remove(next_address)

    # Return to hub
    distance_to_hub = distance_dict[visited_list[-1], '4001 South 700 East']
    truck.travel(distance_to_hub)
    truck.finish_time = truck.current_time
    truck.status = "IN HUB"


if __name__ == '__main__':
    main()
