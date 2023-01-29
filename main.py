import numpy as np
from random import random
from random import shuffle
from numpy.random import randint
from copy import copy
import matplotlib.pyplot as plt #to plot the graph


#city = (x,y) point on 2d graph
class City:
    def __init__(self, x, y, name) -> None:
        self.x = x
        self.y = y
        self.name = name #name of the point

    #print(city) should print the name of the city
    def __repr__(self) -> str:
        return f"{self.name}"


# cities = list of cities in the TSP
class TSP:
    def __init__(self, city_list, start_temp, min_temp, cooling_rate) -> None:
        self.start_temp = start_temp
        self.min_temp = min_temp
        self.cooling_rate = cooling_rate

        #city_list = [(x,y, name)]
        self.cities = [] #list of cities in the problem
        for c in city_list :
            x = c[0]
            y = c[1]
            name = c[2]
            self.cities.append(City(x,y,name))

        #state = list of cities in sequence

    
    #cost function
    # returns sum of edges btw adjecent cities
    def f(self, state) :
        dist = 0
        n = len(state)

        for i in range(0, n-1) :
            #add distance btw city i and city i+1 to the total distance
            city1 = state[i]
            city2 = state[i+1]
            dist = dist + self.distance_btw(city1, city2)

        #now only distance btw last city and first city is left
        dist = dist + self.distance_btw(state[n-1] , state[0])

        return dist


    #return distance btw 2 cities
    @staticmethod
    def distance_btw(c1, c2):
        dist = np.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)
        return dist


    def solve(self):
        #start with a random state
        state = self.cities
        shuffle(state) 
        #print this random solution
        print(f"The initial random solution is {state} and the distance is {self.f(state)}\n")

        #best state found yet
        best_state = state

        #set temp to starting temp
        temp = self.start_temp
        while temp > self.min_temp :
            #neighbour state
            neighbour = self.generate_neighbour(state)

            #should we transition from current state to neighbour state?
            if self.transition(state, neighbour, temp) == True:
                state = neighbour

                #is this new state the best state yet?
                #lower f(x) = better state
                if self.f(state) < self.f(best_state) :
                    #update best state value
                    best_state = state

            #temperature decay
            temp = temp*self.cooling_rate
        ### iterations over ####

        #print the answers
        print(f"The answer is {best_state}. \nThe distance is {self.f(best_state)}\n")
        self.display(best_state)

        return best_state


    
    #generate neighbour state of the current state
    #by swapping any 2 cities randomly
    def generate_neighbour(self, state) :
        #state = #current state
        neighbour = copy(state)

        #random integer in range [0,n-1]
        i1 = randint(0, len(state))
        i2 = randint(0, len(state))

        #swap cities at index i1 and i2
        neighbour[i1] , neighbour[i2] = neighbour[i2] , neighbour[i1]

        return neighbour


    #return true if we should transition state-->neighbour
    def transition(self, state, neighbour, temp) :
        #calculate costs
        current_cost = self.f(state)
        neighbour_cost = self.f(neighbour)

        #if its a good move
        if neighbour_cost < current_cost : #low cost = better state
            return True

        #its a bad move
        # probability of accepting a bad move = value of metropolis function
        diff = current_cost - neighbour_cost
        probability = np.exp( diff/temp )

        if random() < probability :
            return True
        else:
            return False 


    #plot the graph
    def display(self, state) :
        x_coord = []
        y_coord = []
        names = []

        #add each city's coordinates to the list, in sequence
        for city in state:
            x_coord.append(city.x)
            y_coord.append(city.y)
            names.append(city.name) 

        #add the first city again at the end
        x_coord.append(state[0].x)
        y_coord.append(state[0].y)
        names.append(state[0].name)

        #scatter plot
        plt.scatter(x_coord, y_coord)
        #label all points
        for i in range(len(x_coord)):
            plt.annotate(names[i], (x_coord[i], y_coord[i] + 0.2))

        #connect the points with lines 
        plt.plot(x_coord, y_coord)
        plt.show()


############# driver code #####################
#list of cities
num = 13 #number of cities
cities = []
max_dist = 1000
for i in range(num) :
    tup = (max_dist*random(), max_dist*random(), i+1) #(x, y, name)
    cities.append(tup)

#test case
cities2 = [(947.3612445509046 , 872.9585107695043), (942.8609024631703 , 151.5408509461057), (944.7317526958012 , 123.33296895218825), (212.57740899784116 , 653.9571002434129), (188.3908379453012 , 349.25288255239786), (209.70695797968696 , 286.9696061099798), (275.8040347314483 , 17.565098727461482), (406.7735035187862 , 20.57622842965612), (853.7323446491461 , 123.48985777584132), (867.7433164109344 , 311.98198704313063), (962.0845394904624 , 447.4731786842732), (593.2445091792242 , 408.3265323472042), (569.3824107564518 , 485.2592895044864), (364.56046603040005 , 732.5706121326565), (118.60599689859053 , 883.4367479820525), (129.40647626991887 , 965.4524857132357)]
#num = 16
#shortest tot distance found yet = 3773  (image saved in this folder, figure3)
# SimulatedAnnealing(cities2, 10000, 1e-2, 0.98)

tsp = TSP(cities, 1000, 1e-3, 0.98)
tsp.solve()