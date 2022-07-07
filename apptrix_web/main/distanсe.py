from math import sin, cos, atan, sqrt, pi, radians


def dist(long1, lat1, long2, lat2):
    R = 6371.009  # km
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])
    delta = abs(long1 - long2)

    angle = atan(
        sqrt((cos(lat2) * sin(delta)) ** 2 + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta)) ** 2) /
        (sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(delta))
    )
    return angle * R
