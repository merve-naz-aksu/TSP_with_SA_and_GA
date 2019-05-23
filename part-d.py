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
    start = np.where(city_name=='Ankara') # starting point
    random_route = np.arange(n)
    random_route = np.delete(random_route, start)
    np.random.shuffle(random_route)
    random_route = np.insert(random_route, 0, start)
    random_route = np.append(random_route, random_route[0])
    return random_route

# This function gets distances from distancematrix Excel file 
def measure_route(apath):

    distance_matrix = np.genfromtxt('distancematrix.csv', dtype='str',delimiter=',', encoding='utf-8')
    distance_matrix[distance_matrix==''] = 0 
    total = 0    
    def distance(i,j,distance_matrix):
   # this function returns the total distance of a path
        return float(distance_matrix[i+1, j+1])

    for i,j in zip(apath[:-1],apath[1:]):
        d=distance(i,j,distance_matrix)
        total = total + d
    return total

def draw_route(path):
    for i,j in zip(path[:-1],path[1:]):
        plt.plot([x[i],x[j]],[y[i],y[j]],'-o')
        plt.show()
        
city_name, x, y  = get_coordinates()
n           = len(x)
random_route= route(n)
total = measure_route(random_route)
print('Random route map:',random_route)
print('Total distance of random route:',total,'km')
# GENETIC ALGORITHM : 
def create_initial_population(n):
    #creates and sorts an initial population of size n.
    l=len(x)   
    population = []

    for i in range(n):
        p = route(l)
        population.append(p)
    population=np.array(population)
    population = sort_population(population)    
    return population

def population_performance(population):
    # returns an array that stores the performance of each path of a population
    perf = []
    for i in population:
        perf.append(measure_route(i))
    return np.array(perf)

def sort_population(population):
    #sort the population according to its performance, (total distance)
    performance = population_performance(population)
    i = np.argsort(performance)
    return population[i]

def cross_over(route1, route2,mutation=0.5):
    # this function uses two route and generate a daughter routh which called as new_route    
    # pop the last elements that repeat the first one.
    route1 = route1[:-1]
    route2 = route2[:-1]
    k     = np.random.randint(0,n) # cross over location
    new_route = np.hstack((route1[:k], route2[k:]))
       
    # Repeated number :
    unique, counts = np.unique(new_route, return_counts=True)
    d = dict(zip(unique, counts))
    replace=[]
    for i in d:
        if d[i]==2:
            replace.append(i)
    # Missing number:
    if len(set(new_route))!=len(set(route2)):
        missing = list(set(route1)-set(new_route))
        for i,j in zip(replace,missing):
            if np.random.rand()<mutation:
                index=np.where(new_route==i)[0][0]
            else:
                index=np.where(new_route==i)[0][1]            
            new_route[index]=j
    # MUTATION:
    # introduce random mutation by swapping two points, keep the start and end points
    if np.random.rand()>mutation:
        i1,i2 = np.random.randint(0,n,2)
        new_route[i1], new_route[i2] = new_route[i2], new_route[i1]
    #Append the first element to the new_route
    new_route = np.append(new_route,new_route[0])
    return new_route

def multiply(population,n):
    # reproduces the best n individuals of a population to produce n*n new indivioduals and sorts the new population
    # return the sorted new population  
    population=population[:n]
    new_pop = []
    for i in population:
        for j in population:
            new_pop.append(cross_over(i,j))
    new_pop = np.array(new_pop)
    new_pop = sort_population(new_pop)
    return new_pop
# Calling :
population  = create_initial_population(82)
shortest_dist = measure_route(population[0])
shortest_route = population[0]

performance_list = []
i = 0
try:
      while True:
          i += 1
          print('generation', i, 'best performance %5.2f'% measure_route(population[0]))
          performance_list.append(measure_route(population[0]))
         
          population = multiply(population,10)
          if measure_route(population[0]) < shortest_dist:
                shortest_dist = measure_route(population[0])
                shortest_route = population[0]
except KeyboardInterrupt:
      start = np.where(city_name=='Ankara') # starting point
      if shortest_route[0] != start[0]:
            shortest_route = np.delete(shortest_route,0)
            b = shortest_route[:int(np.where(shortest_route==start[0])[0])]
            c = shortest_route[int(np.where(shortest_route==start[0])[0])+1:]
            shortest_route = np.concatenate([np.array(start[0]), c, b, np.array(start[0])])
      pass

#PRINT:
print("\nThe shortest route map:",shortest_route)
print('Found Min distance=',shortest_dist)
# PLOTS:
plt.figure(1)
draw_route(population[0])
plt.plot(x[5],y[5],'k*',ms=20,lw = 2)
plt.title('Shortest route with Genetic Algorithm')
plt.figure(2)
plt.title('Performance')
plt.plot(performance_list,'.-')
plt.show()

