import igraph as ig
import numpy as np
from classes.Generator import Generator
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO) #set to debug for printing debug messages

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG) #set to debug for printing debug messages
class TriangleFinder:
    def __init__(self,
                 graph: ig.Graph()
                 ) -> ig.Graph():
        self.graph = graph

        # initialize two all 0 arrays
        # one will keep track of the number of nodes with degree i we encounter
        # the other sums up all the cluster coefficients of nodes with degree i, to compute average later
        self.numOfNodesWithDegree = [0] * graph.vcount()
        self.sumOfClusterCoefficients = [0] * graph.vcount()

        # do the actual finding of triangles
        self.findTriangles()

        # compute the average cluster coefficient by degree
        self.avgClusterCoefficient = [-1] * graph.vcount()
        self.avgTotalClusterCoefficient = 0
        for i in range(graph.vcount()):
            if self.numOfNodesWithDegree[i] != 0:
                self.avgClusterCoefficient[i] = self.sumOfClusterCoefficients[i] / self.numOfNodesWithDegree[i]
                self.avgTotalClusterCoefficient = self.avgTotalClusterCoefficient + self.sumOfClusterCoefficients[i]
        self.avgTotalClusterCoefficient = self.avgTotalClusterCoefficient/(graph.vcount())
        #print(self.avgClusterCoefficient)
        #print(self.avgTotalClusterCoefficient)

    def findTriangles(self):
        for v in self.graph.vs:
            logging.debug(v)
            # note: the size of this neighbours list is the degree of the node
            neighbours = v.neighbors()
            numOfTriangles = 0

            # if it has less than two neighbours, skip it, as it cannot possibly be part of a triangle
            if len(neighbours) > 1 :
                # now that we have the neighbours we can check for triangles by going over each pair of neighbours
                # and checking if said neighbours are themselves connected
                b=len(neighbours)

                for n1 in neighbours:
                    for n2 in neighbours:
                        if n1 != n2:
                            if self.graph.get_eid(n1, n2, directed=False, error=False) != -1:
                                numOfTriangles = numOfTriangles + 1
                        else:
                            pass # Fixing this would mean messing with a lot of index stuff. And it should only happen once of every vertex
                            #raise Exception("Trying to look for triangle with two identical nodes")

                numOfTriangles = numOfTriangles/2 #all triangles get coutned twice
                clusterCoefficient = 2*numOfTriangles / (len(neighbours) * (len(neighbours)-1) )
                logging.debug("The number of triangles is {}".format(numOfTriangles))
                logging.debug("The clusterCoefficient is {}".format(clusterCoefficient))
            else:
                clusterCoefficient = 0

            # add num of triangles and clustercoefficient to the vertex as attributes
            # and include them in the num/sum arrays we initialized earlier
            v["numOfTriangles"] = numOfTriangles
            v["clusterCoefficient"] = clusterCoefficient
            self.numOfNodesWithDegree[len(neighbours)] = self.numOfNodesWithDegree[len(neighbours)] + 1
            self.sumOfClusterCoefficients[len(neighbours)] = self.sumOfClusterCoefficients[len(neighbours)] + clusterCoefficient


if __name__ == '__main__':
    # parameters
    # delta = 0  # model parameter
    # gamma = 0.5  # model parameter
    # beta = 1  # model parameter
    # n = 20  # amount of nodes
    the_graph = Generator(gamma=(1.0+2/3)/2, beta=1, n=100)
    #Generator.draw(the_graph.gtriv)

    triangles1 = TriangleFinder(the_graph.gtriv)
    triangles2 = TriangleFinder(the_graph.ghpa)
    triangles3 = TriangleFinder(the_graph.ghmax)

   # print(triangles1.avgClusterCoefficient)

    graphSizesToTry = [100, 250, 500, 1000, 2500]#, 5000, 10000]
    gammasToTry = [(0.5+2/3)/2, (1.0+2/3)/2]
    betasToTry = [1]
    numberOfRepeats = 10
    for beta0 in betasToTry:
        for gamma0 in gammasToTry:
            for n0 in graphSizesToTry:

                triangles1totalcoeffs = [0.0] * n0
                triangles2totalcoeffs = [0.0] * n0
                triangles3totalcoeffs = [0.0] * n0

                triangles1totalnodesofdeg = [0.0] *n0
                triangles2totalnodesofdeg = [0.0] *n0
                triangles3totalnodesofdeg = [0.0] *n0

                #procedure for repeats is to run numberofrepeats of these simulations
                #then we sum up the clustercoeff for all nodes in all generated graphs(by degree)
                #and divide by number of nodes
                for i in range(numberOfRepeats):
                    the_graph = Generator(gamma=gamma0, beta=beta0, n=n0)
                    #Generator.draw(the_graph.gtriv)

                    triangles1 = TriangleFinder(the_graph.gtriv)
                    triangles2 = TriangleFinder(the_graph.ghpa)
                    triangles3 = TriangleFinder(the_graph.ghmax)

                    for j in range(n0):
                        triangles1totalcoeffs[j] += triangles1.sumOfClusterCoefficients[j]
                        triangles2totalcoeffs[j] += triangles2.sumOfClusterCoefficients[j]
                        triangles3totalcoeffs[j] += triangles3.sumOfClusterCoefficients[j]

                        triangles1totalnodesofdeg[j] += triangles1.numOfNodesWithDegree[j]
                        triangles2totalnodesofdeg[j] += triangles2.numOfNodesWithDegree[j]
                        triangles3totalnodesofdeg[j] += triangles3.numOfNodesWithDegree[j]

                triangles1avgcoeffs = [0.0]*n0
                triangles2avgcoeffs = [0.0]*n0
                triangles3avgcoeffs = [0.0]*n0
                for i in range(n0):
                    if triangles1totalnodesofdeg[i] != 0:
                        triangles1avgcoeffs[i] = triangles1totalcoeffs[i]/triangles1totalnodesofdeg[i]
                    else:
                        triangles1avgcoeffs[i] = -1

                    if triangles2totalnodesofdeg[i] != 0:
                        triangles2avgcoeffs[i] = triangles2totalcoeffs[i]/triangles2totalnodesofdeg[i]
                    else:
                        triangles2avgcoeffs[i] = -1

                    if triangles3totalnodesofdeg[i] != 0:
                        triangles3avgcoeffs[i] = triangles3totalcoeffs[i]/triangles3totalnodesofdeg[i]
                    else:
                        triangles3avgcoeffs[i] = -1

                gtrivCoeffPerDegGraph = "\n\n\n\n\ngtriv n=%d gamma=%f beta=%f\n{" %(triangles1.graph.vcount(), gamma0, beta0)
                #for coeff in triangles1.avgClusterCoefficient:
                for deg in range(len(triangles1.avgClusterCoefficient)):
                    if triangles1avgcoeffs[deg] != -1:
                        gtrivCoeffPerDegGraph += "{%d,%f}," %(deg, triangles1avgcoeffs[deg])
                gtrivCoeffPerDegGraph += "}"
                sys.stdout.write(gtrivCoeffPerDegGraph)
                sys.stdout.write("\n\n total number of nodes with deg")
                print(triangles1totalnodesofdeg)

                gtrivCoeffPerDegGraph = "\n\n\n\n\nghpa n=%d gamma=%f beta=%f\n{" %(triangles2.graph.vcount(), gamma0, beta0)
                #for coeff in triangles1.avgClusterCoefficient:
                for deg in range(len(triangles2.avgClusterCoefficient)):
                    if triangles2avgcoeffs[deg] != -1:
                        gtrivCoeffPerDegGraph += "{%d,%f}," %(deg, triangles2avgcoeffs[deg])
                gtrivCoeffPerDegGraph += "}"
                sys.stdout.write(gtrivCoeffPerDegGraph)
                sys.stdout.write("\n\n total number of nodes with deg")
                print(triangles2totalnodesofdeg)

                gtrivCoeffPerDegGraph = "\n\n\n\n\nghmax n=%d gamma=%f beta=%f\n{" %(triangles3.graph.vcount(), gamma0, beta0)
                #for coeff in triangles1.avgClusterCoefficient:
                for deg in range(len(triangles3.avgClusterCoefficient)):
                    if triangles3avgcoeffs[deg] != -1:
                        gtrivCoeffPerDegGraph += "{%d,%f}," %(deg, triangles3avgcoeffs[deg])
                gtrivCoeffPerDegGraph += "}"
                sys.stdout.write(gtrivCoeffPerDegGraph)
                sys.stdout.write("\n\n total number of nodes with deg")
                print(triangles3totalnodesofdeg)


