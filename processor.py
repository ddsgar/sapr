import numpy as np

class Processor:
    def __init__(self, nodes, elements, loads, boundary_conditions):
        self.nodes = nodes
        self.elements = elements
        self.loads = loads
        self.boundary_conditions = boundary_conditions

    def assemble_global_matrix(self):
        n = len(self.nodes)
        K = np.zeros((n, n))
        b = np.zeros(n)

        for elem in self.elements:
            node1 = elem['node1']
            node2 = elem['node2']
            A = elem['A']
            E = elem['E']
            L = np.linalg.norm(np.array(self.nodes[node2]) - np.array(self.nodes[node1]))

            k_local = (E * A / L) * np.array([[1, -1], [-1, 1]])

            K[node1, node1] += k_local[0, 0]
            K[node1, node2] += k_local[0, 1]
            K[node2, node1] += k_local[1, 0]
            K[node2, node2] += k_local[1, 1]

        for load in self.loads:
            node = load['node']
            F = load['F']
            b[node] += F

        for bc in self.boundary_conditions:
            node = bc['node']
            u = bc['u']
            v = bc['v']
            if u == 0:
                K[node, :] = 0
                K[:, node] = 0
                K[node, node] = 1
                b[node] = 0

        return K, b

    def solve(self):
        K, b = self.assemble_global_matrix()
        u = np.linalg.solve(K, b)
        return u

    def calculate_stresses(self, u):
        stresses = []
        for elem in self.elements:
            node1 = elem['node1']
            node2 = elem['node2']
            A = elem['A']
            E = elem['E']
            L = np.linalg.norm(np.array(self.nodes[node2]) - np.array(self.nodes[node1]))

            delta_u = u[node2] - u[node1]
            sigma = E * delta_u / L
            stresses.append(sigma)

        return stresses
