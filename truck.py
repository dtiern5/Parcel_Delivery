from datetime import datetime, timedelta, time


class Truck:
    package_list = []

    def __init__(self):
        self.package_list = []
        self.route = []
        self.miles = 0.0
        self.speed = 18
        self.start_time = datetime.now()
        self.current_time = datetime.now()
        self.finish_time = datetime.now()
        self.status = "IN HUB"

    def load(self, package):
        self.package_list.append(package)
        self.route.append(package[1])


    def remove(self, package):
        self.package_list.remove(package)
        self.route.remove(package[1])

    def depart(self, time):
        for package in self.package_list:
            package.status = "EN ROUTE"

        self.start_time = time
        self.current_time = time

    def deliver(self, package, miles):
        # self.remove(package)
        self.miles += miles
        added_time = timedelta(minutes = (miles / self.speed) * 60)
        self.current_time += added_time

    def __str__(self):
        return "\nstart time: %s\nmiles: %.2f\nfinish time: %s\nstatus: %s" % (self.start_time, self.miles, self.finish_time, self.status)