import csv
from logging import warn, error, debug
from user import User
import numpy
import pandas
import matplotlib
import statistics


## parse homes.txt
#  input:
#    f: filename
#  output:
#    a dict of all users from homes.txt with key=user_id, value=User object
def cp1_1_parse_homes(f):
    dictUsers_out = dict()
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            id = int(i[0].strip())
            # id is the primary attribute, always have id
            # some other factors may lost in dataset2
            if len(i) > 1:
                # strip() integers not the string
                home_lat = float(i[1].strip())
                home_lon = float(i[2].strip())
                home_shared = bool(int(i[3].strip()))
                user = User(id, home_lat, home_lon, home_shared)
            else:
                user = User(u_id = id, u_home_shared = False)
            #dictUsers_out.update(((id, user),))
            dictUsers_out[id] = user         
              
    return dictUsers_out               



## parse friends.txt
#  input:
#    f: filename
#    dictUsers: dictionary of users, output of cp1_1_parse_homes()
#  no output, modify dictUsers directly
def cp1_2_parse_friends(f, dictUsers):
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            id1 = int(i[0].strip())
            id2 = int(i[1].strip())
            #You may assume all users referenced in a friends.txt exist in homes.txt.
            #if id_1 in dictUsers and id_2 in dictUsers:
            # add each in the other's friends set
            dictUsers[id1].friends.add(id2)
            dictUsers[id2].friends.add(id1)
            
            


# return all answers to Checkpoint 1.3 of MP Handout in variables
# order is given in the template
def cp1_3_answers(dictUsers):
    # TODO: return your answers as variables in the given order
    #1
    u_cnt = len(dictUsers)
    #2 unknow locations should be user.home_shared is False
    u_noloc_cnt = sum(1 for user in dictUsers.values() if  user.home_shared is False)
    #3
    u_noloc_nofnds_cnt = sum(1 for user in dictUsers.values() if user.home_shared is False and len(user.friends) == 0)
    number_shared_locations = sum(user.home_shared for user in dictUsers.values())
    #4
    p_b = number_shared_locations / u_cnt
    #5
    number_correctly_inferred1 = sum(1 for user in dictUsers.values() if user.home_shared is False and len(user.friends) > 0)
    p_u1 = (number_shared_locations + number_correctly_inferred1) / u_cnt 
    #6
    number_correctly_inferred2 = sum(1 for user in dictUsers.values() if user.home_shared is False and any(dictUsers[friend].home_shared for friend in user.friends))
    p_u2 = (number_shared_locations + number_correctly_inferred2) / u_cnt
    return u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2




