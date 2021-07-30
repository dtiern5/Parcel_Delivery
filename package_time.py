from datetime import timedelta


def convert_time(time):
    """
    Converts string to timedelta for use in incrementing times during delivery stops.
    Performs this by splitting the string at ':' and creating a new timedelta object.
    :param time: The string to convert
    :return: The string converted to timedelta
    Time complexity: O(1)
    """
    try:
        (h, m, s) = time.split(':')
        delta_object = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        return delta_object
    except:
        print("Error: Time format is incorrect")


def check_packages_by_truck(truck, time):
    """
    Prints each package's status in a given truck at a given time.
    Does so by checking the time against when the truck leaves the hub, and when
    the package should be delivered, and then updating the package status.
    :param truck: The truck whose package statuses are to be checked
    :param time: A string representing the timestamp we want to check
    :return: None
    Time complexity: O(n)
    """
    status_time = convert_time(time)
    for package in truck.package_list:
        if status_time < truck.start_time:
            package.status = 'AT THE HUB'
        elif status_time < package.delivery_time:
            package.status = 'EN ROUTE on %s' % truck.name
        else:
            package.status = 'DELIVERED by %s at %s' % (truck.name, package.delivery_time)
        print(package)


def print_all_packages_at_time(hash_table, time):
    """
    Prints every package within a hash table at a given time
    :param hash_table: The hash table containing the packages
    :param time: The time to check on the status of the packages
    :return: None
    Time complexity: O(1) (We know we have 40 packages, so we run the loop a constant 40 times)
    """
    for p in range(1, 41):
        print_single_package_by_time(hash_table, time, p)


def print_single_package_by_time(hash_table, time, package_id):
    """
    Prints the status of a single package at a given time
    Does so by checking the time against when the truck leaves the hub, and when
    the package should be delivered, and then updating the package status.
    :param hash_table: The hash table containing the package
    :param time: The time to check on the status of the package
    :param package_id: The ID of the package to check
    :return: None
    Time Complexity: O(1)
    """

    package = hash_table.search(package_id)
    status_time = convert_time(time)

    # Truck one leaves at 8:00:00, truck two leaves at 9:05:00, and truck three at 11:00:00
    if package.truck == '1':
        start_time = convert_time('9:05:00')
    if package.truck == '2':
        start_time = convert_time('9:05:00')
    if package.truck == '3':
        start_time = convert_time('11:00:00')

    if status_time < start_time:
        package.status = 'AT THE HUB'
    elif status_time < package.delivery_time:
        package.status = 'EN ROUTE on Truck %s' % package.truck
    else:
        package.status = 'DELIVERED by Truck %s at %s' % (package.truck, package.delivery_time)
    print(package)
