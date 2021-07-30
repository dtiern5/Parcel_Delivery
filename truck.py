from datetime import datetime, timedelta, time


class Truck:
    package_list = []

    # Time complexity: O(1)
    # Space complexity: O(1)
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

    # Time complexity: O(1)
    # Space complexity: O(1)
    def load(self, package):
        self.package_list.append(package)
        self.route.append(package[1]) # The address

    # Time complexity: O(1)
    # Space complexity: O(1)
    def remove(self, package):
        self.package_list.remove(package)
        self.route.remove(package[1]) # The address

    # Time complexity: O(n)
    # Space complexity: O(1)
    def depart(self, time):
        for package in self.package_list:
            package.status = "EN ROUTE"
        # Start time for when the truck leaves the HUB
        # Current time will increase at every stop
        self.start_time = time
        self.current_time = time

    # Time complexity: O(1)
    # Space complexity: O(1)
    def travel(self, miles):
        self.miles += miles # Keep track of total miles the truck travels
        added_time = timedelta(minutes=(miles / self.speed) * 60)
        self.current_time += added_time

    def __str__(self):
        return "\nstart time: %s\nmiles: %.2f\nfinish time: %s\nstatus: %s" % (self.start_time, self.miles, self.finish_time, self.status)