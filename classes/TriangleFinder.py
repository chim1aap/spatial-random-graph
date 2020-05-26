import igraph as ig
import numpy as np
from classes.Generator import Generator

debug = True


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
        for i in range(graph.vcount()):
            if self.numOfNodesWithDegree[i] != 0:
                self.avgClusterCoefficient[i] = self.sumOfClusterCoefficients[i] / self.numOfNodesWithDegree[i]
        print(self.avgClusterCoefficient)

    def findTriangles(self):
        for v in self.graph.vs:
            if debug:
                print(v)
            # note: the size of this neighbours list is the degree of the node
            neighbours = v.neighbors()
            numOfTriangles = 0

            # if it has less than two neighbours, skip it, as it cannot possibly be part of a triangle
            if len(neighbours) > 1 :
                # now that we have the neighbours we can check for triangles by going over each pair of neighbours
                # and checking if said neighbours are themselves connected
                b=len(neighbours)

                for n1 in range(len(neighbours)):
                    for n2 in range(n1 + 1, len(neighbours)):
                        if n1 != n2:
                            if self.graph.get_eid(n1, n2, directed=False, error=True) != -1:
                                numOfTriangles = numOfTriangles + 1
                        else:
                            pass # Fixing this would mean messing with a lot of index stuff. And it should only happen once of every vertex
                            #raise Exception("Trying to look for triangle with two identical nodes")

                clusterCoefficient = 2*numOfTriangles / (len(neighbours) * (len(neighbours)-1) )
                if debug:
                    print(numOfTriangles)
                    print(clusterCoefficient)
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
    the_graph = Generator(delta=0.5, gamma=0.5, beta=1, n=10)
    the_graph.gtriv
    the_graph.ghma
    #Generator.draw(the_graph.gtriv)

    triangles = TriangleFinder(the_graph.simplegraph())


