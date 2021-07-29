# Daniel Tierney, Student ID: #001510821

import csv
from datetime import datetime, timedelta, time

from package_time import check_packages_by_truck, convert_time, print_all_packages_at_time, print_single_package_by_time
from hash_table import ChainingHashTable
from package import Package
from truck import Truck
from undirected_graph import UndirectedGraph


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

    print("WGUPS Parcel Delivery System")
    print("")

    # print(len(truck_one.package_list))
    # print(len(truck_two.package_list))
    # print(len(truck_three.package_list))

    truck_one.depart(convert_time('8:00:00'))
    # print(truck_one.start_time)
    greedy_algo(myGraph, truck_one)

    truck_two.depart(convert_time('9:05:00'))
    # print(truck_two.start_time)
    greedy_algo(myGraph, truck_two)

    truck_three.depart(convert_time('10:00:00'))
    # print(truck_three.start_time)
    greedy_algo(myGraph, truck_three)


    # print("\nTRUCK ONE PACKAGE LIST: ")
    # for package in truck_one.package_list:
    #     print(package)
    #
    # print("\nTRUCK TWO PACKAGE LIST: ")
    # for package in truck_two.package_list:
    #     print(package)
    #
    # print("\nTRUCK Three PACKAGE LIST: ")
    # for package in truck_three.package_list:
    #     print(package)

    # print("truck_one: ", truck_one)
    # print("truck_two: ", truck_two)
    # print("truck_three: ", truck_three)
    #
    # print("\ntotal miles: %.2f" % (truck_one.miles + truck_two.miles + truck_three.miles))

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


    print(print_all_packages_at_time(myHash, '9:15:00'))
    print(print_single_package_by_time(myHash, '9:00:00', 4))

    print(print_all_packages_at_time(myHash, '12:15:00'))