import numpy as np
import igraph as ig


debug = True

class generator():
    def __init__(self,
            n,
            gamma,
            beta,
            delta
    ):
        self.n = n
        self.gamma = gamma
        self.beta = beta
        self.delta =delta
        #self.g = ig.Graph()
        generator.make_graph(self.n)

    # TODO
    def hpa(s, t) -> bool:
        """
        hpa function
        @param s: weight of left node
        @param t: weight of right node
        @return: True if hMax < 1
        """
        h = 1 / beta * max(s, t) ** (1 - gamma) - min(s, t) ** gamma
        return h < 1


    def hmax(s, t) -> bool:
        """
        hMax function
        @param s: weight of left node
        @param t: weight of right node
        @return: True if hMax < 1
        """
        h = (1 / beta) * max(s, t) ** (1 + gamma)
        return h < 1


    def htriv(s, t):
        if (abs(s - t) < 1):
            return True
        return False


    def generate_weigths(amount):
        """
        Generates the weights
        @param amount: amount of weights
        @return: list of rv in [0,1]
        """
        return np.random.random(amount)


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


    def make_vertices(n):
        g = ig.Graph()
        g.add_vertices(n)
        # Make the graph and atributes
        g.vs["x"] = generator.generate_positions(n)
        g.vs["y"] = generator.generate_positions(n)
        coords = []
        for i in range(n):
            x = round(g.vs[i]["x"], 2)
            y = round(g.vs[i]["y"], 2)
            coords.append((x, y))
        g.vs["coords"] = coords
        g.vs["weight"] = generator.generate_weigths(n)
        return g


    def edges_triv(g):
        # Make edges
        for i in range(len(g.vs)):
            for j in range(i + 1, len(g.vs)):
                s = g.vs[i]
                t = g.vs[j]
                if generator.htriv(s["weight"], t["weight"]):
                    edge = g.add_edge(s, t)  # add_edges is mss sneller.
                    edge["method"] = "triv"
                    if debug:
                        print("adding edge type triv \n {} \n {}".format(s, t))

        return g


    def edges_hpa(g):
        # Make edges
        for i in range(len(g.vs)):
            for j in range(i + 1, len(g.vs)):
                s = g.vs[i]
                t = g.vs[j]
                if generator.hpa(s["weight"], t["weight"]):
                    edge = g.add_edge(s, t)  # add_edges is mss sneller.
                    edge["method"] = "hpa"
                    if debug:
                        print("adding edge type hpa \n {} \n {}".format(s, t))

        return g


    def edges_hmax(g):
        # Make edges
        for i in range(len(g.vs)):
            for j in range(i + 1, len(g.vs)):
                s = g.vs[i]
                t = g.vs[j]
                if generator.hmax(s["weight"], t["weight"]):
                    edge = g.add_edge(s, t)  # add_edges is mss sneller.
                    edge["method"] = "hmax"
                    if debug:
                        print("adding edge type hmax \n {} \n {}".format(s, t))
        return g


    def make_graph(n):
        g = generator.make_vertices(n)
        g["delta"] = delta
        g["gamma"] = gamma
        g["beta"] = beta
        g["n"] = n
        generator.edges_triv(g)
        generator.edges_hmax(g)
        generator.edges_hpa(g)
        print(ig.GraphSummary(g, verbosity=1,
                              print_edge_attributes=True,
                              # print_graph_attributes=True,
                              # print_vertex_attributes=True
                              ))
        generator.draw(g)


    def draw(g):
        visual_style = {
            "vertex_label": g.vs["coords"],
            "edge_label": g.es["method"]
        }
        ig.plot(g, layout=g.vs["coords"], **visual_style)


if __name__ == '__main__':
    # parameters
    delta = 0  # model parameter
    gamma = 0.5  # model parameter
    beta = 1  # model parameter
    n = 20  # amount of nodes

    generator.make_graph(5)
