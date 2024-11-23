class Preprocessor:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.loads = []
        self.boundary_conditions = []

    def add_node(self, x, y):
        self.nodes.append((x, y))

    def add_element(self, node1, node2, A, E, sigma_max, section_type, k, b, r):
        self.elements.append({
            'node1': node1,
            'node2': node2,
            'A': A,
            'E': E,
            'sigma_max': sigma_max,
            'section_type': section_type,
            'k': k,
            'b': b,
            'r': r
        })

    def add_load(self, load_type, node1, node2=None, F=None):
        if load_type == "Сосредоточенная":
            self.loads.append({
                'type': load_type,
                'node': node1,
                'F': F
            })
        elif load_type == "Распределенная":
            self.loads.append({
                'type': load_type,
                'node1': node1,
                'node2': node2,
                'F': F
            })

    def add_boundary_condition(self, node, u, v):
        self.boundary_conditions.append({
            'node': node,
            'u': u,
            'v': v
        })
