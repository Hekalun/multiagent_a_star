from pyvisgraph.visible_vertices import edge_distance
from pyvisgraph.visible_vertices import visible_vertices
from heapdict import heapdict
import random


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

def neighbors(v, edges):
    res = set()
    for e in edges:
        res.add(e.get_adjacent(v))
    return res


def a_star_multi(graph, agents, add_to_visgraph, heuristic=lambda x, y: 0):

    frontiers = {}
    g_scores = {}
    Ps = {}
    locations = {}
    accum_dists = {}

    for (origin, destination) in agents:
        frontiers[origin] = heapdict()
        g_scores[origin] = {}
        Ps[origin] = {}
        Ps[origin][origin] = origin
        locations[origin] = origin

        frontiers[origin][origin] = 0
        g_scores[origin][origin] = 0
        accum_dists[origin] = 0


    # Each timestep of A*
    agents_copy = list(agents)
    while len(agents_copy) > 0:
        occupied = set()

        # comment this out for sort agents via f score
        agents_copy.sort(reverse=True, key=lambda x: accum_dists[x[0]] + edge_distance(x[1], locations[x[0]]))

        # or comment this out for shuffle randomly
        #random.shuffle(agents_copy)

        for (origin, destination) in agents_copy:

            frontier = frontiers[origin]
            v = None
            while frontier:
                v, _ = frontier.popitem()
                if v not in occupied:
                    break

            # if no paths, remove agent from agents
            if v is None:
                Ps[origin] = None
                agents_copy.remove((origin, destination))
                continue

            occupied.add(v)
            locations[origin] = v
            P = Ps[origin]
            accum_dists[origin] += edge_distance(v, P[v])

            # if found result, remove agent from agents
            if v == destination:
                agents_copy.remove((origin, destination))

            # else expand
            edges = graph[v]
            if add_to_visgraph != None and len(add_to_visgraph[v]) > 0:
                edges = add_to_visgraph[v] | graph[v]

            g_score = g_scores[origin]

            for e in edges:
                w = e.get_adjacent(v)
                new_score = g_score[v] + edge_distance(v, w)
                if w not in g_score or new_score < g_score[w]:
                    g_score[w] = new_score

                    h = heuristic(w, destination)

                    # comment this block out for look_ahead heuristics:
                    '''
                    nbs = neighbors(w, add_to_visgraph[w] | graph[w])
                    if destination not in nbs:
                        turn = False
                        for x in nbs:
                            if destination in neighbors(x, add_to_visgraph[x] | graph[x]):
                                turn = True
                                break
                        if turn:
                            h *= 1.4
                        else:
                            h *= 2
                    '''
                    
                        
                            

                    frontier[w] = (new_score + h, w)
                    P[w] = v

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


def shortest_path_parallel(graph, agents, h, add_to_visg=None):
    #Ps = a_star_multi(graph, agents, add_to_visg, edge_distance)
    Ps = a_star_multi(graph, agents, add_to_visg, h)
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

