# Parcel_Delivery
WGUPS Parcel Delivery Application
C950 Data Structures and Algorithms II
Daniel Tierney
dtiern5@wgu.edu
August 1, 2021


A.  Identification of a named algorithm

	A nearest neighbor algorithm was implemented for this project. A nearest neighbor algorithm decides what is the optimal next step, with disregard to the optimization of the following steps. The algorithm is very simple to understand, and leads to maintainable and relatively efficient code. It performs at a time complexity of O(n^2). 
	The chosen algorithm makes some sacrifices in performance for ease of use and maintainability. There are other algorithms that would better optimize the total miles travelled by the trucks, and algorithms that would better optimize the time complexity. These are discussed in section I3.


B. Overview of program (including pseudocode)

The program starts by running main().

It creates an empty ChainingHashTable and three truck objects. It then simultaneously populates the hash table with the data from ‘WGUPS Package Data.csv’ and loads the trucks with their associated packages (CSV is modified to manually load the trucks, a new column was created with numbers ‘1’, ‘2’, and ‘3’)

A graph is created from ‘WGUPS Distance Table.csv’ using the addresses as vertices and the distances between them as edges.

The trucks are then given a time to start their route. Truck one leaves at 8:00 and truck two leaves at 9:05, when the late packages arrive. These trucks have all of the packages with deadlines. Packages 3, 18, 36, and 38 are correctly on the second truck.
The grouped packages 13, 14, 15, 16, 19, and 20 are all on the first truck. The package with the missing address (package 9) is placed on the third truck.

The first truck returns at 10:44:40, so we use that driver to depart the third truck at 10:45:00.

The UI then starts, prompting the user for input. It will show any package and truck information needed at any given time of the day.

All packages meet their deadlines and all of this information can be found through the UI.
The Nearest Neighbor Algorithm performs in the following manner:
	1. Create a list of all unvisited locations that a truck must visit on its route 
	2. Instantiate a list of all visited locations in the order they are visited 
	3. While that unvisited locations list is not empty, we iterate through finding the shortest distance to any location on the list from the truck’s current location 
	4. When that location is determined, the truck can travel to drop off the requisite 	packages. The location is removed from the unvisited locations list in order to ensure we do not visit the same location twice. The location is also appended to the visited locations list in order to convey the truck’s current location. 
	5. Once the unvisited list is exhausted, a final destination is set to the hub to bring the truck back. 



Pseudocode:
unvisited_list = all addresses in the truck’s route
start  = HUB address
visited_list = [start]
distance_list = edge weights from graph
while unvisited_list has addresses:
	shortest_distance = None
	next_address = None
	for each address in the unvisited_list:
		distance = distance between address and last location in visited_list
if distance is first to be checked or if distance is less than shortest_distance:
	shortest_distance = distance
	next_address = address
	append address to visited_list
	remove address from unvisited_list
Set a final destination to the HUB in order to return the truck


B2. Programming environment

	This application was created using Python 3.8 and the PyCharm IDE. Data provided by WGU was in .xlsx format. It was exported to .csv and cleaned up for ease of use with Python. Everything was completed on a local Apple MacBook Air M1 with 16GB RAM.


B3. Space-time complexity

	Each major segment of code has its space-time complexity documented within the docstrings just after the definition of each function. The entire program has a space-time complexity of O(n^2), as both the algorithm and the creation of the graph perform at O(n^2).


B4. Ability to scale and adapt to increasing number of packages

	There are improvements to be made relating to scalability. In its current form, the program needs manual input to determine which packages should go on which truck. This could prove to be ineffective as the number of packages grows. The program would fare better in scalability if an algorithm performed this task instead. In order to do so, we would need consistency in the structure of “Special notes” for each of the packages so the program could dictate which packages must travel together, be delayed, or be rushed in an earlier shipment. We could then group packages by zip codes to try and match the efficiency of manual selection.
 
	Using CSV should remain efficient with a larger number of packages. Data can then be manipulated in excel before export to CSV for the application to use. 
 
	More packages could mean that WGUPS would need to purchase additional trucks and hire additional drivers. More efficiency in loading could lead to an increase in average mph of the trucks. These are very easy changes to make within the code. Average truck speed can be changed within the initialization of truck objects, and that change will be reflected throughout the application. Adding an additional driver or truck simply takes a few lines of code in main().
 
	The nearest neighbor algorithm should perform just as well with more locations, although looking into a more efficient solution could be beneficial as scale increases.


B5. Efficiency and maintainability of the software
	
	As discussed previously, the algorithm itself is simple to understand and relatively efficient with an O(n^2) time complexity. If someone new was brought in to maintain the code they would have no trouble seeing how the overall program functions. Any changes in truck speed can currently be done within the constructor. Adding options to change the number of trucks, truck capacity, speed, and start times could be added to the UI as well for ease of use. The code is also heavily documented for clarification at potentially unclear or complicated points.


B6. Strengths and weaknesses of the hash table
	The main strength of the hash table is its high performance and quick lookup times. While the worst case is O(n), the average time complexity to look up an item is O(1). They also create and delete entries with efficiency. The time complexity is constant regardless of the number of items in the table.
	Hash tables come with their own set of weaknesses. Large data sets produce more unavoidable collisions, which increases the bucket size and reduces efficiency of searching. Resizing of the hash table can help mitigate these problems. Hash tables also perform best when the maximum number of entries is known in advance.


C1.  Create an identifying comment within the first line of a file named “main.py” that includes your first name, last name, and student ID.

Completed in line 1 of main.py
“Daniel Tierney, Student ID: #001510821”


C2. Include comments in your code to explain the process and the flow of the program.

	The code is commented throughout, with special attention to make sure the algorithm and creation of the graph are clear
D1. Identification of a self-adjusting data structure

	The self-adjusting data structure I chose to store the package data is a chaining hash table. “Chaining handles hash table collisions by using a list for each bucket, where each list may store multiple items that map to the same bucket” (Lysecky, Vahid). 
	It operates with key-value pairs. For this application, the IDs of the packages makes perfect sense to use as a key, with the packages themselves being values. The key is hashed, and then placed into the appropriate bucket.
	The number of buckets is set, but the size of the bucket is self-adjusting, with entries stored in a list. The hash table adapts when new data is added to it, making that data accessible. The worst case search time is O(n), but it’s average case is a constant O(1), making a hash table suitable for efficient retrieval of data.


E. Develop a hash table

	The hash table has its own class called ChainingHashTable in hash_table.py.
	The hash table storing the package data is created using the hash_packages function in main.py. That function is called one time from main().


F. Develop a look-up function

	The look-up function is the pain purpose of the UI. A list of options will be given on startup of the application. The user types the number and presses enter, then follows the prompts.

	All times must be given in “hh:mm:ss” format or an exception informs the user of their error.

	Using the UI, the user can look up the status of:
		1. Any individual package
		2. Every package
		3. Packages loaded to a specific truck
	The user can also check the total travel distances of any and all trucks, as well as the routes taken, finish time, and number of packages on each truck.
  

Justification for the core algorithm including:
	I1. Two strengths
	I2. Verification that the algorithm meets the requirements in the scenario

	The nearest neighbor algorithm makes sacrifices to both time-complexity and optimization of its result, but it makes up for these in its simplicity and ease of use. Other algorithms will outperform it in different ways, but they all have advantages and disadvantages.
The main advantages of the Nearest Neighbor Algorithm are its ease of implementation and its relative efficiency. It is also very simple to understand, making it maintainable, and even flexible if changes were needed in the future.
	Another key advantage is that it gives a reasonable enough solution that other algorithms can work to improve, even if it isn’t immediately the optimal solution. For example: the 2-opt algorithm discussed in section I3 could be used to further optimize the results from the nearest neighbor algorithm.
	The algorithm managed to create routes that delivered all packages before their deadline, and minimized the total miles travelled by the trucks to a reasonable degree.


I3. Identification of two other algorithms that could be used, and how they differ
	A Greedy Algorithm would perform better than the Nearest Neighbor algorithm chosen for this project. A greedy algorithm performs at O(n). It would first sort all of the possible distances in the truck’s route (edges of the graph), and then begin creating a route by adding the shortest distances, without repeating a vertex, until a cycle is formed [1]. I believe switching to a greedy algorithm for this application would be an overall improvement.
 
	The 2-opt algorithm could also be implemented, likely resulting in less miles for the trucks. The algorithm, however, would take more time and space to execute. Using the result of the Nearest Neighbor algorithm (or any other solution), 2-opt works by removing two edges from the route, and reconnecting the route in the only available way. If the solution leads to a shorter overall travel time, then the route is updated [3]. This will generally repeat a set number of times.

J. Things to be done differently on a repeat of this project

	I struggled for quite a while importing the distance CSV and putting its data into an undirected graph. I eventually decided to fill in the rest of the CSV, simplifying the process. After working with the data, I’ve come to realize my errors. I think going back and updating the logic of searching the table would be beneficial, as the project could be completed without manipulating the CSV. In a real world setting, this would save time and labor as well.
	This would be done by simply checking if the distance between address_1 and address_2 was empty in the table. If so, we would simply return the distance of those addresses swapped (address_2 and address_1). We can only do this because the distances for this project are bi-directional. In a real world setting, this may not be the case, and we would need the entire CSV filled in with the relevant distances.
	
	I also struggled to come up with an algorithm for sorting the packages and loading the trucks. I ended up doing so manually. After getting more experience with the data, I can see some ways to efficiently automate the loading of the trucks.
	First, parsing the Special notes and placing those packages on the requisite trucks. Placing late arrivals with the 10:30 deadline on truck 2, and the rest of the late arrivals on truck 3. Other packages with early deadlines would then be loaded on truck 1. For the rest of the packages, I could separate the zip codes and try to group the packages near each other to be delivered together. All of this may or may not reduce the mileage on the trucks, but it could save labor for this hypothetical service in the future and is worth exploring.
 
	There are some small artifacts throughout the project that I could change as well. I started by updating the status of packages and trucks in real time (when a truck departs, all of its packages are updated to “EN ROUTE,” and when delivered, they are updated to “DELIVERED.” In the end, this proved to be unnecessary, as my calls to display data simply check where the package is at that time, and update the status accordingly. So those statuses are only relevant to the user when those functions to display data are called.


K1. Justification for the data structure and verification that it meets all requirements, including explanations on how changes to number of trucks, packages, and cities would affect the data structure

	The larger the set of packages becomes, the more collisions will occur in the hash table. This can lead to longer look-up times as more packages are stored in each bucket. We want to create a hash table that spreads out data for efficient look up times. This could mean altering the number of buckets in larger datasets. 
	Hash tables are generally implemented as an array with linked-lists as buckets. Since searching the hash is much more efficient than searching the buckets, we want to limit the amount of packages in each bucket. On the other hand, creating a larger hash table takes more memory, some of which may not be used. If WGUPS continues to increase their daily deliveries, determining an effective hash table size would be beneficial in order to minimize the space taken by the hash table, and maximize the efficiency of the look-up function.
	Changing the number of trucks or cities would not affect the look-up time or space usage of the data structure. Changing the number of packages would, as the look-up time is O(n). The trucks and addresses associated with the packages in the hash table are stored within the package itself.


K2. Identification of two other data structures that could be used, and how they differ

Package data could be stored in a list of lists, with each inner list holding all of the data for an individual package. This would slow down lookup time, but it would give us the ability to iterate over the data. Python also allows lists to contain objects of differing types, which would be beneficial in storing package information that contains integers and strings.
 
Another option would be to use a queue. A queue would allow us to place higher priority packages (with earlier delivery deadlines) towards the beginning of the queue. We could optimize distance by prioritizing clusters of addresses nearby each other, trusting that the queue would deliver the higher priority packages first. It’s possible that this change could allow truck 3 to deliver packages before the 10:30 deadline as well.



Works Cited
[1] https://en.wikipedia.org/wiki/Travelling_salesman_problem
[2] Lysecky, Roman, and Frank Vahid. C950: Data Structures and Algorithms II. zyBooks.com, learn.zybooks.com/zybook/WGUC950AY20182019. 
[3] G. A. CROES, ‘‘A method for solving traveling salesman problems,’’ Operations Res. 6 (1958).
