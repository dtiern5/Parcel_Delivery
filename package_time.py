from datetime import timedelta


def convert_time(time):
    try:
        (h, m, s) = time.split(':')
        datetime_object = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        return datetime_object
    except:
        print("Could not convert to time delta - please check for correct format 'H:mm:ss'")

def check_status_at_time(truck, time):
    status_time = convert_time(time)
    for package in truck.package_list:
        if status_time < truck.start_time:
            package.status = 'AT THE HUB'
        elif status_time < package.delivery_time:
            package.status = 'EN ROUTE on %s' % (truck.name)
        else:
            package.status = 'DELIVERED by %s at %s' % (truck.name, package.delivery_time)
        print(package)