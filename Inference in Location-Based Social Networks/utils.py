import math
import sys


def distance_km(a_lat, a_lon, b_lat, b_lon):
    RADS_IN_DEGREE = math.pi / 180.0
    EARTH_MEAN_RADIUS_METERS = 6371009.0
    a_lat_rads = a_lat * RADS_IN_DEGREE
    a_lon_rads = a_lon * RADS_IN_DEGREE
    b_lat_rads = b_lat * RADS_IN_DEGREE
    b_lon_rads = b_lon * RADS_IN_DEGREE

    cos_val = math.cos(a_lat_rads) * math.cos(b_lat_rads) * math.cos(a_lon_rads - b_lon_rads)
    sin_val = math.sin(a_lat_rads) * math.sin(b_lat_rads)
    if abs((cos_val + sin_val) - 1.0) <= sys.float_info.epsilon: return 0.0
    acos_val = math.acos(cos_val + sin_val)
    return (acos_val * EARTH_MEAN_RADIUS_METERS) / 1000.0

