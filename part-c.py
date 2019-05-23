import numpy as np
import matplotlib.pyplot as plt

# This function gets coordinates from coordinates Excel file 
def get_coordinates():  
    Coord = np.genfromtxt('Coordinates.csv', dtype='str', delimiter=',', encoding='utf-8').T   
    x = Coord[1].astype(float)
    y = Coord[2].astype(float)
    city_name = Coord[0]
    return city_name, x, y, 

# This function creates a random path
def route(n):
#    start = np.where(city_name=='Ankara') # starting point
    random_route = np.arange(n)
#    random_route = np.delete(random_route, start)
    np.random.shuffle(random_route)
#    random_route = np.insert(random_route, 0, start)
    random_route = np.append(random_route, random_route[0])
    return random_route

def distance(path):
    # this function returns the total distance of a path
    distance_matrix = np.genfromtxt('distancematrix.csv', dtype='str',delimiter=',', encoding='utf-8')
    distance_matrix[distance_matrix==''] = 0
    
    route_distance = 0
    for i,j in zip(path[:-1],path[1:]):
        route_distance += float(distance_matrix[i+1, j+1])
    return route_distance

def draw_route(path):
    for i,j in zip(path[:-1],path[1:]):
        plt.plot([x[i],x[j]],[y[i],y[j]],'-o')
        plt.show()
       
# SIMULATED ANNEALING ALGORITHM: 
city_name, x, y  = get_coordinates()
n= len(x)
random_route= route(n)

def swap(path):
# generate two random indeces to swap.
      i, j = np.random.randint(n, size=2)
      i1, i2 = path[[i, j]]
      # swap the values
      path[i], path[j] = i2, i1
      path = np.append(path, path[0])
      return path

# Calculating the probabily for accepting a path as a solution
def probability(route, new_route, temperature):
      # if the new path is shorter, accept it
      if new_route <= route:
            return 1
      # if the new path is longer, calculate the probability; used to get out of local minima.
      return np.exp((route-new_route)/temperature)

# Assume initial path is the shortest.
shortest_route = random_route
shortes_dist = distance(shortest_route)

# Temperature Data:
temp = 100 # initial temp.
cooling_rate = 0.00001 # cooling rate.
# Distance and Temperature array:
distances   = [shortes_dist]
temperatures = [temp]
# performance tracking
# Iterations:
i = 1
while temp > 0.1:
      
      new_path = swap(random_route[:-1].copy())   
      current_dist = distance(random_route)
      new_dist = distance(new_path)
      
      # keep track of the shortest path
      if new_dist < shortes_dist:
            shortes_dist = new_dist
            shortest_path = new_path
      if probability(current_dist, new_dist, temp) > np.random.rand():
            random_route = new_path
      temp *= 1 - cooling_rate  # Cool system
      temperatures.append(temp)
      distances.append(new_dist)

      print('iteration', i, 'shortest distance: %5.2f - temp: %4.5f'%(shortes_dist, temp))
      i += 1
      
a = np.where(city_name=='Ankara') # starting point
if shortest_route[0] != a[0]:
      shortest_route = np.delete(shortest_route,0)
      b = shortest_route[:int(np.where(shortest_route==a[0])[0])]
      c = shortest_route[int(np.where(shortest_route==a[0])[0])+1:]
      shortest_route = np.concatenate([np.array(a[0]), c, b, np.array(a[0])])
print('the shortest path is: ', shortest_route, '\nwith minimum distance= ', shortes_dist)

def plot_path(path, label, p):

      for i, j in zip(path[:-1], path[1:]):
            plt.plot([x[i],x[j]], [y[i], y[j]], 'r:')
            plt.plot([x[i],x[j]], [y[i], y[j]], 'o')
      plt.title(label)
      plt.text(41,44,'Shortest route distance:%s'%shortes_dist)
plt.figure(1)  
plot_path(shortest_path, 'Shortest Route',1)
plt.plot(x[5],y[5],'k*',ms=20,lw = 2)
plt.show()
plt.figure(2)
plt.plot(distances,'.-')

