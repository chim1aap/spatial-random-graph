import igraph as ig
import numpy as np

debug = True


class Generator:
    def __init__(self,
                 n: int,
                 gamma: float,
                 beta: float,
                 delta: float
                 ) -> ig.Graph():
        self.n = n
        self.gamma = gamma
        self.beta = beta
        self.delta = delta
        # self.g = ig.Graph()
        self.g = self.make_graph()

    def hpa(self, s, t) -> bool:
        """
        hpa function
        @param s: weight of left node
        @param t: weight of right node
        @return: True if hMax < 1
        """
        h = 1 / self.beta * max(s, t) ** (1 - self.gamma) - min(s, t) ** self.gamma
        return h < 1

    def hmax(self, s, t) -> bool:
        """
        hMax function
        @param s: weight of left node
        @param t: weight of right node
        @return: True if hMax < 1
        """
        h = (1 / self.beta) * max(s, t) ** (1 + self.gamma)
        return h < 1

    @staticmethod
    def htriv(s, t):
        """
        A trivial h function
        :param s: left weight
        :param t: right weight
        :return: boolean
        """
        if abs(s - t) < 1:
            return True
        return False

    @staticmethod
    def generate_weigths(amount):
        """
        Generates the weights
        @param amount: amount of weights
        @return: list of rv in [0,1]
        """
        return np.random.random(amount)

    @staticmethod
    def generate_positions(size):
        """
        generates a list of `size`
        @param size: integer
        @return: list of random variables in_R [-n/2,n/2]
        """
        ans = np.random.random(size)  # list in [0,1]
        ans = ans * size  # list in [0,n]
        ans = ans - 0.5 * size  # list in [-n/2,n/2
        return ans

    @staticmethod
    def make_vertices(n):
        """
        Creates a graph of n vertices.
        :param n: graph size
        :return: graph
        """
        g = ig.Graph()
        g.add_vertices(n)
        # Make the graph and atributes
        g.vs["x"] = Generator.generate_positions(n)
        g.vs["y"] = Generator.generate_positions(n)
        coords = []
        for i in range(n):
            x = round(g.vs[i]["x"], 2)
            y = round(g.vs[i]["y"], 2)
            coords.append((x, y))
        g.vs["coords"] = coords
        g.vs["weight"] = Generator.generate_weigths(n)
        return g

    def edges_triv(self, g):
        # Make edges
        for i in range(len(g.vs)):
            for j in range(i + 1, len(g.vs)):
                s = g.vs[i]
                t = g.vs[j]
                if self.htriv(s["weight"], t["weight"]):
                    edge = g.add_edge(s, t)  # add_edges is mss sneller.
                    edge["method"] = "triv"
                    if debug:
                        print("adding edge type triv \n {} \n {}".format(s, t))

        return g

    def edges_hpa(self, g):
        # Make edges
        for i in range(len(g.vs)):
            for j in range(i + 1, len(g.vs)):
                s = g.vs[i]
                t = g.vs[j]
                if self.hpa(s["weight"], t["weight"]):
                    edge = g.add_edge(s, t)  # add_edges is mss sneller.
                    edge["method"] = "hpa"
                    if debug:
                        print("adding edge type hpa \n {} \n {}".format(s, t))

        return g

    def edges_hmax(self, g):
        # Make edges
        for i in range(len(g.vs)):
            for j in range(i + 1, len(g.vs)):
                s = g.vs[i]
                t = g.vs[j]
                if self.hmax(s["weight"], t["weight"]):
                    edge = g.add_edge(s, t)  # add_edges is mss sneller.
                    edge["method"] = "hmax"
                    if debug:
                        print("adding edge type hmax \n {} \n {}".format(s, t))
        return g

    def make_graph(self):
        g = Generator.make_vertices(self.n)
        g["delta"] = self.delta
        g["gamma"] = self.gamma
        g["beta"] = self.beta
        g["n"] = self.n
        Generator.edges_triv(self, g)
        Generator.edges_hmax(self, g)
        Generator.edges_hpa(self, g)
        print(ig.GraphSummary(g, verbosity=1,
                              print_edge_attributes=True,
                              # print_graph_attributes=True,
                              # print_vertex_attributes=True
                              ))
        Generator.draw(g)

        return g

    @staticmethod
    def draw(g):
        """
        Draws the graph
        :param g: g
        :return: the picture
        """
        visual_style = {
            "vertex_label": g.vs["coords"],
            "edge_label": g.es["method"],
            "vertex_size": 20,
            #"bbox" : (g["n"],g["n"] ) #TODO
        }
        print(g["n"])
        return ig.plot(g, layout=g.vs["coords"], **visual_style)


if __name__ == '__main__':
    # parameters
    # delta = 0  # model parameter
    # gamma = 0.5  # model parameter
    # beta = 1  # model parameter
    # n = 20  # amount of nodes
    the_graph = Generator(delta=0.5, gamma=0.5, beta=1, n=20)
