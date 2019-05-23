# In this part:
#Cordinates and distanaces are read from exel files
#A random route is created which start from ANKARA, visits every other city and returns back to Ankara
#Then calculate the total distance of the route.

import numpy as np
import matplotlib.pyplot as plt

# This function gets coordinates from coordinates excel file 
def get_coordinates():  
    Coord = np.genfromtxt('Coordinates.csv', dtype='str', delimiter=',', encoding='utf-8').T   
    city_name = Coord[0]
    x = Coord[1].astype(float)
    y = Coord[2].astype(float)
    
    return city_name, x, y

# This function creates a random path
def route(n):
    start = np.where(city_name=='Ankara') # starting point
    random_route = np.arange(n)
    random_route = np.delete(random_route, start)
    np.random.shuffle(random_route)
    random_route = np.insert(random_route, 0, start)
    random_route = np.append(random_route, random_route[0])
    return random_route

# This function gets distances from distancematrix excel file 
def measure_route(apath):
           # this function returns the total distance of a path
    distance_matrix = np.genfromtxt('distancematrix.csv', dtype='str',delimiter=',', encoding='utf-8')
    distance_matrix[distance_matrix==''] = 0 
    
    def distance(i,j,distance_matrix):
        return float(distance_matrix[i+1, j+1])
    
    total = 0
    for i,j in zip(apath[:-1],apath[1:]):
        d=distance(i,j,distance_matrix)
        total = total + d
    return total

def draw_route(path):
    for i,j in zip(path[:-1],path[1:]):
        plt.plot([x[i],x[j]],[y[i],y[j]],'-o')
        plt.show()
        
# setting vars: x-coord, y-coord ... etc.
city_name, x, y  = get_coordinates()
n           = len(x)
random_route= route(n)
total = measure_route(random_route)
# PRINT:
print('Total distance of random route:',total,'km')
#PLOT:
plt.figure()
plt.title ('Random Route')
draw_route(random_route)
plt.plot(x[5],y[5],'k*',ms=20,lw = 2)




