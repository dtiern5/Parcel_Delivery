from datetime import timedelta


def convert_time(time):
    try:
        (h, m, s) = time.split(':')
        datetime_object = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        return datetime_object
    except:
        print("Could not convert to time delta - please check for correct format 'H:mm:ss'")


def check_packages_by_truck(truck, time):
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
    for p in range(1, 41):
        print_single_package_by_time(hash_table, time, p)


def print_single_package_by_time(hash_table, time, package_id):
    package = hash_table.search(package_id)
    status_time = convert_time(time)

    if package.preferredTruck == '1':
        start_time = convert_time('8:00:00')
    if package.preferredTruck == '2':
        start_time = convert_time('9:05:00')
    if package.preferredTruck == '3':
        start_time = convert_time('10:00:00')

    if status_time < start_time:
        package.status = 'AT THE HUB'
    elif status_time < package.delivery_time:
        package.status = 'EN ROUTE on Truck %s' % package.preferredTruck
    else:
        package.status = 'DELIVERED by Truck %s at %s' % (package.preferredTruck, package.delivery_time)
    print(package)


# def check_all_packages_at_time(hash_table, time):
#     status_time = convert_time(time)
#     for p in range(0, 40):
#         package = hash_table.search(p + 1)
#
#         if package.preferredTruck == '1':
#             start_time = convert_time('8:00:00')
#         if package.preferredTruck == '2':
#             start_time = convert_time('9:05:00')
#         if package.preferredTruck == '3':
#             start_time = convert_time('10:00:00')
#
#         if status_time < start_time:
#             package.status = 'AT THE HUB'
#         elif status_time < package.delivery_time:
#             package.status = 'EN ROUTE on Truck %s' % package.preferredTruck
#         else:
#             package.status = 'DELIVERED by Truck %s at %s' % (package.preferredTruck, package.delivery_time)
#         print(package)
