from pyvisgraph.visible_vertices import edge_distance
from heapdict import heapdict


def a_star_single(graph, origin, destination, add_to_visgraph, occupied, heuristic=lambda x, y: 0):
    frontier = heapdict()
    g_score = {}
    P = {}

    frontier[origin] = 0
    g_score[origin] = 0

    timestep = 0
    while frontier:
        v, _ = frontier.popitem()

        if timestep >= len(occupied):
            occupied.append(set())

        if v in occupied[timestep]:
            continue

        # record expanded nodes
        occupied[timestep].add(v)
        timestep += 1

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


def a_star_multi(graph, agents, add_to_visgraph, heuristic=lambda x, y: 0):

    frontiers = {}
    g_scores = {}
    Ps = {}

    for (origin, destination) in agents:
        frontiers[origin] = heapdict()
        g_scores[origin] = {}
        Ps[origin] = {}

        frontiers[origin][origin] = 0
        g_scores[origin][origin] = 0

    # Each timestep of A*
    agents_copy = list(agents)
    # i = 0
    while len(agents_copy) > 0:
        occupied = set()

        # print("Step ", i)
        # i += 1

        # Move each agent by one step sequentially
        # j = 1
        for (origin, destination) in agents_copy:

            # print("Agent ", j)
            # j += 1

            frontier = frontiers[origin]
            v = None
            while frontier:
                v, _ = frontier.popitem()
                # print("popped ", v)
                if v not in occupied:
                    break
                # else:
                #     print("v occupied, continue popping")

            # if no paths, remove agent from agents
            if v is None:
                Ps[origin] = None
                agents_copy.remove((origin, destination))
                # print("Frontier empty, pass")
                continue

            occupied.add(v)
            # print("Expanded ", v)

            # if found result, remove agent from agents
            if v == destination:
                agents_copy.remove((origin, destination))
                # print("Reached destination")

            # else expand
            edges = graph[v]
            if add_to_visgraph != None and len(add_to_visgraph[v]) > 0:
                edges = add_to_visgraph[v] | graph[v]

            g_score = g_scores[origin]
            P = Ps[origin]

            for e in edges:
                w = e.get_adjacent(v)
                new_score = g_score[v] + edge_distance(v, w)
                if w not in g_score or new_score < g_score[w]:
                    g_score[w] = new_score
                    frontier[w] = (new_score + heuristic(w, destination), w)
                    P[w] = v
                    # print(w, " added to frontier")

    return Ps


def shortest_path_single(graph, origin, destination, add_to_visgraph=None, occupied=None):
    P = a_star_single(graph, origin, destination, add_to_visgraph, occupied, edge_distance)
    path = []
    while 1:
        path.append(destination)
        if destination == origin: break
        destination = P[destination]
    path.reverse()
    return path


def shortest_path_parallel(graph, agents, add_to_visg=None):
    Ps = a_star_multi(graph, agents, add_to_visg, edge_distance)
    paths = []
    for (origin, destination) in agents:
        P = Ps[origin]
        if P is None:
            paths.append(None)
            continue
        path = []
        while 1:
            path.append(destination)
            if destination == origin:
                break
            destination = P[destination]
        path.reverse()
        paths.append(path)
    return paths


#########################################################################################################

# def a_star_multi(graph, origin, destination, occupied, add_to_visgraph, g_score, frontier,start, heuristic=lambda x, y: 0):
#     #occupied: a set of occupied vertices by other agents
#     #return: a list of list of vertices
#     #frontier = heapdict()
#     #g_score = {}
#     P = None
#     print("aster origin:", origin,"astar dest:", destination)
#
#     if start:
#         frontier[origin] = 0
#         g_score[origin] = 0
#
#     while frontier:
#         v, _ = frontier.popitem()
#
#         # if found result, return
#         if v == destination:
#             return P, g_score, frontier
#
#         # else expand
#         edges = graph[v]
#         if add_to_visgraph != None and len(add_to_visgraph[v]) > 0:
#             edges = add_to_visgraph[v] | graph[v]
#
#         for e in edges:
#             w = e.get_adjacent(v)
#             print("W:",w,"V:",v)
#
#             if w in occupied:
#                 continue
#             new_score = g_score[v] + edge_distance(v,w)
#
#             if w not in g_score or new_score < g_score[w]:
#                 g_score[w] = new_score
#                 frontier[w] = (new_score + heuristic(w, destination), w)
#                 print("w:",w, frontier[w])
#
#         min_score = 10^99
#         min_key = None
#         for key in frontier:
#             if key != origin and frontier[key][0]<min_score:
#                 min_score,min_key = frontier[key]
#         print("P set to:",min_key)
#         return min_key, g_score, frontier
#
#
#
# def shortest_path_multi(graph, origin, destination, occupied, g_score, frontier, add_to_visgraph=None, start = False):
#     return a_star_multi(graph, origin, destination, occupied, add_to_visgraph, g_score, frontier, start, edge_distance)
#




