from user import User
from utils import distance_km
import csv
from logging import warn, error, debug
import numpy
import pandas
import matplotlib
import statistics


def cp2_1_simple_inference(dictUsers):
    dictUsersInferred = dict()  # dict to return, store inferred results here
    # you should keep everything in dictUsers as is / read-only
    for i in dictUsers.values():
        # home location not share
        if i.home_shared == False:
            #initialize lat, lon, shared all to 0
            sum_lat = 0
            sum_lon = 0
            friends_share_loca = 0
            for f in i.friends:
                friends = dictUsers[f]
                if friends.home_shared == True:
                    # if homeLoc is shared then return home Loc
                    sum_lat = sum_lat + friends.home_lat
                    sum_lon = sum_lon + friends.home_lon
                    friends_share_loca += 1
            if friends_share_loca != 0 :
                avg_lat = sum_lat / friends_share_loca 
                avg_lon = sum_lon / friends_share_loca
                user = User(i.id, avg_lat, avg_lon, True)
            else:
                #no share, a user without home location
                user = User(u_id = i.id, u_home_shared = False)
            dictUsersInferred[i.id] = user
        else:
            dictUsersInferred[i.id] = i   
    return dictUsersInferred

# get the idea of the campuswire and calculate the median
def cp2_2_improved_inference(dictUsers):
    dictUsersInferred = dict()
    # Leverage shared home locations of friends of friends
    # friends of friends at least 1 me + 1 friend + 1 friend's friend = 3
    # 3 is better compare 4 or 5
    threshold = 3
    for i in dictUsers.values():
        # same as above
        if i.home_shared == False:
            lat = []
            lon = []
            friends_share_loca = 0
            for f in i.friends:
                friends = dictUsers[f]
                if friends.home_shared == True:
                    lat.append(friends.home_lat)
                    lon.append(friends.home_lon)
                    friends_share_loca += 1
            # if the number of friends had shared their home locations is below a certain threshold
            if friends_share_loca < threshold:
                for f in i.friends:
                    #compute the geographic center of the shared home locations of friends of friends
                    friends = dictUsers[f]
                    for ff in friends.friends:
                        fof = dictUsers.get(ff)
                        if fof and fof.home_shared:
                            lat.append(fof.home_lat)
                            lon.append(fof.home_lon)
                            friends_share_loca += 1
            if lat and lon:
                lat.sort()
                lon.sort()
                med_lat = lat[len(lat) // 2]
                med_lon = lon[len(lon) // 2]
                # even to find median
                if len(lat) % 2 == 0:
                    med_lat = (med_lat + lat[len(lat) // 2 - 1]) / 2
                    med_lon = (med_lon + lon[len(lon) // 2 - 1]) / 2
                user = User(i.id, med_lat, med_lon, True)
            else:
                user = User(u_id = i.id, u_home_shared = False)
        else:
            user = i
        dictUsersInferred[i.id] = user
    return dictUsersInferred
            


                            
def cp2_calc_accuracy(truth_dict, inferred_dict):
    # distance_km(a,b): return distance between a and be in km
    # recommended standard: is accuate if distance to ground truth < 25km
    if len(truth_dict) != len(inferred_dict) or len(truth_dict)==0:
        return 0.0
    sum = 0
    for i in truth_dict:
        if truth_dict[i].home_shared:
            sum += 1
        elif truth_dict[i].latlon_valid() and inferred_dict[i].latlon_valid():
            if distance_km(truth_dict[i].home_lat, truth_dict[i].home_lon, inferred_dict[i].home_lat,
                           inferred_dict[i].home_lon) < 25.0:
                sum += 1
    return sum * 1.0 / len(truth_dict)




