# Referred " http://omega.uta.edu/~gopikrishnav/classes/common/4308_5360/slides/chapter03.pdf and Wikipedia"

import sys
from Queue import Queue
from heapq import heappush,heappop

class priorityQueue(Queue):
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = []
    def _put(self, item):
        return heappush(self.queue,item)
    def _get(self):
        return heappop(self.queue)

def graphBuilding(fileName):
    givenGraph = {}
    file = open(fileName, 'r')
    for eachLine in file:
        if 'END OF INPUT' in eachLine: # If the File reaches End of Input, the program should terminate
            return givenGraph
        nodeA, nodeB, cost = eachLine.lower().split() # Splitting the each line of input, to nodeA, nodeB, the distance as cost
        givenGraph.setdefault(nodeA, []).append((nodeB,cost)) # since given graph is bi directional
        givenGraph.setdefault(nodeB, []).append((nodeA, cost))

def findRoute(givenGraph, source, destination):
    closedSet = set() # The Closed Set Holds all the States
    fringe = priorityQueue() # Fringe is Priority Queue which has the nodes already sorted in path cost - to keep track of visited nodes
    fringe.put((0,[source]))
    while fringe.empty() is False:
        cost, routing = fringe.get()
        vertex = routing[len(routing)-1]
        if vertex not in closedSet:
            closedSet.add(vertex)
            if vertex == destination:
                routing.append(cost) # The cost associated with the vertex has to be appended to routing
                return routing
                print(routing) # If the vertex is matched with the destination which we are looking for we just return the route and print the route
            Neighbours = givenGraph[vertex]
            for nei in [nei[0] for nei in Neighbours]:
                if nei not in closedSet:
                    pos = [node[0] for node in givenGraph[vertex]].index(nei)
                    cummulativeCost = cost + int(givenGraph[vertex][pos][1])
                    croute = routing[:]
                    croute.append(nei)
                    fringe.put((cummulativeCost,croute))

if __name__ == "__main__":
    fileName = sys.argv[1] # Taking all the arguments from command Line - input.txt
    source = str(sys.argv[2]).lower(); # Source Argument
    destination = str(sys.argv[3]).lower(); # Destination Argument
    givenGraph = {}; routing = []
    givenGraph = graphBuilding(fileName) # First will build the graph with the given input file
    if(givenGraph.has_key(source)is False): #validate the source and destination, if found call the findroute to get the route and cost
        print('Given Source is not found in the Input File')
        sys.exit()
    elif(givenGraph.has_key(destination) is False):
        print('Given Destinstion is not found in the Input File')
        sys.exit()
    else:
        routing = findRoute(givenGraph, source, destination)
        if routing:
            cost = routing[-1]
            print('Distance: %s, kilometers'%(cost))
            print('Route: ')
            for var in routing[:-2]:
                var1 = routing.index(var)
                pos = [var2[0] for var2 in givenGraph[var]].index(routing[var1+1])
                cost = givenGraph[var][pos][1]
                print('%s to %s, %s kilometers' %(var,routing[var1+1],cost))
        else: # If there is not route exists for the given source and destination in the given input file, print the following
            print('Distance: Infinity')
            print('Route:' )
            print(routing)
