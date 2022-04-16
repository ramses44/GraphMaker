class Nodes(type):
    _nodes = set()

    def __call__(cls, *args, **kwargs):
        nw = super(Nodes, cls).__call__(*args, **kwargs)
        cls._nodes.add(nw)
        return nw


class Node(metaclass=Nodes):
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.neigh = dict()

    def link(self, other):
        self.neigh[other] = self.neigh.get(other, 0) + 1

    def unlink(self, other):
        if self.neigh[other] == 1:
            self.neigh.pop(other)
        else:
            self.neigh[other] -= 1

    def __del__(self):
        for other in self.__class__._nodes:
            if self in other.neigh:
                other.neigh.pop(self)
        self.__class__._nodes.discard(self)

    def __hash__(self):
        return self.x * self.y + self.x + self.y

    def __repr__(self):
        return f"Node №{self.num} at {self.x, self.y}"


def make_edges_set(nodes, orient=False):
    res = []

    for node in nodes:
        for neigh, count in node.neigh.items():
            for _ in range(count):
                res.append((node.num, neigh.num))

    return res


def make_matrix(nodes, orient=False):
    n = max(map(lambda x: x.num, nodes))
    m = [[0] * n for _ in range(n)]

    for node in nodes:
        for neigh, count in node.neigh.items():
            m[node.num - 1][neigh.num - 1] += count
            if not orient:
                m[neigh.num - 1][node.num - 1] += count

    return m






