# FEEL FREE TO EDIT THIS FILE FOR DEBUGGING PURPOSES,
# BUT GRADING ENVIRONMENT WILL NOT USE YOUR VERSION

# Tips:
#
# If you want to store additional information into this
# given class, or add methods to it, create your own
# classes/subclasses in cp1.py and/or cp2.py.

import copy

class User(object):
    id = -1
    home_lat = -999
    home_lon = -999
    friends = set()
    home_shared = False

    def __init__(self, u_id=-1, u_lat=-999, u_lon=-999, u_home_shared=False):
        if not isinstance(u_id, User):
            self.id = u_id
            self.home_lat = u_lat
            self.home_lon = u_lon
            self.friends = set()
            self.home_shared = u_home_shared
        else:
            self.id = u_id.id
            self.home_lat = u_id.home_lat
            self.home_lon = u_id.home_lon
            self.home_shared = u_id.home_shared
            self.friends = copy.deepcopy(u_id.friends)

    def latlon_valid(self):
       return self.home_lat <= 90 and self.home_lat >= -90 and self.home_lon <= 180 and self.home_lon >= -180
