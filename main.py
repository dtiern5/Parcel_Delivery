# Daniel Tierney, Student ID: #001510821

import csv
from datetime import datetime, timedelta, time

from package_time import check_packages_by_truck, convert_time, print_all_packages_at_time, print_single_package_by_time
from hash_table import ChainingHashTable
from package import Package
from truck import Truck
from undirected_graph import UndirectedGraph


# TODO: FINISH DOCUMENT
def ui(hash_table, distance_graph, truck_one, truck_two, truck_three):
    print("WGUPS Parcel Delivery System\n"
          "Please select an option:\n"
          "1. Individual package status\n"
          "2. All package statuses\n"
          "3. Package status by truck\n"
          "4. Truck travel distances\n"
          "5. Number of packages in each truck\n"
          "6. Exit application\n")

    user_selection = input("Select a number: ")

    if user_selection == '1':
        package_id = int(input("Package ID number: "))
        package_at_time = input("Time of day to display package (HH:MM:SS): ")
        print("\nPackage status: ")
        try:
            print_single_package_by_time(hash_table, package_at_time, package_id)
        except:
            print("Package not found")
        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '2':
        time_to_check = input("Time of day to display package statuses (HH:MM:SS): ")
        try:
            print("\nDisplaying all packages:")
            print_all_packages_at_time(hash_table, time_to_check)
        except:
            print("Correct format: (HH:MM:SS)")
        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '3':
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
        except:
            print("Correct format: (HH:MM:SS)")

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '4':
        print("Truck one miles: %.2f" % truck_one.miles)
        print("Truck two miles: %.2f" % truck_two.miles)
        print("Truck three miles: %.2f" % truck_three.miles)
        print("Total miles: %s" % (truck_one.miles + truck_two.miles + truck_three.miles))

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '5':
        print("Truck one: %s packages" % len(truck_one.package_list))
        print("Truck two: %s packages" % len(truck_two.package_list))
        print("Truck three: %s packages" % len(truck_three.package_list))

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '6':
        print("Exiting...")
        quit()

# Inserts all of the packages into a hash table
# Time complexity: O(n)
# Space complexity: O(n)
def hash_packages(filename):
    with open(filename) as wguPackages:
        reader = csv.reader(wguPackages, delimiter=',')

        for line in reader:
                pId = int(line[0])
                pAddress = line[1]
                pCity = line[2]
                pState = line[3]
                pZip = line[4]
                pDeadline = line[5]
                pWeight = line[6]
                pNotes = line[7]
                pTruck = line[8]

                # Create Package object
                package = Package(pId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pTruck)

                # Insert it into the hash table
                myHash.insert(pId, package)

                # Load package onto truck (manually for now)
                load_package(package)

# Loads packages onto trucks based on manual additions to the CSV
# Time complexity: O(1)
# Space complexity: O(1)
def load_package(package):

    if package.truck == '1':
        truck_one.package_list.append(package)
        truck_one.route.append(package.address)
    if package.truck == '2':
        truck_two.package_list.append(package)
        truck_two.route.append(package.address)
    if package.truck == '3':
        truck_three.package_list.append(package)
        truck_three.route.append(package.address)

# Creates a graph with addresses as vertexes and distance between addresses as edges
# Time complexity: O(n^2) due to the nested for loops
# Space complexity: O(n)
def create_distance_graph(filename):
    graph = UndirectedGraph()

    csv_data_array = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for line in reader:
            csv_data_array.append(line)

    for line in csv_data_array:
        graph.add_vertex(line[1]) # Vertex is the address
    for row in range(0, len(csv_data_array)):
        edges = (csv_data_array[row])[2:len(csv_data_array)+2]
        for j in range(2, len(edges)): # j is each edge weight
            graph.add_undirected_edge(csv_data_array[row][1], csv_data_array[j-2][1], float(csv_data_array[row][j]))
    return graph

"""
Greedy algorithm populates a list of unvisited locations in a truck's route. Starting at the hub, it calculates
the closest destination in miles, drops off the package, and repeats until no destinations are left. At that point, it
returns to the hub. The time and miles travelled are updated at each stop along the route.
"""
# Time complexity: O(n^2)
# Space complexity: O(n)
def greedy_algo(graph, truck):
    # Create a list of all unvisited locations on the truck's route
    unvisited_list = []
    for address in truck.route:
        unvisited_list.append(address)

    # Every truck starts at the hub.
    # We select the current location of the truck in the loop with visited_list[-1] selecting the last index
    start = '4001 South 700 East'
    visited_list = [start]

    distance_dict = graph.edge_weights # Dictionary {('address1', 'address2'): distance, ('address2', 'address1'): distance)...}
    time = truck.start_time # Start time is chosen when the truck departs
    truck.status = "ON ROUTE"

    while len(unvisited_list) > 0:
        # Initialize the shortest_distance and next_address. They will be given values with the first checked address
        shortest_distance = None
        next_address = None

        for address in unvisited_list:
            distance = distance_dict[visited_list[-1], address] # From current location to next address
            if shortest_distance is None: # 'None' if it's the first address checked in this loop
                shortest_distance = distance
                next_address = address
            if distance < shortest_distance:
                shortest_distance = distance
                next_address = address

        # 'time' will be stored with the delivered package
        elapsed_time = timedelta(minutes = (shortest_distance / truck.speed) * 60)
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

    # print("Truck finish time: ", truck.finish_time)
    # print("ROUTE: ", visited_list)


# Time Complexity: O(1)
if __name__ == '__main__':
    myHash = ChainingHashTable() # Create a chaining hash table for the packages
    myGraph = create_distance_graph('WGUPS Distance Table.csv') #
    # Create truck objects
    truck_one = Truck('Truck 1')
    truck_two = Truck('Truck 2')
    truck_three = Truck('Truck 3')
    hash_packages('WGUPS Package Data.csv')

    truck_one.depart(convert_time('9:05:00'))
    greedy_algo(myGraph, truck_one)

    truck_two.depart(convert_time('9:05:00'))
    greedy_algo(myGraph, truck_two)

    truck_three.depart(convert_time('10:00:00'))
    greedy_algo(myGraph, truck_three)



    ui(myHash, myGraph, truck_one, truck_two, truck_three)
