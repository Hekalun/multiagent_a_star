from pyvisgraph.visible_vertices import edge_distance
from heapdict import heapdict


def a_star(graph, origin, destination, add_to_visgraph, heuristic=lambda x, y: 0):
    frontier = heapdict()
    g_score = {}
    P = {}

    frontier[origin] = 0
    g_score[origin] = 0

    while frontier:
        v, _ = frontier.popitem()
        print(v)

        # if found result, return
        if v == destination:
            return P

        # else expand
        edges = graph[v]
        if add_to_visgraph != None and len(add_to_visgraph[v]) > 0:
            edges = add_to_visgraph[v] | graph[v]
        for e in edges:
            w = e.get_adjacent(v)
            new_score = g_score[v] + edge_distance(v, w)
            if w not in g_score or new_score < g_score[w]:
                g_score[w] = new_score
                frontier[w] = (new_score + heuristic(w, destination), w)
                P[w] = v

    return None


def shortest_path(graph, origin, destination, add_to_visgraph=None):
    P = a_star(graph, origin, destination, add_to_visgraph, edge_distance)
    path = []
    while 1:
        path.append(destination)
        if destination == origin: break
        destination = P[destination]
    path.reverse()
    return path
