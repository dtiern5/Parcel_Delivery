# Daniel Tierney, Student ID: #001510821

import csv
from datetime import datetime, timedelta, time

from package_time import check_packages_by_truck, convert_time, print_all_packages_at_time, print_single_package_by_time
from hash_table import ChainingHashTable
from package import Package
from truck import Truck
from undirected_graph import UndirectedGraph

# TODO: Write UI
# TODO: BIG O
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
        print("Truck one has %s packages" % len(truck_one.package_list))
        print("Truck two has %s packages" % len(truck_two.package_list))
        print("Truck three has %s packages" % len(truck_three.package_list))

        print()
        ui(hash_table, distance_graph, truck_one, truck_two, truck_three)

    if user_selection == '6':
        print("Exiting...")
        quit()



def loadPackagesToTrucks(filename):
    with open(filename) as wguPackages:
        reader = csv.reader(wguPackages, delimiter=',')

        # print('LOAD PACKAGE DATA:')

        for line in reader:
                pId = int(line[0])
                pAddress = line[1]
                pCity = line[2]
                pState = line[3]
                pZip = line[4]
                pDeadline = line[5]
                pWeight = line[6]
                pNotes = line[7]
                pPreferredTruck = line[8]

                # Create Package object
                package = Package(pId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pPreferredTruck)

                # print(package)

                # Insert it into the hash table
                myHash.insert(pId, package)

                # Group packages for loading the trucks
                if pPreferredTruck == '1':
                    truck_one.package_list.append(package)
                    truck_one.route.append(pAddress)
                if pPreferredTruck == '2':
                    truck_two.package_list.append(package)
                    truck_two.route.append(pAddress)
                if pPreferredTruck == '3':
                    truck_three.package_list.append(package)
                    truck_three.route.append(pAddress)

def createDistanceGraph(filename):
    graph = UndirectedGraph()

    csv_data_array = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for line in reader:
            csv_data_array.append(line)
            #print('\nLINE:')
            #print(line)
    # print("csv_as_array")
    # print(csv_data_array)
    for line in csv_data_array:
        graph.add_vertex(line[1]) # Vertex is address
        # print("Line[1]: ", line[1])
    for row in range(0, len(csv_data_array)):
        edges = (csv_data_array[row])[2:len(csv_data_array)+2]
        # print(edges)
        for j in range(2, len(edges)): # j is each edge weight
            graph.add_undirected_edge(csv_data_array[row][1], csv_data_array[j-2][1], float(csv_data_array[row][j]))
    return graph

def greedy_algo(graph, truck):
    unvisited_queue = []
    for address in truck.route:
        unvisited_queue.append(address)
    start = '4001 South 700 East' # Every truck starts at the hub
    visited_queue = [start]

    distance_list = graph.edge_weights
    total_distance = 0
    time = truck.start_time
    truck.status = "ON ROUTE"

    while len(unvisited_queue) > 0:
        shortest_distance = None
        next_address = None

        for address in unvisited_queue:
            distance = distance_list[visited_queue[-1], address] # From current location to next address
            if shortest_distance is None:
                shortest_distance = distance
                next_address = address
            if distance < shortest_distance:
                shortest_distance = distance
                next_address = address

        total_distance += shortest_distance
        elapsed_time = timedelta(minutes = (shortest_distance / 18) * 60)
        time += elapsed_time
        # print('elapsed_time: ', elapsed_time)
        # print("total_distance: ", total_distance)
        # print("shortest_distance: ", shortest_distance)
        # print("next address: ", next_address)

        visited_queue.append(next_address)
        for package in truck.package_list:
            if package.address == next_address:
                package.deliver(time)
                truck.deliver(package, shortest_distance)

        unvisited_queue.remove(next_address)


    visited_queue.remove('4001 South 700 East')
    # print('total distance: ', total_distance)
    # print('total time: ', time)

    # Return to hub
    distance_to_hub = distance_list[visited_queue[-1], '4001 South 700 East']
    total_distance += distance_to_hub
    elapsed_time = timedelta(minutes=(distance_to_hub / 18) * 60)
    time += elapsed_time

    # print('\ntotal distance after return: ', total_distance)
    # print('total time after return: ', time)
    # print('\n')

    truck.finish_time = truck.current_time
    truck.status = "IN HUB"
    # print("GREEDY ROUTE: ", visited_queue)
    return visited_queue

if __name__ == '__main__':
    # Create a chaining hash table for the packages
    myHash = ChainingHashTable()
    myGraph = createDistanceGraph('WGUPS Distance Table.csv')
    truck_one = Truck('Truck 1')
    truck_two = Truck('Truck 2')
    truck_three = Truck('Truck 3')
    loadPackagesToTrucks('WGUPS Package File.csv')

    truck_one.depart(convert_time('8:00:00'))
    greedy_algo(myGraph, truck_one)

    truck_two.depart(convert_time('9:05:00'))
    greedy_algo(myGraph, truck_two)

    truck_three.depart(convert_time('10:00:00'))
    greedy_algo(myGraph, truck_three)

    ui(myHash, myGraph, truck_one, truck_two, truck_three)
    #
    #
    # print("\ntotal miles: %.2f" % (truck_one.miles + truck_two.miles + truck_three.miles))
    #
    # check_status_at_time(truck_one, '9:00:00')
    # print("\n\n")
    # check_status_at_time(truck_one, '7:00:00')
    # print("\n\n")
    # check_status_at_time(truck_one, '12:00:00')
    # print("\n\n")
    # check_status_at_time(truck_one, '9:00:00')
    # print("\n\n")
    # check_status_at_time(truck_one, '7:00:00')
    # print("\n\n")
    #
    # print(print_all_packages_at_time(myHash, '9:15:00'))
    # print(print_single_package_by_time(myHash, '9:00:00', 4))
    #
    # print(print_all_packages_at_time(myHash, '12:15:00'))