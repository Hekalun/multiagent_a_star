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

#########################################################################################################

def a_star_multi(graph, origin, destination, occupied, add_to_visgraph, g_score, frontier,start, heuristic=lambda x, y: 0):
    #occupied: a set of occupied vertices by other agents
    #return: a list of list of vertices
    #frontier = heapdict()
    #g_score = {}
    P = None
    print("aster origin:",origin,"astar dest:",destination)

    if start:  
        frontier[origin] = 0
        g_score[origin] = 0


    while frontier:
        v, _ = frontier.popitem()

        # if found result, return
        if v == destination:
            return P, g_score, frontier

        # else expand
        edges = graph[v]
        if add_to_visgraph != None and len(add_to_visgraph[v]) > 0:
            edges = add_to_visgraph[v] | graph[v]
    
        for e in edges:
            w = e.get_adjacent(v)
            print("W:",w,"V:",v)

            if w in occupied:
                continue
            new_score = g_score[v] + edge_distance(v,w)
            
            if w not in g_score or new_score < g_score[w]:
                g_score[w] = new_score
                frontier[w] = (new_score + heuristic(w, destination), w)
                print("w:",w, frontier[w])
            
        min_score = 10^99  
        min_key = None
        for key in frontier:
            if key != origin and frontier[key][0]<min_score:
                min_score,min_key = frontier[key]
        print("P set to:",min_key)
        return min_key, g_score, frontier



def shortest_path_multi(graph, origin, destination, occupied, g_score, frontier, add_to_visgraph=None, start = False):
    return a_star_multi(graph, origin, destination, occupied, add_to_visgraph, g_score, frontier, start,edge_distance)
    




