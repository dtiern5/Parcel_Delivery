from datetime import timedelta

class Truck:

    def __init__(self, name):
        self.name = name
        self.package_list = []
        self.route = []
        self.miles = 0.0
        self.speed = 18
        self.start_time = None
        self.current_time = None
        self.finish_time = None
        self.status = "IN HUB"


    def load(self, package):
        """
        Loads a single package to the truck by appending it to the truck's package_list.
        Also adds the address of the package to the truck's route
        :param package: The package to load onto the truck
        :return: None
        Time Complexity: O(1)
        """
        self.package_list.append(package)
        self.route.append(package[1]) # The address


    def remove(self, package):
        """
        Removes a package from the truck by removing it from the truck's package_list.
        Also removes the address of the package from the truck's route
        :param package: The package to remove from the truck
        :return: None
        Time Complexity: O(1)
        """
        self.package_list.remove(package)
        self.route.remove(package[1]) # The address

    def depart(self, time):
        """
        Updates each package's status in the truck to 'EN ROUTE'
        Sets the start time (for checking on statuses of packages in the UI)
        Sets the current time, which will be incremented at each stop
        :param time: The time the truck departs from the hub
        :return: None
        Time Complexity: O(n)
        """
        for package in self.package_list:
            package.status = "EN ROUTE"
        # Start time for when the truck leaves the HUB
        # Current time will increase at every stop
        self.start_time = time
        self.current_time = time

    def travel(self, miles):
        """
        Updates the miles on the truck at the time given
        :param miles: The number of miles the truck travelled
        :return: None
        Time Complexity: O(1)
        """
        self.miles += miles # Keep track of total miles the truck travels
        added_time = timedelta(minutes=(miles / self.speed) * 60)
        self.current_time += added_time

    def __str__(self):
        return "\nstart time: %s\nmiles: %.2f\nfinish time: %s\nstatus: %s" % (self.start_time, self.miles, self.finish_time, self.status)