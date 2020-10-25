#! /usr/bin/env python

__author__ = 'Rodion "rodde" Efremov'


class Digraph:
    """This class implements a directed, weighted graph with nodes represented by integers. """

    def __init__(self):
        """Initializes this digraph."""
        self.nodes = set()
        self.children = dict()
        self.parents = dict()
        self.edges = 0

    def add_node(self, node):
        """If 'node' is not already present in this digraph,
           adds it and prepares its adjacency lists for children and parents."""
        if node in self.nodes:
            return

        self.nodes.add(node)
        self.children[node] = dict()
        self.parents[node] = dict()

    def add_arc(self, tail, head, weight):
        """Creates a directed arc pointing from 'tail' to 'head' and assigns 'weight' as its weight."""
        if tail not in self.nodes:
            self.add_node(tail)

        if head not in self.nodes:
            self.add_node(head)

        self.children[tail][head] = weight
        self.parents[head][tail] = weight
        self.edges += 1

    def has_arc(self, tail, head):
        if tail not in self.nodes:
            return False

        if head not in self.nodes:
            return False

        return head in self.children[tail].keys()

    def get_arc_weight(self, tail, head):
        if tail not in self.nodes:
            raise Exception("The tail node is not present in this digraph.")

        if head not in self.nodes:
            raise Exception("The head node is not present in this digraph.")

        if head not in self.children[tail].keys():
            raise Exception("The edge (", tail, ", ", head, ") is not in this digraph.")

        return self.children[tail][head]

    def remove_arc(self, tail, head):
        """Removes the directed arc from 'tail' to 'head'."""
        if tail not in self.nodes:
            return

        if head not in self.nodes:
            return

        del self.children[tail][head]
        del self.parents[head][tail]
        self.edges -= 1

    def remove_node(self, node):
        """Removes the node from this digraph. Also, removes all arcs incident on the input node."""
        if node not in self.nodes:
            return

        self.edges -= len(self.children[node]) + len(self.parents[node])

        # Unlink children:
        for child in self.children[node]:
            del self.parents[child][node]

        # Unlink parents:
        for parent in self.parents[node]:
            del self.children[parent][node]

        del self.children[node]
        del self.parents [node]
        self.nodes.remove(node)

    def __len__(self):
        return len(self.nodes)

    def number_of_arcs(self):
        return self.edges

    def get_parents_of(self, node):
        """Returns all parents of 'node'."""
        if node not in self.nodes:
            return []

        return self.parents[node].keys()

    def get_children_of(self, node):
        """Returns all children of 'node'."""
        if node not in self.nodes:
            return []

        return self.children[node].keys()

    def clear(self):
        del self.nodes[:]
        self.children.clear()
        self.parents.clear()
        self.edges = 0


def test():
    digraph = Digraph()
    assert len(digraph) == 0

    for i in range(10):
        assert len(digraph) == i
        digraph.add_node(i)
        assert len(digraph) == i + 1

    digraph.remove_node(8)
    assert len(digraph) == 9
    digraph.remove_node(9)
    assert len(digraph) == 8
    assert digraph.number_of_arcs() == 0

    digraph.add_arc(8, 7, 20.0)
    assert digraph.has_arc(8, 7)
    assert 20.0 == digraph.get_arc_weight(8, 7)
    assert digraph.number_of_arcs() == 1

    digraph.add_arc(9, 8, 10.0)
    assert digraph.number_of_arcs() == 2
    assert digraph.get_arc_weight(9, 8) == 10.0
    assert digraph.has_arc(9, 8)
    assert not digraph.has_arc(8, 9)
    digraph.remove_node(8)
    assert not digraph.has_arc(9, 8)
    assert digraph.number_of_arcs() == 0

    digraph.remove_node(5)
    assert len(digraph) == 8

    digraph.add_arc(0, 3, 1.0)
    digraph.add_arc(1, 3, 2.0)
    digraph.add_arc(3, 6, 3.0)
    digraph.add_arc(3, 7, 4.0)

    assert digraph.number_of_arcs() == 4

    assert 0 in digraph.get_parents_of(3)
    assert 1 in digraph.get_parents_of(3)
    assert 6 in digraph.get_children_of(3)
    assert 7 in digraph.get_children_of(3)

    try:
        digraph.get_arc_weight(3, 100)
        assert False
    except Exception:
        pass

    try:
        digraph.get_arc_weight(100, 3)
        assert False
    except Exception:
        pass

    try:
        digraph.get_arc_weight(2, 3)
        assert False
    except Exception:
        pass

if __name__ == "__main__":
    test()