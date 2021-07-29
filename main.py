import csv
from datetime import datetime, timedelta, time

import undirected_graph
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
    print("unvisited_queue: ", unvisited_queue)

    start = '4001 South 700 East' # Every truck starts at the hub
    greedy_route = [start]

    distance_list = graph.edge_weights
    total_distance = 0
    time = truck.start_time
    truck.status = "ON ROUTE"

    while len(unvisited_queue) > 0:
        shortest_distance = None
        next_address = None

        for address in unvisited_queue:
            distance = distance_list[greedy_route[-1], address] # From current location to next address
            if shortest_distance == None:
                shortest_distance = distance
                next_address = address
            if distance < shortest_distance:
                shortest_distance = distance
                next_address = address

        total_distance += shortest_distance
        elapsed_time = timedelta(minutes = (shortest_distance / 18) * 60)
        time += elapsed_time
        print('elapsed_time: ', elapsed_time)
        #print("total_distance: ", total_distance)
        #print("shortest_distance: ", shortest_distance)
        #print("next address: ", next_address)

        greedy_route.append(next_address)
        for package in truck.package_list:
            if package.address == next_address:
                package.deliver(time)
                truck.deliver(package, shortest_distance)

        unvisited_queue.remove(next_address)


    greedy_route.remove('4001 South 700 East')
    print('\ntotal distance: ', total_distance)
    print('total time: ', time)

    # Return to hub
    distance_to_hub = distance_list[greedy_route[-1], '4001 South 700 East']
    total_distance += distance_to_hub
    elapsed_time = timedelta(minutes=(distance_to_hub / 18) * 60)
    time += elapsed_time

    print('\ntotal distance after return: ', total_distance)
    print('total time after return: ', time)
    print('\n')

    truck.finish_time = truck.current_time
    truck.status = "IN HUB"
    return greedy_route



        # smallest_distance = graph.edge_weights.get(greedy_route[len(greedy_route) - 1], unvisited_queue[0])
        # print(smallest_distance)
        # for i in range(1, len(unvisited_queue)):
        #     next_distance = graph.edge_weights.get(greedy_route[len(greedy_route) - 1], unvisited_queue[i])
        #     if  next_distance < smallest_distance:
        #         smallest_distance = next_distance
        #         print(smallest_distance)
        #     current_location = unvisited_queue.pop(smallest_distance)
        #     print('popped ', current_location)





        # current_vertex = unvisited_queue.pop(smallest_index)



if __name__ == '__main__':
    # Create a chaining hash table for the packages
    myHash = ChainingHashTable()
    myGraph = createDistanceGraph('WGUPS Distance Table.csv')

    truck_one = Truck()
    truck_two = Truck()
    truck_three = Truck()

    loadPackagesToTrucks('WGUPS Package File.csv')

    # greedy_algo(myGraph, truck_one)

    print(myGraph.edge_weights)

    # print(len(truck_one.package_list))
    # print(len(truck_two.package_list))
    # print(len(truck_three.package_list))

    # print(myGraph.edge_weights.get('4001 South 700 East', '1060 Dalton Ave S'))

    truck_one.depart(datetime(year=2021, month=7, day=28, hour=8, minute=0, second=0))
    print(truck_one.start_time)
    print(greedy_algo(myGraph, truck_one))

    truck_two.depart(datetime(year=2021, month=7, day=28, hour=9, minute=10, second=0))
    print(truck_two.start_time)
    print(greedy_algo(myGraph, truck_two))

    truck_three.depart(datetime(year=2021, month=7, day=28, hour=9, minute=30, second=0))
    print(truck_three.start_time)
    print(greedy_algo(myGraph, truck_three))


    print("\nTRUCK ONE PACKAGE LIST: ")
    for package in truck_one.package_list:
        print(package)

    print("\nTRUCK TWO PACKAGE LIST: ")
    for package in truck_two.package_list:
        print(package)

    print("\nTRUCK Three PACKAGE LIST: ")
    for package in truck_three.package_list:
        print(package)

    print("truck_one: ", truck_one)
    print("truck_two: ", truck_two)
    print("truck_three: ", truck_three)

    print("\ntotal miles: %.2f" % (truck_one.miles + truck_two.miles + truck_three.miles))