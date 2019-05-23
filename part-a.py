# In this part:
#Cordinates and distanaces are read from exel files
import numpy as np

# This function gets coordinates from coordinates excel file 
def get_coordinates():  
    Coord = np.genfromtxt('Coordinates.csv', dtype='str', delimiter=',', encoding='utf-8').T   
    city_name = Coord[0]
    x = Coord[1].astype(float)
    y = Coord[2].astype(float)
    return city_name, x, y

def get_distances():
# this function returns the total distance of a path
    distance_matrix = np.genfromtxt('distancematrix.csv', dtype='str',delimiter=',', encoding='utf-8')
    distance_matrix[distance_matrix==''] = 0 
    return distance_matrix

city_name, x, y  = get_coordinates()
distances = get_distances()