class Package:

    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, notes, truck):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.truck = truck
        self.status = 'AT THE HUB'
        self.delivery_time = None

    def deliver(self, delivery_time):
        self.status = 'DELIVERED'
        self.delivery_time = delivery_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state,
                                                   self.zipcode, self.deadline, self.weight, self.notes,
                                                   self.status)

