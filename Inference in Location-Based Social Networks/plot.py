import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap


# Draws a map plotting geolocation of uid and uid's friends
def draw_map(uid, dictUsers):
    plt.figure(figsize=(16, 9))
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.bluemarble()
    if dictUsers[uid].latlon_valid():
        m.scatter(x=dictUsers[uid].home_lon,y=dictUsers[uid].home_lat,s=10,c='red',latlon=True)
        print("Plotting user {}".format(uid))
    else:
        print("user {} invalid, skipping...".format(i))

    for i in dictUsers[uid].friends:
        if dictUsers[i].latlon_valid():
            m.scatter(x=dictUsers[i].home_lon,y=dictUsers[i].home_lat,s=7,c='yellow',latlon=True)
            print("Plotting user {}".format(i))
        else:
            print("user {} invalid, skipping...".format(i))
    plt.title("friends for user {}".format(uid))
    plt.show()
